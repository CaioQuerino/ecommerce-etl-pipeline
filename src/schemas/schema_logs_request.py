from pyspark.sql.types import (
    StructType, 
    StructField,
    TimestampType,
    StringType,
    IntegerType
)

def get_schema() -> StructType :
    return StructType ([
        StructField("timestamp", TimestampType(), True),
        StructField("client_ip", StringType(), True),
        StructField("method", StringType(), True),
        StructField("uri", StringType(), True),
        StructField("status_code", IntegerType(), True),
        StructField("response_size_bytes", IntegerType(), True),
        StructField("user_agent", StringType(), True)
    ])