from kafka import KafkaProducer
import json
import os


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_SECURITY_PROTOCOL = os.getenv(
    "KAFKA_SECURITY_PROTOCOL"
)

KAFKA_SASL_MECHANISM = os.getenv(
    "KAFKA_SASL_MECHANISM"
)

KAFKA_SASL_USERNAME = os.getenv(
    "KAFKA_SASL_USERNAME"
)

KAFKA_SASL_PASSWORD = os.getenv(
    "KAFKA_SASL_PASSWORD"
)

KAFKA_SSL_CAFILE = os.getenv(
    "KAFKA_SSL_CAFILE"
)


producer_config = {
    "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
    "value_serializer": lambda value: json.dumps(value).encode("utf-8"),
}


if KAFKA_SECURITY_PROTOCOL:
    producer_config["security_protocol"] = KAFKA_SECURITY_PROTOCOL

if KAFKA_SASL_MECHANISM:
    producer_config["sasl_mechanism"] = KAFKA_SASL_MECHANISM

if KAFKA_SASL_USERNAME:
    producer_config["sasl_plain_username"] = KAFKA_SASL_USERNAME

if KAFKA_SASL_PASSWORD:
    producer_config["sasl_plain_password"] = KAFKA_SASL_PASSWORD

if KAFKA_SSL_CAFILE:
    producer_config["ssl_cafile"] = KAFKA_SSL_CAFILE


producer = KafkaProducer(**producer_config)


def publish_claim_event(event):
    producer.send("claims-events", event)
    producer.flush()