
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, when
from pyspark.sql.types import StructType, IntegerType, StringType, TimestampType
from sqlalchemy.orm import sessionmaker
from models import Purchase
from database import SessionLocal
import logging
import os
from datetime import datetime

# Suppress Spark internal logging
logging.getLogger("py4j").setLevel(logging.ERROR)
os.environ["PYSPARK_LOG_LEVEL"] = "ERROR"

# Kafka message schema
schema = StructType() \
    .add("id", IntegerType()) \
    .add("email", StringType()) \
    .add("purchase_id", StringType()) \
    .add("timestamp", StringType())

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaConsumerWithSurge") \
    .config("spark.jars", "jars/spark-sql-kafka-0-10_2.12-3.5.0.jar,jars/kafka-clients-4.0.0.jar") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sqlite_purchases_topic") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON values
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select(
        col("data.id"),
        col("data.email"),
        col("data.purchase_id").cast("int").alias("purchase_id"),
        col("data.timestamp").cast("timestamp").alias("timestamp")
    )

# Add watermark and aggregate counts per 1-minute window
parsed_df_with_watermark = parsed_df.withWatermark("timestamp", "1 minute")

purchase_counts = parsed_df_with_watermark \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("purchase_id")
    ).count()

# Hardcoded product base prices
price_df = spark.createDataFrame([
    (1, 3.99),
    (2, 2.99),
    (3, 4.99),
    (4, 5.99),
    (5, 2.99),
    (6, 9.99),
    (7, 19.99),
    (8, 19.99),
    (9, 6.99)
], ["purchase_id", "base_price"])


# Join with prices and calculate surge
enriched = purchase_counts \
    .join(price_df, on="purchase_id", how="left") \
    .withColumn(
        "final_price",
        when(col("count") > 10, col("base_price") * 1.2).otherwise(col("base_price"))
    ) \
    .select("window", "purchase_id", "count", "base_price", "final_price")

# Write to DB and log
def insert_surge_purchase(spark_df, batch_id):
    print("\n======================================")
    print(f" Processing Batch ID: {batch_id}")
    print("======================================")
    spark_df.show(truncate=False)

    rows = spark_df.collect()
    db = SessionLocal()

    for row in rows:
        print(f"Writing to DB: Product {row.purchase_id} | "
              f"Base: {row.base_price} | Surge: {row.final_price} | "
            #   f"Time: {datetime.now()}"
            )
        if row.base_price is None or row.final_price is None:
            print(f"⚠️ Skipping row with missing price info: {row}")
            continue

        surge_applied = row.final_price > row.base_price
        if surge_applied:
            print(f"🚨 Surge detected for product {row.purchase_id}, "
                  f"price hiked from {row.base_price} to {row.final_price}")

        purchase = Purchase(
            email="surge@system",
            product_id=int(row.purchase_id),
            timestamp=datetime.utcnow(),
            base_price=row.base_price,
            surge_price=row.final_price
        )
        db.add(purchase)

    db.commit()
    db.close()

# Attach streaming write
query = enriched.writeStream \
    .outputMode("update") \
    .foreachBatch(insert_surge_purchase) \
    .start()

query.awaitTermination()
