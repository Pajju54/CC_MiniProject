# test_producer.py
from kafka.kafka_producer import send_log_to_kafka
import time

import os

print("Kafka Server:", os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
print("Kafka Topic:", os.getenv("KAFKA_LOG_TOPIC"))

log = {
    "level": "INFO",
    "message": "This is a test log from Prajwal 🚀",
    "timestamp": "2025-04-04T16:00:00"
}

send_log_to_kafka(log)
print("Log sent (hopefully 🤞)...")
