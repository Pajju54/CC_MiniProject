# kafka_producer.py
from confluent_kafka import Producer
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_LOG_TOPIC = os.getenv("KAFKA_LOG_TOPIC", "api-logs")

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_log_to_kafka(log_data: dict):
    try:
        producer.produce(
            topic=KAFKA_LOG_TOPIC,
            value=json.dumps(log_data).encode("utf-8"),
            callback=delivery_report
        )
        producer.poll(0)
        producer.flush()
        time.sleep(1)  
    except Exception as e:
        print(f"Error sending log to Kafka: {str(e)}")
