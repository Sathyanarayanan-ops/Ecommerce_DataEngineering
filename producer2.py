from time import sleep
from json import dumps
from kafka import KafkaProducer
import re

def to_dict(line):
    product_type, sku, price, availability, number_sold, revenue_generated, customer_demographics, stock_levels, lead_times, order_quantities, shipping_times, shipping_carriers, shipping_costs, supplier_name, location, lead_time, production_volumes, manufacturing_lead_time, manufacturing_costs, inspection_results, defect_rates, transportation_modes, routes, costs = line.split(",")
    
    if product_type and sku and price and availability and number_sold and revenue_generated and customer_demographics and stock_levels and lead_times and order_quantities and shipping_times and shipping_carriers and shipping_costs and supplier_name and location and lead_time and production_volumes and manufacturing_lead_time and manufacturing_costs and inspection_results and defect_rates and transportation_modes and routes and costs:
        print(product_type, sku, price, availability, number_sold, revenue_generated, customer_demographics, stock_levels, lead_times, order_quantities, shipping_times, shipping_carriers, shipping_costs, supplier_name, location, lead_time, production_volumes, manufacturing_lead_time, manufacturing_costs, inspection_results, defect_rates, transportation_modes, routes, costs)
        data_dict = {
            "product_type": product_type,
            "sku": sku,
            "price": price,
            "availability": availability,
            "number_sold": number_sold,
            "revenue_generated": revenue_generated,
            "customer_demographics": customer_demographics,
            "stock_levels": stock_levels,
            "lead_times": lead_times,
            "order_quantities": order_quantities,
            "shipping_times": shipping_times,
            "shipping_carriers": shipping_carriers,
            "shipping_costs": shipping_costs,
            "supplier_name": supplier_name,
            "location": location,
            "lead_time": lead_time,
            "production_volumes": production_volumes,
            "manufacturing_lead_time": manufacturing_lead_time,
            "manufacturing_costs": manufacturing_costs,
            "inspection_results": inspection_results,
            "defect_rates": defect_rates,
            "transportation_modes": transportation_modes,
            "routes": routes,
            "costs": costs
        }
        
        return data_dict
    else:
        return None

def stream_file_lines(filename, kafka_producer):
    # Open the requested file for reading
    try:
        with open(filename, 'r') as file:
            count = 0 # Count the number of dicts sent to Kafka
            skipped = 0 # Count the number of access log entries skipped and not sent to Kafka
            for line in file:
                if line:
                    
                    data_dict = to_dict(line)
                    if data_dict is None:
                        skipped += 1
                        continue
                    
                    key = data_dict["ip_address"] if data_dict["ip_address"] else "unknown"
                    
                    # Send to Kafka
                    kafka_producer.send("topic_test", key=key, value=data_dict)
                    count += 1
                    
                    print(f"Sent {count} value(s) to topic_test. {skipped} skipped")
                    
                    sleep(1) 
        
            print(f"Finished streaming {count} messages from {filename}")
            
    except FileNotFoundError:
        print(f"File {filename} not found. Please check the path and try again.")

# We have already setup a producer for you
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8'),
    key_serializer=lambda x: x.encode('utf-8')
)

# Top level call to stream the data to kafka topic. Provide the path to the data. Use a smaller data file for testing.
stream_file_lines("archive2/access.log", producer)


# FOR TESTING TO_DICT
# with open("supply_chain_data.csv", "r") as file:
#     for i in range(3):
#         line = file.readline()
#         if line:
#             data_dict = to_dict(line)
#             if data_dict is None:
#                 continue
            
#             sleep(1)