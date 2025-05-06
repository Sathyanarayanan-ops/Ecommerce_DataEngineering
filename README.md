Here’s a polished and structured `README.md` for your `Ecommerce_DataEngineering` project that clearly explains setup, usage, and context:

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

