# Ecommerce_DataEngineering
Pipeline to monitor live customer insights using Kafka , process data using Spark 

Clone the repo using one of the branches, do not use master branch 

After cloning , go to /frontend and do npm i 

Go to /backend and do pip install -r requirements.txt

Try running the app 

npm run dev on one cli in /frontend
  
uvicorn backend.main:app --reload from another cli /backend


Setup Tommy Went Through<br/>
You will need 5 terminal total: 1 in frontend, 4 in backend
Frontend 1<br/>
cd frontend<br/>
npm i<br/>
npm run dev<br/>

Backend 1<br/>
Note: Virtual Environment may not be necesasry but can help streamline package installations
cd backend<br/>
python3 -m venv .venv<br/>
source .venv/bin/activate<br/>
pip3 install -r requirements.txt<br/>
pip3 install "fastapi[standard]"<br/>
uvicorn main:app --reload<br/>
#test2
Backend 2<br/>
https://kafka.apache.org/downloads version 4.0.0 binary move to backend and unzip <br/>
**Run the single following command only once!!!<br/>
bin/kafka-storage.sh format --standalone -t $(uuidgen) -c config/server.properties <br/><br/>
bin/kafka-server-start.sh config/server.properties <br/>

Backend 3<br/>
cd backend<br/>
source .venv/bin/activate<br/>
python3 producer.py<br/>
make purchases on frontend and watch it update in the terminal where producer.py ran<br/>

Backend 3<br/>
cd backend<br/>
source .venv/bin/activate<br/>
python3 consumer.py<br/>
make purchases on frontend and watch it update in the terminal where consumer.py ran this is where price surges are handled<br/>


Currently does not actually utilize the kafka producer, awaiting setup for kafka brokers (zookeeper or KRaft mode)


--------------------------------------------------------


Spark set up -- shoaib 

pip install requirements 


run command 
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 sparkconsumer.py

To run the spark job 




--
