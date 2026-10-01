from fastapi import APIRouter, Depends
import duckdb

from api.main import get_current_user

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

DB_PATH = "dbt_insureiq360/dev.duckdb"


def get_connection():
    return duckdb.connect(DB_PATH)


@router.get("/")
async def get_kafka_events(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                event_id,
                claim_id,
                event_type,
                customer_id,
                policy_id,
                claim_amount,
                status,
                received_at
            FROM kafka_claim_events
            ORDER BY received_at DESC
        """).fetchall()

        return [
            {
                "event_id": row[0],
                "claim_id": row[1],
                "event_type": row[2],
                "customer_id": row[3],
                "policy_id": row[4],
                "claim_amount": row[5],
                "status": row[6],
                "received_at": row[7]
            }
            for row in rows
        ]

    finally:
        con.close()