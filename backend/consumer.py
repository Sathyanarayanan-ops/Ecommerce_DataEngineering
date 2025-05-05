# from kafka import KafkaConsumer
# import json

# def induce_price_surge(arr):
#     """
#     Check if there are 3 consecutive identical numbers in the array.
#     """
#     if len(arr) < 3:
#         return None
    
#     # Scan the array looking for 3 consecutive identical numbers
#     for i in range(len(arr) - 2):
#         if arr[i]["purchase_id"] == arr[i+1]["purchase_id"] == arr[i+2]["purchase_id"]:
#             return arr[i]["purchase_id"]
    
#     return None

# # Set up Kafka consumer
# consumer = KafkaConsumer(
#     'sqlite_purchases_topic',
#     bootstrap_servers='localhost:9092',
#     auto_offset_reset='earliest',
#     value_deserializer=lambda v: json.loads(v.decode('utf-8'))
# )

# # Collect messages into a DataFrame
# data = []

# print("Consuming messages from Kafka...")

# for message in consumer:
#     purchase = message.value
#     print(f"Received: {purchase}")
    
#     data.append(purchase)
    
#     # analyze every 5 messages
#     if len(data) >= 5:
#         res = induce_price_surge(data)
#         if res is not None:
#             print(f"Inducing price surge on {str(res)}")

#         # Reset or store for later
#         data = []


# from datetime import datetime
# from pyflink.common.serialization import SimpleStringSchema
# from pyflink.datastream import StreamExecutionEnvironment
# from pyflink.datastream.connectors import KafkaSource
# from pyflink.common import Types, WatermarkStrategy
# import json
 
# def create_source():
#     kafka_source = KafkaSource \
#         .builder() \
#         .set_bootstrap_servers('localhost:9092') \
#         .set_group_id('flink-consumer-group') \
#         .set_topics('sqlite_purchases_topic') \
#         .set_value_only_deserializer(SimpleStringSchema()) \
#         .build()
    
#     return kafka_source
 
# def process_data(value):
#     """
#     Process the incoming message and implement surge logic if needed.
#     """
#     data = json.loads(value)
    
#     # Implement your surge logic here (price surge, etc.)
#     return json.dumps(data)
 
# def main():
#     # Set up the Flink execution environment
#     env = StreamExecutionEnvironment.get_execution_environment()
 
#     # env.add_jars("file:///Users/shoaib/Documents/School_VSCode/Big_Data_Engineering/Ecommerce_DataEngineering/backend/flink-2.0.0/lib/flink-connector-kafka-4.0.0-2.0.jar")
#     # env.add_jars("file:///Users/shoaib/Documents/School_VSCode/Big_Data_Engineering/Ecommerce_DataEngineering/backend/flink-2.0.0/lib/kafka-clients-4.0.0.jar")
    
    
#     # Define Kafka source
#     source = create_source()
 
#     # Add the Kafka source to the Flink data stream
#     stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
 
 
#     # Apply transformation to process data
#     processed_stream = stream.map(lambda value: process_data(value), output_type=Types.STRING())
 
#     # Print the processed data to console (or sink to another Kafka topic if needed)
#     processed_stream.print()
 
#     # Execute the Flink job
#     env.execute('Flink Kafka Source Consumer')
 
# if __name__ == '__main__':
#     main()


from pyflink.common import Types, WatermarkStrategy, Configuration
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import KafkaSource
from pyflink.common.serialization import SimpleStringSchema
import json
from datetime import datetime

def create_source():
    return KafkaSource \
        .builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_topics('sqlite_purchases_topic') \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .set_properties({
            'group.id': 'flink-consumer-group',
            'auto.offset.reset': 'earliest'
        }) \
        .build()

def process_data(value):
    try:
        data = json.loads(value)
        # Example processing: Add processing timestamp
        data['flink_processed_at'] = datetime.now().isoformat()
        return data
    except json.JSONDecodeError as e:
        return {'error': str(e), 'raw_value': value}

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # REQUIRED: Add Kafka connector JAR
    env.add_jars(
        "file:///path/to/flink-sql-connector-kafka-3.1.0-1.18.jar"
    )

    source = create_source()
    
    # Define explicit return type
    output_type = Types.MAP(Types.STRING(), Types.STRING())

    stream = env.from_source(
        source,
        WatermarkStrategy.for_monotonous_timestamps(),
        "Kafka Source"
    )

    processed_stream = stream \
        .map(lambda value: process_data(value), output_type=output_type)

    # Add sink instead of just printing
    processed_stream.print()

    env.execute('Ecommerce Purchase Processing')

if __name__ == '__main__':
    main()