# Ecommerce_DataEngineering
Pipeline to monitor live customer insights using Kafka , process data using Spark 

Clone the repo using one of the branches, do not use master branch 

After cloning , go to /frontend and do npm i 

Go to /backend and do pip install -r requirements.txt

Try running the app 

npm run dev on one cli in /frontend
  
uvicorn backend.main:app --reload from another cli /backend


Setup Tommy Went Through<br/>
cd backend<br/>
python3 -m venv .venv<br/>
source .venv/bin/activate<br/>
pip3 install -r requirements.txt<br/>
pip3 install "fastapi[standard]"<br/>
cd ../frontend<br/>
npm i<br/>
npm run dev<br/>
new terminal<br/>
cd backend<br/>
source .venv/bin/activate<br/>
uvicorn main:app --reload<br/>
new terminal<br/>
cd backend<br/>
source .venv/bin/activate<br/>
python3 producer.py<br/>
make purchases on frontend and watch it update in the terminal where producer.py ran<br/>
Currently does not actually utilize the kafka producer, awaiting setup for kafka brokers (zookeeper or KRaft mode)

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
