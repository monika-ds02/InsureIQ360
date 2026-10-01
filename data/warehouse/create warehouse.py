import pandas as pd
from pathlib import Path

# ============================================================
# INSUREIQ 360 - CREATE DATA WAREHOUSE
# Silver -> Warehouse
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SILVER_DIR = BASE_DIR / "data" / "silver"
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"

# Create warehouse folder
WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("INSUREIQ 360 DATA WAREHOUSE")
print("=" * 60)

print("\nSilver folder:")
print(SILVER_DIR)

print("\nWarehouse folder:")
print(WAREHOUSE_DIR)


# Silver file -> Warehouse file
files = {
    "customers_cleaned.csv": "customers.csv",
    "policies_cleaned.csv": "policies.csv",
    "claims_cleaned.csv": "claims.csv",
    "payments_cleaned.csv": "payments.csv",
    "repairs_cleaned.csv": "repairs.csv",
    "support_cleaned.csv": "support.csv"
}


for silver_file, warehouse_file in files.items():

    source = SILVER_DIR / silver_file
    destination = WAREHOUSE_DIR / warehouse_file

    print("\nProcessing:", silver_file)

    if not source.exists():
        print("ERROR: File not found")
        print(source)
        continue

    df = pd.read_csv(source)

    df.to_csv(destination, index=False)

    print("Created:", warehouse_file)
    print("Rows:", len(df))
    print("Columns:", len(df.columns))


# ============================================================
# FINAL CHECK
# ============================================================

print("\n" + "=" * 60)
print("WAREHOUSE CREATED")
print("=" * 60)

for file in WAREHOUSE_DIR.glob("*.csv"):
    print("✓", file.name)
1
print("\nWarehouse location:")
print(WAREHOUSE_DIR)

print("\n" + "=" * 60)
print("COMPLETED")
print("=" * 60)