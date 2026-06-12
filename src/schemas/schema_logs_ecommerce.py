from pyspark.sql.types import (
    StructType, 
    StructField,
    TimestampType,
    IntegerType,
    StringType,
    DoubleType
)

def get_schema() -> StructType :
    return StructType([
    StructField("accessed_date", TimestampType(), True),
    StructField("duration_(secs)", IntegerType(), True),
    StructField("network_protocol", StringType(), True),
    StructField("ip", StringType(), True),
    StructField("bytes", IntegerType(), True),
    StructField("accessed_Ffom", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("gender", StringType(), True),
    StructField("country", StringType(), True),
    StructField("membership", StringType(), True),
    StructField("language", StringType(), True),
    StructField("sales", DoubleType(), True),
    StructField("returned", StringType(), True),
    StructField("returned_amount", DoubleType(), True),
    StructField("pay_method", StringType(), True)
])