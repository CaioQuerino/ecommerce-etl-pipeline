import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.initialize_spark import initialize_spark
from utils.initialize_client import get_client
from schemas.schema_logs_ecommerce import get_schema

from dotenv import load_dotenv

load_dotenv()

def process() :

    spark = initialize_spark()
    schema = get_schema()
    s3_client = get_client("s3")

    input_path = f"s3a://{os.getenv("S3_BUCKET_NAME")}/raw/logs/*.csv"
    output_path = f"s3a://{os.getenv("S3_BUCKET_NAME")}/processed/logs/"

    df = spark.read.csv(input_path, schema=schema, header=True)

    if not df.isEmpty():
        df_processed = df.filter(df.membership == "Premium") \
                         .drop("ip", "accessed_Ffom", "language", "pay_method", "returned_amount", "returned", "sales") \
        
        df_processed.write.mode("overwrite").parquet(output_path)

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