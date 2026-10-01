import duckdb

con = duckdb.connect("dbt_insureiq360/dev.duckdb")

con.execute("""
INSERT OR REPLACE INTO alert_workflows
(
    alert_id,
    claim_id,
    alert_type,
    assigned_to,
    workflow_status,
    trigger,
    acknowledged_at
)
VALUES
(
    'INV-CLM001',
    'CLM001',
    'Investigator',
    'Investigator',
    'Assigned',
    'High-risk claim',
    NULL
),
(
    'SLA-CLM001',
    'CLM001',
    'SLA Breach',
    'Manager',
    'Escalated',
    'SLA breach',
    NULL
)
""")

con.close()

print("Alert workflow records created successfully")
