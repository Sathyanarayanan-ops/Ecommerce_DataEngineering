
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

# Define schema for incoming Kafka data
purchase_schema = StructType([
    StructField("id", IntegerType()),
    StructField("email", StringType()),
    StructField("purchase_id", StringType()),
    StructField("timestamp", TimestampType())
])

def surge_detection():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("SurgePriceDetection") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "sqlite_purchases_topic") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse JSON from Kafka value
    parsed_df = df.select(
        from_json(col("value").cast("string"), purchase_schema).alias("data")
    ).select("data.*")

    # Process stream with windowing
    windowed_counts = parsed_df \
        .withColumn("processing_time", current_timestamp()) \
        .groupBy(
            col("purchase_id"),
            window(col("processing_time"), "30 seconds")
        ) \
        .count() \
        .withColumn("surge_active", col("count") >= 10) \
        .withColumn("window_end", col("window").end) \
        .select(
            "purchase_id",
            "count",
            "surge_active",
            "window_end"
        )

    # Output results
    query = windowed_counts.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime="30 seconds") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    surge_detection()