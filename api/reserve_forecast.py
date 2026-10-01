from fastapi import APIRouter, Depends
import duckdb

from api.main import get_current_user


router = APIRouter(
    prefix="/reserve-forecast",
    tags=["Reserve Forecast"]
)


DB_PATH = "dbt_insureiq360/dev.duckdb"


def get_connection():
    return duckdb.connect(DB_PATH)


@router.get("/")
async def get_reserve_forecast(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        # Get current claims information
        row = con.execute("""
            SELECT
                COUNT(*) AS total_claims,
                COALESCE(SUM(claim_amount), 0) AS total_claim_amount,
                COALESCE(
                    SUM(
                        CASE
                            WHEN LOWER(status) = 'pending'
                            THEN claim_amount
                            ELSE 0
                        END
                    ),
                    0
                ) AS pending_claim_amount
            FROM fact_claims
        """).fetchone()

        total_claims = row[0]
        total_claim_amount = row[1]
        pending_claim_amount = row[2]

        # Simple reserve estimate:
        # pending claim amount is treated as the current reserve exposure.
        forecast_amount = pending_claim_amount

        return [
            {
                "period": "Current",
                "expected_claims": total_claims,
                "forecast_amount": forecast_amount
            }
        ]

    finally:
        con.close()