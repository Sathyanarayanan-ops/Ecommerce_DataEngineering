import sqlite3
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka():
    conn = sqlite3.connect('purchases.db')
    cursor = conn.cursor()
    
    last_id = 0

    while True:
        cursor.execute("SELECT * FROM purchases WHERE id > ?", (last_id,))
        rows = cursor.fetchall()
        
        for row in rows:
            data = {
                "id": row[0],
                "email": row[1],  
                "purchase_id": row[2],  
                "timestamp": row[3]
            }
            
            print(f"Sending data to Kafka: {data}")
            
            producer.send("sqlite_purchases_topic", data)
            
            last_id = row[0]

        time.sleep(4)  # Batch every 4 seconds

send_to_kafka()


# import sqlite3
# import json
# import time
# import logging
# from kafka import KafkaProducer
# from kafka.errors import KafkaError

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class SQLiteCDC:
#     def __init__(self):
#         self.producer = KafkaProducer(
#             bootstrap_servers='localhost:9092',
#             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#             acks='all',
#             retries=3,
#             linger_ms=100
#         )
#         self.last_id = self.load_last_offset()

#     @staticmethod
#     def load_last_offset():
#         try:
#             with open('offset.dat', 'r') as f:
#                 return int(f.read())
#         except (FileNotFoundError, ValueError):
#             return 0

#     @staticmethod
#     def save_last_offset(offset):
#         with open('offset.dat', 'w') as f:
#             f.write(str(offset))

#     def run(self):
#         while True:
#             try:
#                 with db_connection() as conn:
#                     cursor = conn.cursor()
#                     records = fetch_new_records(cursor, self.last_id)
                    
#                     if records:
#                         self.process_records(records)
                        
#                     time.sleep(1)  # Reduced sleep for better latency

#             except (sqlite3.OperationalError, KafkaError) as e:
#                 logger.error(f"Error occurred: {str(e)}")
#                 time.sleep(5)  # Backoff on error

#     def process_records(self, records):
#         try:
#             for row in records:
#                 data = {
#                     "id": row[0],
#                     "email": row[1],
#                     "purchase_id": row[2],
#                     "timestamp": row[3]
#                 }
                
#                 future = self.producer.send(
#                     "sqlite_purchases_topic",
#                     value=data,
#                     key=str(row[0]).encode()  # Key by ID for ordering
#                 )
                
#                 # Block until confirmation
#                 future.get(timeout=10)
                
#                 self.last_id = row[0]
#                 self.save_last_offset(self.last_id)
                
#                 logger.info(f"Sent record {row[0]}")

#         except Exception as e:
#             logger.error(f"Failed to process records: {str(e)}")
#             raise

# if __name__ == "__main__":
#     cdc = SQLiteCDC()
#     cdc.run()