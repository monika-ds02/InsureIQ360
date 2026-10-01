from kafka import KafkaConsumer
import json
import sqlite3

DB_PATH = r"..\data\bronze\insureIQ360_bronze.db"

consumer = KafkaConsumer(
    "claims",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="insureiq360-db-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Kafka Consumer started...")
print("Waiting for claim messages...")

for message in consumer:
    claim = message.value

    print("Received:", claim)

    cursor.execute("""
        INSERT OR REPLACE INTO bronze_claims
        (claim_id, customer_id, policy_id, claim_amount, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        claim["claim_id"],
        claim["customer_id"],
        claim["policy_id"],
        claim["claim_amount"],
        claim["status"]
    ))

    conn.commit()

    print("Saved to Bronze:", claim["claim_id"])