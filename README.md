---

# 🛒 Ecommerce Data Engineering Pipeline

Real-time customer insights pipeline using **Kafka**, **Apache Spark**, **FastAPI**, and **React**. This project demonstrates a full-stack streaming architecture where user purchase behavior on the frontend triggers backend processing, updates a SQLite database, and adjusts product pricing dynamically.

---

## 📦 Features

* ⚡ Live data ingestion using **Kafka**
* 🔄 Real-time data processing via **Apache Spark**
* 🔥 Dynamic surge pricing based on demand
* 🧾 FastAPI backend with SQLite storage
* 🛍️ React-based frontend for product interaction
* 🧪 Pluggable with consumer-producer model for streaming

---

## 🚀 Quickstart Guide

### ⚠️ Use Only Feature Branches

> **Do NOT use the `master` branch.** Clone one of the feature branches to get started.

```bash
git clone -b <feature-branch-name> https://github.com/Sathyanarayanan-ops/Ecommerce_DataEngineering.git
cd Ecommerce_DataEngineering
```

---

## 🖥️ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:3000`

---

## 🧠 Backend Setup

### Terminal 1: FastAPI App

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Runs on `http://localhost:8000`

---

## 🔄 Kafka Setup (KRaft mode - no Zookeeper)

### Terminal 2: Kafka Server

1. Download Kafka 4.0.0 and move it into the `backend/` folder.
2. Unzip it.

```bash
cd backend/kafka_2.13-4.0.0
# Run this only once
bin/kafka-storage.sh format --standalone -t $(uuidgen) -c config/server.properties
# Start Kafka server
bin/kafka-server-start.sh config/server.properties
```

---

## 🧾 Data Stream Processing

### Terminal 3: Kafka Producer

```bash
cd backend
source .venv/bin/activate
python3 producer.py
```

### Terminal 4: Kafka Consumer (handles surge pricing)

```bash
cd backend
source .venv/bin/activate
python3 consumer.py
```

Make purchases on the frontend and observe events logged by producer and consumer.

---

## 🔥 Spark Integration

### Spark Setup by Shoaib

```bash
pip install -r requirements.txt
```

### Terminal 5: Spark Job (for streaming and surge logic)

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 sparkconsumer.py
```

---

## 📈 Architecture Overview

```plaintext
[Frontend - React]
       ↓ (purchase event)
[FastAPI Backend] ──> [Kafka Producer]
                            ↓
                     [Kafka Broker]
                            ↓
               [Kafka Consumer] → Updates SQLite with surge prices
                            ↓
               [Spark Job] → Real-time stream analytics
```

---

```
+--------------------+       +--------------------+       +--------------------+
|                    |       |                    |       |                    |
|    React Frontend  |       |    FastAPI Backend |       |   Kafka Producer   |
|  (User Interactions) | --> |  (API & SQLite DB) | --> |  (Publishes Events) |
|                    |       |                    |       |                    |
+--------------------+       +--------------------+       +--------------------+
                                                              |
                                                              v
                                                     +--------------------+
                                                     |                    |
                                                     |   Kafka Broker     |
                                                     |  (KRaft Mode)      |
                                                     |                    |
                                                     +--------------------+
                                                              |
                                                              v
+--------------------+       +--------------------+       +--------------------+
|                    |       |                    |       |                    |
| Kafka Consumer     |       |   Spark Streaming  |       |   SQLite Database  |
| (Surge Pricing Logic) | --> |  (Real-time Analytics) | --> |  (Updated Prices)  |
|                    |       |                    |       |                    |
+--------------------+       +--------------------+       +--------------------+
                                                              |
                                                              v
                                                     +--------------------+
                                                     |                    |
                                                     | React Frontend     |
                                                     | (Updated UI)       |
                                                     |                    |
                                                     +--------------------+

```


Some demo pictures 

<img width="780" alt="Screenshot 2025-05-07 at 7 28 30 PM" src="https://github.com/user-attachments/assets/6bf06938-9729-482c-8c17-90505893ada2" />


Kafka sending data from DB to spark
<img width="681" alt="Screenshot 2025-05-07 at 7 28 52 PM" src="https://github.com/user-attachments/assets/6f1ddd4a-cced-412a-9fda-c874573005bd" />


Spark data Processing 


<img width="780" alt="Screenshot 2025-05-07 at 7 28 30 PM" src="https://github.com/user-attachments/assets/b1287969-3183-4715-9e84-7d22d1956d0d" />


Surge detection and price hike 

<img width="386" alt="Screenshot 2025-05-07 at 7 33 26 PM" src="https://github.com/user-attachments/assets/58f8795e-0fa8-42c8-93c7-c8d2e7ab623b" />


Sqlite table before and after price hike 


<img width="398" alt="Screenshot 2025-05-07 at 7 33 32 PM" src="https://github.com/user-attachments/assets/fdad9a55-82dd-4593-971f-9e81741a273d" />








