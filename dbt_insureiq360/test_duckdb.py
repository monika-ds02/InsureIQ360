import duckdb

conn = duckdb.connect("dev.duckdb")

conn.execute("INSTALL sqlite")
conn.execute("LOAD sqlite")

rows = conn.execute("""
    SELECT *
    FROM sqlite_scan(
        '../data/bronze/insureIQ360_bronze.db',
        'bronze_claims'
    )
    LIMIT 2
""").fetchall()

print("Bronze data:")
for row in rows:
    print(row)

conn.close()