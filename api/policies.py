from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import duckdb

from api.main import get_current_user

router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)

DB_PATH = "dbt_insureiq360/dev.duckdb"


class PolicyCreate(BaseModel):
    policy_id: str
    customer_id: str
    policy_type: str
    premium: float
    status: str


class Policy(PolicyCreate):
    pass


def get_connection():
    return duckdb.connect(DB_PATH)


# =========================
# GET ALL POLICIES
# =========================
@router.get("/", response_model=List[Policy])
async def get_policies(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                policy_id,
                customer_id,
                policy_type,
                premium,
                status
            FROM policies
            ORDER BY policy_id
        """).fetchall()

        return [
            Policy(
                policy_id=row[0],
                customer_id=row[1],
                policy_type=row[2],
                premium=row[3],
                status=row[4]
            )
            for row in rows
        ]

    finally:
        con.close()


# =========================
# POLICY SUMMARY
# =========================
@router.get("/summary")
async def get_policy_summary(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        total_policies = con.execute("""
            SELECT COUNT(*)
            FROM policies
        """).fetchone()[0]

        active_policies = con.execute("""
            SELECT COUNT(*)
            FROM policies
            WHERE LOWER(status) = 'active'
        """).fetchone()[0]

        inactive_policies = con.execute("""
            SELECT COUNT(*)
            FROM policies
            WHERE LOWER(status) = 'inactive'
        """).fetchone()[0]

        total_premium = con.execute("""
            SELECT COALESCE(SUM(premium), 0)
            FROM policies
        """).fetchone()[0]

        return {
            "total_policies": total_policies,
            "active_policies": active_policies,
            "inactive_policies": inactive_policies,
            "total_premium": total_premium
        }

    finally:
        con.close()


# =========================
# GET POLICY BY ID
# =========================
@router.get("/{policy_id}", response_model=Policy)
async def get_policy(
    policy_id: str,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        row = con.execute("""
            SELECT
                policy_id,
                customer_id,
                policy_type,
                premium,
                status
            FROM policies
            WHERE policy_id = ?
        """, [policy_id]).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Policy not found"
            )

        return Policy(
            policy_id=row[0],
            customer_id=row[1],
            policy_type=row[2],
            premium=row[3],
            status=row[4]
        )

    finally:
        con.close()


# =========================
# CREATE POLICY
# =========================
@router.post("/", response_model=Policy)
async def create_policy(
    policy: PolicyCreate,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT policy_id
            FROM policies
            WHERE policy_id = ?
        """, [policy.policy_id]).fetchone()

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Policy ID already exists"
            )

        con.execute("""
            INSERT INTO policies (
                policy_id,
                customer_id,
                policy_type,
                premium,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, [
            policy.policy_id,
            policy.customer_id,
            policy.policy_type,
            policy.premium,
            policy.status
        ])

        return policy

    finally:
        con.close()


# =========================
# UPDATE POLICY
# =========================
@router.put("/{policy_id}", response_model=Policy)
async def update_policy(
    policy_id: str,
    policy: PolicyCreate,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT policy_id
            FROM policies
            WHERE policy_id = ?
        """, [policy_id]).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Policy not found"
            )

        con.execute("""
            UPDATE policies
            SET
                customer_id = ?,
                policy_type = ?,
                premium = ?,
                status = ?
            WHERE policy_id = ?
        """, [
            policy.customer_id,
            policy.policy_type,
            policy.premium,
            policy.status,
            policy_id
        ])

        row = con.execute("""
            SELECT
                policy_id,
                customer_id,
                policy_type,
                premium,
                status
            FROM policies
            WHERE policy_id = ?
        """, [policy_id]).fetchone()

        return Policy(
            policy_id=row[0],
            customer_id=row[1],
            policy_type=row[2],
            premium=row[3],
            status=row[4]
        )

    finally:
        con.close()


# =========================
# DELETE POLICY
# =========================
@router.delete("/{policy_id}")
async def delete_policy(
    policy_id: str,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT policy_id
            FROM policies
            WHERE policy_id = ?
        """, [policy_id]).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Policy not found"
            )

        con.execute("""
            DELETE FROM policies
            WHERE policy_id = ?
        """, [policy_id])

        return {
            "message": "Policy deleted successfully",
            "policy_id": policy_id
        }

    finally:
        con.close()


# =========================
# GET POLICY WITH CLAIMS
# =========================
@router.get("/{policy_id}/claims")
async def get_policy_with_claims(
    policy_id: str,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        # Get policy
        policy = con.execute("""
            SELECT
                policy_id,
                customer_id,
                policy_type,
                premium,
                status
            FROM policies
            WHERE policy_id = ?
        """, [policy_id]).fetchone()

        if policy is None:
            raise HTTPException(
                status_code=404,
                detail="Policy not found"
            )

        # Get claims for this policy
        claims = con.execute("""
            SELECT
                claim_id,
                customer_id,
                policy_id,
                claim_amount,
                status
            FROM fact_claims
            WHERE policy_id = ?
            ORDER BY claim_id
        """, [policy_id]).fetchall()

        return {
            "policy": {
                "policy_id": policy[0],
                "customer_id": policy[1],
                "policy_type": policy[2],
                "premium": policy[3],
                "status": policy[4]
            },
            "claims": [
                {
                    "claim_id": row[0],
                    "customer_id": row[1],
                    "policy_id": row[2],
                    "claim_amount": row[3],
                    "status": row[4]
                }
                for row in claims
            ]
        }

    finally:
        con.close()