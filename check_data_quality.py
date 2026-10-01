import duckdb

print("InsureIQ360 Data Quality Script Running")

DB_PATH = "dbt_insureiq360/dev.duckdb"

con = duckdb.connect(DB_PATH)

total_claims = con.execute("""
    SELECT COUNT(*)
    FROM fact_claims
""").fetchone()[0]

print("Total Claims:", total_claims)

con.close()

print("Quality Check Completed")