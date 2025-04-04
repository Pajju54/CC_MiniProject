from confluent_kafka import Consumer
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Create Kafka consumer configuration
consumer = Consumer({
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),  # Kafka broker address
    'group.id': 'test-group',                                    # Consumer group ID
    'auto.offset.reset': 'earliest'                              # Start from beginning if no offset is committed
})

# Subscribe to the topic specified in environment variable
consumer.subscribe([os.getenv("KAFKA_LOG_TOPIC")])

print("📡 Listening for Kafka messages... (Press CTRL+C to exit)")

try:
    while True:
        # Poll Kafka for new messages
        msg = consumer.poll(1.0)  # Timeout: 1 second

        if msg is None:
            continue  # No message received, loop again

        if msg.error():
            print("❌ Consumer error:", msg.error())
            continue

        # Decode and print message
        print(f"✅ Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("\n🛑 Stopping consumer...")

finally:
    # Ensure graceful shutdown
    consumer.close()
    print("🚪 Consumer connection closed.")
