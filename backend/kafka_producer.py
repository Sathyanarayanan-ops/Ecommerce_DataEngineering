import sqlite3
import json
import time
import logging
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_kafka_topic():
    """Ensure Kafka topic exists with proper configuration"""
    try:
        admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
        topic = NewTopic(
            name="sqlite_purchases_topic",
            num_partitions=3,
            replication_factor=1
        )
        admin.create_topics([topic])
        logger.info("Topic created successfully")
    except TopicAlreadyExistsError:
        logger.info("Topic already exists, skipping creation")
    except Exception as e:
        logger.error(f"Failed to create topic: {str(e)}")
        raise

def get_last_processed_id():
    """Retrieve last processed ID from file"""
    try:
        with open("last_processed.id", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

def save_last_processed_id(last_id):
    """Persist last processed ID to file"""
    with open("last_processed.id", "w") as f:
        f.write(str(last_id))

def produce_messages():
    """Main producer function"""
    # Create Kafka topic if needed
    create_kafka_topic()
    
    # Configure producer
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
        retries=3
    )
    
    # Database connection
    conn = sqlite3.connect("purchases.db")
    conn.row_factory = sqlite3.Row  # Access columns by name
    
    last_id = get_last_processed_id()
    
    try:
        while True:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM purchases WHERE id > ? ORDER BY id ASC",
                    (last_id,)
                )
                rows = cursor.fetchall()
                
                if not rows:
                    logger.info("No new messages, sleeping...")
                    time.sleep(4)
                    continue
                
                for row in rows:
                    data = dict(row)
                    try:
                        producer.send(
                            "sqlite_purchases_topic",
                            value=data
                        ).get(timeout=10)  # Wait for confirmation
                        last_id = data["id"]
                        save_last_processed_id(last_id)
                        logger.debug(f"Sent record {data['id']}")
                    except Exception as e:
                        logger.error(f"Failed to send {data['id']}: {str(e)}")
                        continue
                
                logger.info(f"Sent {len(rows)} new messages")
                
    finally:
        producer.flush()
        producer.close()
        conn.close()

if __name__ == "__main__":
    produce_messages()