import duckdb

from fastapi import APIRouter, Depends

from api.main import get_current_user


router = APIRouter(
    prefix="/fraud-detection",
    tags=["Fraud Detection"]
)


DB_PATH = "dbt_insureiq360/dev.duckdb"


@router.get("/")
def fraud_detection(
    current_user: dict = Depends(get_current_user)
):

    con = duckdb.connect(DB_PATH)


    total_claims = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
    """).fetchone()[0]


    high_value_claims = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
        WHERE claim_amount >= 40000
    """).fetchone()[0]


    duplicate_claims = con.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT claim_id
            FROM fact_claims
            GROUP BY claim_id
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]


    invalid_customers = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims c
        LEFT JOIN customers cu
        ON c.customer_id = cu.customer_code
        WHERE cu.customer_code IS NULL
    """).fetchone()[0]


    invalid_policies = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims c
        LEFT JOIN policies p
        ON c.policy_id = p.policy_id
        WHERE p.policy_id IS NULL
    """).fetchone()[0]


    fraud_score = 0


    if duplicate_claims > 0:
        fraud_score += 40

    if high_value_claims > 3:
        fraud_score += 20

    if invalid_customers > 0:
        fraud_score += 20

    if invalid_policies > 0:
        fraud_score += 20



    if fraud_score >= 70:
        risk_level = "High"

    elif fraud_score >= 40:
        risk_level = "Medium"

    else:
        risk_level = "Low"



    reasons = []


    if duplicate_claims == 0:
        reasons.append("No duplicate claims detected")
    else:
        reasons.append("Duplicate claims detected")


    if invalid_customers == 0:
        reasons.append("All customers validated")


    if invalid_policies == 0:
        reasons.append("All policies validated")



    con.close()


    return {
        "total_claims": total_claims,
        "fraud_score": fraud_score,
        "risk_level": risk_level,
        "high_value_claims": high_value_claims,
        "duplicate_claims": duplicate_claims,
        "invalid_customers": invalid_customers,
        "invalid_policies": invalid_policies,
        "reasons": reasons
    }