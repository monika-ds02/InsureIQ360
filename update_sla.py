import duckdb

con = duckdb.connect("dbt_insureiq360/dev.duckdb")

con.execute("""
UPDATE fact_claims
SET
    submitted_at = CURRENT_TIMESTAMP - INTERVAL 10 DAY,
    sla_deadline = CURRENT_TIMESTAMP - INTERVAL 3 DAY
""")

con.close()

print("SLA dates populated successfully")
