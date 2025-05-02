import sqlite3
import json
import time
from kafka import KafkaProducer

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

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
            
            #producer.send("sqlite_purchases_topic", data)
            
            last_id = row[0]

        time.sleep(4)  # Batch every 2 seconds

send_to_kafka()