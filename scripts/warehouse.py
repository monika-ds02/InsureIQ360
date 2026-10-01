from pathlib import Path
import pandas as pd
import sqlite3

# ============================================================
# INSUREIQ360 WAREHOUSE LOADER
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SILVER_DIR = PROJECT_ROOT / "data" / "silver"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_FILE = DATABASE_DIR / "insureIQ360.db"

# Make sure database folder exists
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# Datasets
TABLES = [
    "customers",
    "policies",
    "claims",
    "payments",
    "repairs",
    "support"
]

print("=" * 60)
print("       INSUREIQ360 SQLITE WAREHOUSE LOADING")
print("=" * 60)

print(f"\nSilver folder : {SILVER_DIR}")
print(f"Database      : {DATABASE_FILE}")


# ============================================================
# CONNECT TO DATABASE
# ============================================================

connection = sqlite3.connect(DATABASE_FILE)

print("\nDatabase connection successful.")


# ============================================================
# LOAD SILVER CSV FILES
# ============================================================

for table in TABLES:

    csv_file = SILVER_DIR / f"{table}_cleaned.csv"

    print("\n" + "-" * 60)
    print(f"Loading: {csv_file.name}")
    print(f"Table  : {table}")

    if not csv_file.exists():

        print(f"ERROR: File not found: {csv_file}")
        continue

    try:

        # Read Silver CSV
        df = pd.read_csv(csv_file)

        print(f"Rows read: {len(df)}")
        print(f"Columns  : {len(df.columns)}")

        # Load into SQLite
        df.to_sql(
            table,
            connection,
            if_exists="replace",
            index=False
        )

        # Verify row count
        cursor = connection.cursor()

        cursor.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        )

        count = cursor.fetchone()[0]

        print(f"✓ Loaded {count} rows into {table}")

    except Exception as error:

        print(f"✗ ERROR loading {table}")
        print(error)


# ============================================================
# SAVE DATABASE
# ============================================================

connection.commit()
connection.close()

print("\n" + "=" * 60)
print("          WAREHOUSE LOADING COMPLETED")
print("=" * 60)

print(f"\nDatabase created/updated:")
print(DATABASE_FILE)

print("\nRun validation with:")

print("python .\\scripts\\validate_warehouse.py")