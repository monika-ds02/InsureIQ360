from kafka import KafkaProducer
import json
import os


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

CLAIMS_TOPIC = "claims-events"


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)


def publish_claim_event(event):
    producer.send(CLAIMS_TOPIC, event)
    producer.flush()