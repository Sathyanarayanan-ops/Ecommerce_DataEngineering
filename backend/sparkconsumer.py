from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, IntegerType, StringType, TimestampType
 
schema = StructType() \
    .add("id", IntegerType()) \
    .add("email", StringType()) \
    .add("purchase_id", StringType()) \
    .add("timestamp", StringType())
    
spark = SparkSession.builder \
    .appName("KafkaConsumer") \
    .config("spark.jars", "jars/spark-sql-kafka-0-10_2.12-3.5.0.jar, jars/kafka-clients-4.0.0.jar") \
    .getOrCreate()
    
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sqlite_purchases_topic") \
    .option("startingOffsets", "latest") \
    .load()
    
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")
    
query = parsed_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .start()
 
query.awaitTermination()