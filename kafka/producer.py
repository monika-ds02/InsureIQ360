from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

claims = [
    {
        "claim_id": "CLM001",
        "customer_id": "CUS001",
        "policy_id": "POL001",
        "claim_amount": 25000,
        "status": "Pending"
    },
    {
        "claim_id": "CLM002",
        "customer_id": "CUS002",
        "policy_id": "POL002",
        "claim_amount": 45000,
        "status": "Approved"
    }
]

for claim in claims:
    producer.send("claims", value=claim)
    print("Sent:", claim)
    time.sleep(2)

producer.flush()
producer.close()