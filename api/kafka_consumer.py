from kafka import KafkaConsumer
import json
import duckdb
from datetime import datetime
import os


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_SECURITY_PROTOCOL = os.getenv("KAFKA_SECURITY_PROTOCOL")
KAFKA_SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM")
KAFKA_SASL_USERNAME = os.getenv("KAFKA_SASL_USERNAME")
KAFKA_SASL_PASSWORD = os.getenv("KAFKA_SASL_PASSWORD")
KAFKA_SSL_CAFILE = os.getenv("KAFKA_SSL_CAFILE")

CLAIMS_TOPIC = "claims-events"
DB_PATH = "dbt_insureiq360/dev.duckdb"


def run_consumer():
    consumer_config = {
        "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
        "auto_offset_reset": "earliest",
        "enable_auto_commit": True,
        "group_id": "insureiq360-persistence-consumer",
        "value_deserializer": lambda value: json.loads(
            value.decode("utf-8")
        ),
    }

    if KAFKA_SECURITY_PROTOCOL:
        consumer_config["security_protocol"] = KAFKA_SECURITY_PROTOCOL

    if KAFKA_SASL_MECHANISM:
        consumer_config["sasl_mechanism"] = KAFKA_SASL_MECHANISM

    if KAFKA_SASL_USERNAME:
        consumer_config["sasl_plain_username"] = KAFKA_SASL_USERNAME

    if KAFKA_SASL_PASSWORD:
        consumer_config["sasl_plain_password"] = KAFKA_SASL_PASSWORD

    if KAFKA_SSL_CAFILE:
        consumer_config["ssl_cafile"] = KAFKA_SSL_CAFILE

    consumer = KafkaConsumer(
        CLAIMS_TOPIC,
        **consumer_config
    )

    con = duckdb.connect(DB_PATH)

    print("Kafka consumer started...")
    print(f"Kafka server: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"Listening to topic: {CLAIMS_TOPIC}")

    for message in consumer:
        event = message.value

        claim_id = event.get("claim_id")
        event_type = event.get("event_type")

        existing = con.execute("""
            SELECT COUNT(*)
            FROM kafka_claim_events
            WHERE claim_id = ?
              AND event_type = ?
        """, [
            claim_id,
            event_type
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
            event_type,
            event.get("customer_id"),
            event.get("policy_id"),
            event.get("claim_amount"),
            event.get("status")
        ])

        con.commit()

        print(f"Persisted Kafka event: {claim_id}")