from pathlib import Path
import pandas as pd
import sqlite3

# ============================================================
# INSUREIQ360 PROJECT PATHS
# ============================================================

# This file is:
# InsureIQ360/scripts/validate_warehouse.py

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"
SILVER_DIR = PROJECT_ROOT / "data" / "silver"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_FILE = DATABASE_DIR / "insureIQ360.db"


# ============================================================
# EXPECTED DATASETS
# ============================================================

DATASETS = [
    "customers",
    "policies",
    "claims",
    "payments",
    "repairs",
    "support"
]


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("        INSUREIQ360 WAREHOUSE VALIDATION")
print("=" * 60)

print(f"\nProject folder : {PROJECT_ROOT}")
print(f"Bronze folder  : {BRONZE_DIR}")
print(f"Silver folder  : {SILVER_DIR}")
print(f"Database       : {DATABASE_FILE}")


# ============================================================
# 1. CHECK BRONZE DATA
# ============================================================

print("\n[1] CHECKING BRONZE DATA")
print("-" * 60)

bronze_pass = True

for dataset in DATASETS:

    file_path = BRONZE_DIR / f"{dataset}.csv"

    if not file_path.exists():
        print(f"✗ MISSING  : {file_path}")
        bronze_pass = False
        continue

    try:
        df = pd.read_csv(file_path)

        print(
            f"✓ FOUND    : {dataset}.csv "
            f"({len(df)} rows, {len(df.columns)} columns)"
        )

    except Exception as error:
        print(f"✗ ERROR    : {dataset}.csv -> {error}")
        bronze_pass = False


# ============================================================
# 2. CHECK SILVER DATA
# ============================================================

print("\n[2] CHECKING SILVER DATA")
print("-" * 60)

silver_pass = True

for dataset in DATASETS:

    file_path = SILVER_DIR / f"{dataset}_cleaned.csv"

    if not file_path.exists():
        print(f"✗ MISSING  : {file_path}")
        silver_pass = False
        continue

    try:
        df = pd.read_csv(file_path)

        if len(df) == 0:
            print(f"✗ EMPTY    : {dataset}_cleaned.csv")
            silver_pass = False
        else:
            print(
                f"✓ FOUND    : {dataset}_cleaned.csv "
                f"({len(df)} rows, {len(df.columns)} columns)"
            )

    except Exception as error:
        print(f"✗ ERROR    : {dataset}_cleaned.csv -> {error}")
        silver_pass = False


# ============================================================
# 3. CHECK DATABASE
# ============================================================

print("\n[3] CHECKING SQLITE WAREHOUSE")
print("-" * 60)

database_pass = True

if not DATABASE_FILE.exists():

    print(f"✗ DATABASE MISSING: {DATABASE_FILE}")
    database_pass = False

else:

    print(f"✓ DATABASE FOUND: {DATABASE_FILE}")

    try:

        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()

        # Get all SQLite tables
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """)

        existing_tables = {
            row[0] for row in cursor.fetchall()
        }

        print("\nWarehouse tables:")

        for dataset in DATASETS:

            if dataset not in existing_tables:

                print(f"✗ TABLE MISSING : {dataset}")
                database_pass = False

            else:

                cursor.execute(
                    f'SELECT COUNT(*) FROM "{dataset}"'
                )

                row_count = cursor.fetchone()[0]

                if row_count == 0:

                    print(
                        f"✗ EMPTY TABLE  : "
                        f"{dataset} (0 rows)"
                    )

                    database_pass = False

                else:

                    print(
                        f"✓ TABLE        : "
                        f"{dataset} ({row_count} rows)"
                    )

        connection.close()

    except sqlite3.Error as error:

        print(f"✗ DATABASE ERROR: {error}")
        database_pass = False


# ============================================================
# 4. FINAL RESULT
# ============================================================

print("\n" + "=" * 60)
print("                  FINAL RESULT")
print("=" * 60)

if bronze_pass:
    print("✓ BRONZE  : PASSED")
else:
    print("✗ BRONZE  : FAILED")

if silver_pass:
    print("✓ SILVER  : PASSED")
else:
    print("✗ SILVER  : FAILED")

if database_pass:
    print("✓ DATABASE: PASSED")
else:
    print("✗ DATABASE: FAILED")

print("=" * 60)


if bronze_pass and silver_pass and database_pass:

    print("\n🎉 INSUREIQ360 WAREHOUSE VALIDATION PASSED!")
    print("All Bronze, Silver and Database checks are successful.")

else:

    print("\n⚠ VALIDATION FAILED")
    print("Fix the failed section(s) shown above.")