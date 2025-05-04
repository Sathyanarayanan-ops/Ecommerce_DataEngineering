from kafka import KafkaConsumer
import json

def induce_price_surge(arr):
    """
    Check if there are 3 consecutive identical numbers in the array.
    """
    if len(arr) < 3:
        return None
    
    # Scan the array looking for 3 consecutive identical numbers
    for i in range(len(arr) - 2):
        if arr[i]["purchase_id"] == arr[i+1]["purchase_id"] == arr[i+2]["purchase_id"]:
            return arr[i]["purchase_id"]
    
    return None

# Set up Kafka consumer
consumer = KafkaConsumer(
    'sqlite_purchases_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Collect messages into a DataFrame
data = []

print("Consuming messages from Kafka...")

for message in consumer:
    purchase = message.value
    print(f"Received: {purchase}")
    
    data.append(purchase)
    
    # analyze every 5 messages
    if len(data) >= 5:
        res = induce_price_surge(data)
        if res is not None:
            print(f"Inducing price surge on {str(res)}")

        # Reset or store for later
        data = []


