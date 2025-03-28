# Ecommerce_DataEngineering
Pipeline to monitor live customer insights using Kafka , process data using Spark 



Phase 1 :

Setup Kafka to stream continuous live data , using data set or live traffic from website
Verify data flow from kafka 
EDA using data from Kafka
Set up live log for traffic activity - TBD 

Phase 2 :
Set up spark streaming to process live data from Kafka 
Build pipeline to get insights from live data
Build core logic behind pipeline - Identify demand in product , set up threshold for product , set up threshold for price surge 
Implement price surge - Use scheduler to send notifications regarding price surge , set up cool down time for price surge (manually)

Phase 3 :
Store data regarding price surge and general data for historical analysis
Testing with live data 

Phase 4:
Identify scope for ML implementation 

--
