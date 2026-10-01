from fastapi import APIRouter, Depends
import duckdb

from api.main import get_current_user


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


DB_PATH = "dbt_insureiq360/dev.duckdb"


def get_connection():
    return duckdb.connect(DB_PATH)


def calculate_risk_score(claim_amount):
    if claim_amount >= 30000:
        return 100
    elif claim_amount >= 20000:
        return 80
    elif claim_amount >= 10000:
        return 60
    elif claim_amount >= 5000:
        return 40
    else:
        return 20


# -----------------------------------------
# ALL RISK ALERTS
# -----------------------------------------

@router.get("/")
async def get_alerts(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                claim_id,
                policy_id,
                claim_amount,
                status
            FROM fact_claims
            WHERE LOWER(status) = 'pending'
            ORDER BY claim_amount DESC
        """).fetchall()

        alerts = []

        for row in rows:
            claim_id = row[0]
            policy_id = row[1]
            claim_amount = row[2]
            status = row[3]

            risk_score = calculate_risk_score(claim_amount)

            if risk_score >= 80:
                risk_level = "High"
            elif risk_score >= 60:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            alerts.append({
                "claim_id": claim_id,
                "policy_id": policy_id,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "alert": (
                    f"{risk_level} risk pending claim - "
                    f"₹{claim_amount:,.0f}"
                ),
                "status": status
            })

        return alerts

    finally:
        con.close()


# -----------------------------------------
# HIGH-RISK CLAIM → INVESTIGATOR
# -----------------------------------------

@router.get("/investigator")
async def get_investigator_alerts(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                f.claim_id,
                f.policy_id,
                f.claim_amount,
                aw.workflow_status
            FROM fact_claims f
            LEFT JOIN alert_workflows aw
                ON aw.claim_id = f.claim_id
                AND aw.alert_type = 'Investigator'
            WHERE LOWER(f.status) = 'pending'
            ORDER BY f.claim_amount DESC
        """).fetchall()

        investigator_alerts = []

        for row in rows:
            claim_id = row[0]
            policy_id = row[1]
            claim_amount = row[2]
            workflow_status = row[3]

            risk_score = calculate_risk_score(claim_amount)

            if risk_score >= 80:
                investigator_alerts.append({
                    "claim_id": claim_id,
                    "policy_id": policy_id,
                    "claim_amount": claim_amount,
                    "risk_score": risk_score,
                    "risk_level": "High",
                    "assigned_to": "Investigator",
                    "workflow_status": workflow_status or "Assigned",
                    "trigger": "High-risk claim"
                })

        return investigator_alerts

    finally:
        con.close()


# -----------------------------------------
# SLA BREACH → MANAGER
# -----------------------------------------

@router.get("/sla-breach")
async def get_sla_breach_alerts(
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        rows = con.execute("""
            SELECT
                claim_id,
                policy_id,
                claim_amount,
                status,
                submitted_at,
                sla_deadline
            FROM fact_claims
            WHERE LOWER(status) = 'pending'
              AND sla_deadline < CURRENT_TIMESTAMP
            ORDER BY sla_deadline ASC
        """).fetchall()

        sla_alerts = []

        for row in rows:
            claim_id = row[0]
            policy_id = row[1]
            claim_amount = row[2]
            status = row[3]
            submitted_at = row[4]
            sla_deadline = row[5]

            sla_alerts.append({
                "claim_id": claim_id,
                "policy_id": policy_id,
                "claim_amount": claim_amount,
                "status": status,
                "submitted_at": submitted_at,
                "sla_deadline": sla_deadline,
                "assigned_to": "Manager",
                "workflow_status": "Escalated",
                "trigger": "SLA breach"
            })

        return sla_alerts

    finally:
        con.close()


# -----------------------------------------
# ACKNOWLEDGE ALERT
# -----------------------------------------

@router.put("/acknowledge/{alert_id}")
async def acknowledge_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_user)
):
    con = get_connection()

    try:
        existing = con.execute("""
            SELECT
                alert_id,
                workflow_status
            FROM alert_workflows
            WHERE alert_id = ?
        """, [alert_id]).fetchone()

        if not existing:
            return {
                "message": "Alert workflow not found",
                "alert_id": alert_id
            }

        con.execute("""
            UPDATE alert_workflows
            SET
                workflow_status = 'Acknowledged',
                acknowledged_at = CURRENT_TIMESTAMP
            WHERE alert_id = ?
        """, [alert_id])

        return {
            "message": "Alert acknowledged successfully",
            "alert_id": alert_id,
            "workflow_status": "Acknowledged"
        }

    finally:
        con.close()