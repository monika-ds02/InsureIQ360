from kafka import KafkaProducer
import json
import os
import socket

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_SECURITY_PROTOCOL = os.getenv("KAFKA_SECURITY_PROTOCOL")
KAFKA_SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM")
KAFKA_SASL_USERNAME = os.getenv("KAFKA_SASL_USERNAME")
KAFKA_SASL_PASSWORD = os.getenv("KAFKA_SASL_PASSWORD")
KAFKA_SSL_CAFILE = os.getenv("KAFKA_SSL_CAFILE")

print("=== KAFKA DIAGNOSTIC START ===")
print(f"Kafka server: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"Security protocol: {KAFKA_SECURITY_PROTOCOL}")
print(f"SASL mechanism: {KAFKA_SASL_MECHANISM}")
print(f"SASL username: {KAFKA_SASL_USERNAME}")
print(f"SSL CA file: {KAFKA_SSL_CAFILE}")

try:
    kafka_host, kafka_port = KAFKA_BOOTSTRAP_SERVERS.rsplit(":", 1)
    kafka_port = int(kafka_port)

    addresses = socket.getaddrinfo(
        kafka_host,
        kafka_port,
        type=socket.SOCK_STREAM
    )

    print(f"DNS resolved addresses: {addresses}")

    sock = socket.create_connection(
        (kafka_host, kafka_port),
        timeout=10
    )

    print("TCP connection to Kafka succeeded.")
    sock.close()

except Exception as e:
    print(f"TCP/DNS connection test FAILED: {type(e).__name__}: {e}")

print("=== KAFKA DIAGNOSTIC END ===")

producer_config = {
    "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
    "value_serializer": lambda value: json.dumps(value).encode("utf-8"),
    "request_timeout_ms": 10000,
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

producer = None

try:
    producer = KafkaProducer(**producer_config)
    print("Kafka producer connected successfully.")
except Exception as e:
    print(f"Kafka producer unavailable: {type(e).__name__}: {e}")


def publish_claim_event(event):
    if producer is None:
        print("Kafka unavailable. Event not published.")
        return

    producer.send("claims-events", value=event)
    producer.flush()