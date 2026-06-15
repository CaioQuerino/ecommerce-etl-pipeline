import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.initialize_spark import initialize_spark
from utils.initialize_client import get_client
from utils.initialize_logging import initialize_logging
from schemas.schema_logs_request import get_schema
from pyspark.sql import functions as F

def process() :

    spark = initialize_spark()
    logger = initialize_logging()
    schema = get_schema()
    s3_client = get_client("s3")

    bucket_name = "data-lake-logs-request-analytics"
    input_path = f"s3a://{bucket_name}/raw/logs/*.csv"

    logger.info("Iniciando ingestão de logs do S3...")

    df = spark.read.csv(input_path, schema=schema, header=True)

    if df.limit(1).count() > 0:
        logger.info("Aplicando regras de anonimização LGPD...")
        df_anonymized = df.withColumn("client_ip_hash", F.sha2(F.col("client_ip"), 256)) \
                          .drop("client_ip")
        
        logger.info("Gerando agregações de auditoria...")
        df_metrics = (
            df_anonymized
            .groupBy("uri")
            .agg(
                F.count("*").alias("total_accesses"),
                F.countDistinct("client_ip_hash").alias("unique_visitors"),
                F.avg("response_size_bytes").alias("avg_response_size"),
                F.sum(
                    F.when(F.col("status_code") == 200, 1)
                    .otherwise(0)
                ).alias("success_count"),
                F.sum(
                    F.when(F.col("status_code") >= 400, 1)
                    .otherwise(0)
                ).alias("error_count")
            )
            .withColumn(
                "processed_at",
                F.current_timestamp()
            )
        )

        logger.info("Persistindo dados no ScyllaDB...")
        df_metrics.write \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="audit_metrics", keyspace="request_logs") \
            .mode("append") \
            .save()

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