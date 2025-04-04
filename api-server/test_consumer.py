from confluent_kafka import Consumer
import os
from dotenv import load_dotenv
import time

load_dotenv()

consumer = Consumer({
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([os.getenv("KAFKA_LOG_TOPIC")])

print("Listening for messages... (CTRL+C to exit)")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue
        print(f"Received: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
