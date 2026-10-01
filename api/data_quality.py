import duckdb

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordBearer

from api.auth import decode_access_token


router = APIRouter(
    prefix="/data-quality",
    tags=["Data Quality"]
)


DB_PATH = "dbt_insureiq360/dev.duckdb"


# =========================================================
# AUTH
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return payload



# =========================================================
# DATA QUALITY API
# =========================================================

@router.get("/")
def data_quality(
    current_user: dict = Depends(get_current_user)
):

    con = duckdb.connect(DB_PATH)


    total_claims = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
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


    missing_customer_ids = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
        WHERE customer_id IS NULL
        OR TRIM(customer_id) = ''
    """).fetchone()[0]


    missing_policy_ids = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
        WHERE policy_id IS NULL
        OR TRIM(policy_id) = ''
    """).fetchone()[0]


    invalid_amounts = con.execute("""
        SELECT COUNT(*)
        FROM fact_claims
        WHERE claim_amount IS NULL
        OR claim_amount < 0
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


    statuses = con.execute("""
        SELECT DISTINCT status
        FROM fact_claims
        ORDER BY status
    """).fetchall()



    # =====================================================
    # QUALITY SCORE
    # =====================================================

    total_checks = 5

    failed_checks = 0


    if duplicate_claims > 0:
        failed_checks += 1


    if missing_customer_ids > 0:
        failed_checks += 1


    if missing_policy_ids > 0:
        failed_checks += 1


    if invalid_amounts > 0:
        failed_checks += 1


    if invalid_customers > 0 or invalid_policies > 0:
        failed_checks += 1



    passed_checks = total_checks - failed_checks


    quality_score = round(
        (passed_checks / total_checks) * 100,
        2
    )


    con.close()



    return {

        "total_claims": total_claims,

        "duplicate_claims": duplicate_claims,

        "missing_customer_ids": missing_customer_ids,

        "missing_policy_ids": missing_policy_ids,

        "invalid_amounts": invalid_amounts,

        "invalid_customers": invalid_customers,

        "invalid_policies": invalid_policies,


        "quality_score": quality_score,

        "total_checks": total_checks,

        "passed_checks": passed_checks,

        "failed_checks": failed_checks,


        "statuses": [
            row[0]
            for row in statuses
        ]
    }