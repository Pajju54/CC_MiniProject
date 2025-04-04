# test_producer.py
# This script sends multiple test log messages to Kafka using our custom producer

from kafka.kafka_producer import send_log_to_kafka
import os
import time

# Print Kafka configuration for verification
print("🔌 Kafka Server:", os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
print("📦 Kafka Topic:", os.getenv("KAFKA_LOG_TOPIC"))

# Define multiple test log messages
test_logs = [
    {
        "level": "INFO",
        "message": "Prajwal's app booted up successfully 🚀",
        "timestamp": "2025-04-04T16:00:00"
    },
    {
        "level": "DEBUG",
        "message": "Debugging middleware behavior... 🔍",
        "timestamp": "2025-04-04T16:01:00"
    },
    {
        "level": "WARNING",
        "message": "High memory usage detected ⚠️",
        "timestamp": "2025-04-04T16:02:00"
    },
    {
        "level": "ERROR",
        "message": "Unable to connect to the database ❌",
        "timestamp": "2025-04-04T16:03:00"
    },
    {
        "level": "CRITICAL",
        "message": "System crash imminent! 💥",
        "timestamp": "2025-04-04T16:04:00"
    }
]

# Send each log entry with a slight delay
for idx, log in enumerate(test_logs):
    print(f"\n📤 Sending test log #{idx + 1}: {log['level']}")
    send_log_to_kafka(log)
    time.sleep(1)  # Simulate time gap between logs

print("\n✅ All test logs sent (fingers crossed 🤞)")
