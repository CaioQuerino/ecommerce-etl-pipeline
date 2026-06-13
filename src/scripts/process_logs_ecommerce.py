import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.initialize_spark import initialize_spark
from utils.initialize_client import get_client
from schemas.schema_logs_ecommerce import get_schema
from pyspark.sql import functions as F
import logging

from dotenv import load_dotenv

load_dotenv()

def process() :

    spark = initialize_spark()
    schema = get_schema()
    s3_client = get_client("s3")
    
    # Configuração básica de log (Dynatrace SDK pode capturar logs do stdout/stderr)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("DynatraceExecutionLogs")

    bucket_name = os.getenv("S3_BUCKET_NAME")
    input_path = f"s3a://{bucket_name}/raw/logs/*.csv"
    
    logger.info("Iniciando ingestão de logs do S3...")
    df = spark.read.csv(input_path, schema=schema, header=True)

    if df.limit(1).count() > 0:
        # 1. Limpeza e Anonimização (LGPD) - Mascarando o IP
        logger.info("Aplicando regras de anonimização LGPD...")
        df_anonymized = df.withColumn("ip_hash", F.sha2(F.col("ip"), 256)) \
                          .drop("ip", "language", "pay_method")

        # 2. Agregação de métricas para auditoria
        logger.info("Gerando agregações de auditoria...")
        df_metrics = df_anonymized.groupBy("membership").agg(
            F.count("*").alias("total_accesses"),
            F.current_timestamp().alias("processed_at")
        )
        
        # 3. Escrita no ScyllaDB (usando o protocolo Cassandra)
        logger.info("Persistindo dados no ScyllaDB...")
        df_metrics.write \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="audit_metrics", keyspace="ecommerce_logs") \
            .mode("append") \
            .save()

        bucket_name = os.getenv("S3_BUCKET_NAME")
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix="raw/logs/")
        
        if 'Contents' in response:
            for obj in response['Contents']:
                copy_source = {'Bucket': bucket_name, 'Key': obj['Key']}
                new_key = obj['Key'].replace("raw/logs/", "archive/logs/", 1)
                s3_client.copy_object(Bucket=bucket_name, CopySource=copy_source, Key=new_key)
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                
        spark.stop()
    else:
        spark.stop()

if __name__ == "__main__":
    process()