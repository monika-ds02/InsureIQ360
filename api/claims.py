from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import duckdb

from api.kafka_producer import publish_claim_event
from api.main import get_current_user


router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)


DB_PATH = "dbt_insureiq360/dev.duckdb"


class ClaimCreate(BaseModel):
    claim_id: str
    customer_id: str
    policy_id: str
    claim_amount: float
    status: str


class Claim(ClaimCreate):
    pass


def get_connection():
    return duckdb.connect(DB_PATH)


# =========================
# GET ALL CLAIMS
# =========================

@router.get("/", response_model=List[Claim])
async def get_claims(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                claim_id,
                customer_id,
                policy_id,
                claim_amount,
                status
            FROM fact_claims
            ORDER BY claim_id
        """).fetchall()

        return [
            Claim(
                claim_id=row[0],
                customer_id=row[1],
                policy_id=row[2],
                claim_amount=row[3],
                status=row[4]
            )
            for row in rows
        ]

    finally:
        con.close()


# =========================
# CLAIMS SUMMARY
# =========================

@router.get("/summary")
async def get_claims_summary(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        total_claims = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
        """).fetchone()[0]

        pending_claims = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
            WHERE LOWER(status) = 'pending'
        """).fetchone()[0]

        approved_claims = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
            WHERE LOWER(status) = 'approved'
        """).fetchone()[0]

        total_claim_amount = con.execute("""
            SELECT COALESCE(SUM(claim_amount), 0)
            FROM fact_claims
        """).fetchone()[0]

        return {
            "total_claims": total_claims,
            "pending_claims": pending_claims,
            "approved_claims": approved_claims,
            "total_claim_amount": total_claim_amount
        }

    finally:
        con.close()


# =========================
# KPI - CLAIM FREQUENCY
# =========================

@router.get("/kpi/claim-frequency")
async def claim_frequency(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        result = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
        """).fetchone()

        return {
            "claim_frequency": result[0]
        }

    finally:
        con.close()


# =========================
# KPI - CLAIM SEVERITY
# =========================

@router.get("/kpi/claim-severity")
async def claim_severity(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        result = con.execute("""
            SELECT
                COALESCE(AVG(claim_amount), 0)
            FROM fact_claims
        """).fetchone()

        return {
            "claim_severity": round(result[0], 2)
        }

    finally:
        con.close()


# =========================
# CLAIMS SUMMARY BY CUSTOMER
# =========================

@router.get("/summary/customer")
async def get_customer_claim_summary(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                customer_id,
                COUNT(*) AS claim_count,
                COALESCE(SUM(claim_amount), 0) AS total_claim_amount
            FROM fact_claims
            GROUP BY customer_id
            ORDER BY customer_id
        """).fetchall()

        return [
            {
                "customer_id": row[0],
                "claim_count": row[1],
                "total_claim_amount": row[2]
            }
            for row in rows
        ]

    finally:
        con.close()


# =========================
# CLAIMS SUMMARY BY POLICY
# =========================

@router.get("/summary/policy")
async def get_policy_claim_summary(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                policy_id,
                COUNT(*) AS claim_count,
                COALESCE(SUM(claim_amount), 0) AS total_claim_amount
            FROM fact_claims
            GROUP BY policy_id
            ORDER BY policy_id
        """).fetchall()

        return [
            {
                "policy_id": row[0],
                "claim_count": row[1],
                "total_claim_amount": row[2]
            }
            for row in rows
        ]

    finally:
        con.close()


# =========================
# CLAIMS DASHBOARD
# =========================

@router.get("/dashboard")
async def get_claims_dashboard(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        summary = con.execute("""
            SELECT
                COUNT(*) AS total_claims,
                SUM(
                    CASE
                        WHEN LOWER(status) = 'pending' THEN 1
                        ELSE 0
                    END
                ) AS pending_claims,
                SUM(
                    CASE
                        WHEN LOWER(status) = 'approved' THEN 1
                        ELSE 0
                    END
                ) AS approved_claims,
                COALESCE(SUM(claim_amount), 0) AS total_claim_amount
            FROM fact_claims
        """).fetchone()

        customer_rows = con.execute("""
            SELECT
                customer_id,
                COUNT(*) AS claim_count,
                COALESCE(SUM(claim_amount), 0) AS total_claim_amount
            FROM fact_claims
            GROUP BY customer_id
            ORDER BY customer_id
        """).fetchall()

        policy_rows = con.execute("""
            SELECT
                policy_id,
                COUNT(*) AS claim_count,
                COALESCE(SUM(claim_amount), 0) AS total_claim_amount
            FROM fact_claims
            GROUP BY policy_id
            ORDER BY policy_id
        """).fetchall()

        return {
            "summary": {
                "total_claims": summary[0],
                "pending_claims": summary[1] or 0,
                "approved_claims": summary[2] or 0,
                "total_claim_amount": summary[3]
            },
            "customer_summary": [
                {
                    "customer_id": row[0],
                    "claim_count": row[1],
                    "total_claim_amount": row[2]
                }
                for row in customer_rows
            ],
            "policy_summary": [
                {
                    "policy_id": row[0],
                    "claim_count": row[1],
                    "total_claim_amount": row[2]
                }
                for row in policy_rows
            ]
        }

    finally:
        con.close()


# =========================
# GET CLAIM BY ID
# =========================

@router.get("/{claim_id}", response_model=Claim)
async def get_claim(
    claim_id: str,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        row = con.execute("""
            SELECT
                claim_id,
                customer_id,
                policy_id,
                claim_amount,
                status
            FROM fact_claims
            WHERE claim_id = ?
        """, [claim_id]).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Claim not found"
            )

        return Claim(
            claim_id=row[0],
            customer_id=row[1],
            policy_id=row[2],
            claim_amount=row[3],
            status=row[4]
        )

    finally:
        con.close()


# =========================
# CREATE CLAIM
# =========================

@router.post("/", response_model=Claim)
async def create_claim(
    claim: ClaimCreate,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT claim_id
            FROM fact_claims
            WHERE claim_id = ?
        """, [claim.claim_id]).fetchone()

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Claim ID already exists"
            )

        result = con.execute("""
            INSERT INTO fact_claims (
                claim_id,
                customer_id,
                policy_id,
                claim_amount,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            RETURNING
                claim_id,
                customer_id,
                policy_id,
                claim_amount,
                status
        """, [
            claim.claim_id,
            claim.customer_id,
            claim.policy_id,
            claim.claim_amount,
            claim.status
        ]).fetchone()

        created_claim = Claim(
            claim_id=result[0],
            customer_id=result[1],
            policy_id=result[2],
            claim_amount=result[3],
            status=result[4]
        )

        # Publish claim-created event to Kafka
        publish_claim_event({
            "claim_id": created_claim.claim_id,
            "customer_id": created_claim.customer_id,
            "policy_id": created_claim.policy_id,
            "claim_amount": created_claim.claim_amount,
            "status": created_claim.status,
            "event_type": "claim_created"
        })

        return created_claim

    finally:
        con.close()


# =========================
# UPDATE CLAIM
# =========================

@router.put("/{claim_id}", response_model=Claim)
async def update_claim(
    claim_id: str,
    claim: ClaimCreate,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT claim_id
            FROM fact_claims
            WHERE claim_id = ?
        """, [claim_id]).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Claim not found"
            )

        result = con.execute("""
            UPDATE fact_claims
            SET
                customer_id = ?,
                policy_id = ?,
                claim_amount = ?,
                status = ?
            WHERE claim_id = ?
            RETURNING
                claim_id,
                customer_id,
                policy_id,
                claim_amount,
                status
        """, [
            claim.customer_id,
            claim.policy_id,
            claim.claim_amount,
            claim.status,
            claim_id
        ]).fetchone()

        return Claim(
            claim_id=result[0],
            customer_id=result[1],
            policy_id=result[2],
            claim_amount=result[3],
            status=result[4]
        )

    finally:
        con.close()


# =========================
# DELETE CLAIM
# =========================

@router.delete("/{claim_id}")
async def delete_claim(
    claim_id: str,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT claim_id
            FROM fact_claims
            WHERE claim_id = ?
        """, [claim_id]).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Claim not found"
            )

        con.execute("""
            DELETE FROM fact_claims
            WHERE claim_id = ?
        """, [claim_id])

        return {
            "message": "Claim deleted successfully",
            "claim_id": claim_id
        }

    finally:
        con.close()