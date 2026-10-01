from kafka import KafkaConsumer
import json
import duckdb
from datetime import datetime

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
CLAIMS_TOPIC = "claims-events"
DB_PATH = "dbt_insureiq360/dev.duckdb"

consumer = KafkaConsumer(
    CLAIMS_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="insureiq360-persistence-consumer",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

con = duckdb.connect(DB_PATH)

print("Kafka consumer started...")
print(f"Listening to topic: {CLAIMS_TOPIC}")

for message in consumer:
    event = message.value

    claim_id = event.get("claim_id")

    existing = con.execute("""
        SELECT COUNT(*)
        FROM kafka_claim_events
        WHERE claim_id = ?
          AND event_type = ?
    """, [
        claim_id,
        event.get("event_type")
    ]).fetchone()[0]

    if existing > 0:
        print(f"Duplicate event skipped: {claim_id}")
        continue

    event_id = int(datetime.now().timestamp() * 1000000)

    con.execute("""
        INSERT INTO kafka_claim_events (
            event_id,
            claim_id,
            event_type,
            customer_id,
            policy_id,
            claim_amount,
            status,
            received_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, [
        event_id,
        claim_id,
        event.get("event_type"),
        event.get("customer_id"),
        event.get("policy_id"),
        event.get("claim_amount"),
        event.get("status")
    ])

    con.commit()

    print(f"Persisted Kafka event: {claim_id}")