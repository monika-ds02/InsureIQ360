import duckdb

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.auth import decode_access_token


router = APIRouter(
    prefix="/risk-analytics",
    tags=["Risk Analytics"]
)


DB_PATH = "dbt_insureiq360/dev.duckdb"



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)



def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return payload




@router.get("/")
def risk_analytics(
    current_user: dict = Depends(get_current_user)
):

    con = duckdb.connect(DB_PATH)


    total_claims = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
    """).fetchone()[0]



    total_amount = con.execute("""
        SELECT SUM(claim_amount)
        FROM fact_claims
    """).fetchone()[0] or 0



    average_claim = con.execute("""
        SELECT AVG(claim_amount)
        FROM fact_claims
    """).fetchone()[0] or 0



    pending_claims = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
        WHERE status='Pending'
    """).fetchone()[0]



    approved_claims = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
        WHERE status='Approved'
    """).fetchone()[0]



    high_value_claims = con.execute("""
        SELECT
            claim_id,
            claim_amount,
            status
        FROM fact_claims
        ORDER BY claim_amount DESC
        LIMIT 5
    """).fetchall()



    con.close()



    return {

        "total_claims": total_claims,

        "total_claim_amount": total_amount,

        "average_claim_amount": round(
            average_claim,
            2
        ),

        "pending_claims": pending_claims,

        "approved_claims": approved_claims,


        "risk_level": "Low",


        "high_value_claims": [
            {
                "claim_id": row[0],
                "amount": row[1],
                "status": row[2]
            }
            for row in high_value_claims
        ]

    }