from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# INSUREIQ360 VISUALIZATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE = PROJECT_ROOT / "database" / "insureIQ360.db"

OUTPUT_DIR = PROJECT_ROOT / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# CONNECT TO DATABASE
# ============================================================

print("=" * 60)
print("             INSUREIQ360 VISUALIZATION")
print("=" * 60)

print(f"\nDatabase: {DATABASE}")

if not DATABASE.exists():
    print("\nERROR: Database not found!")
    print(DATABASE)
    exit()

connection = sqlite3.connect(DATABASE)

print("✓ Database connected")


# ============================================================
# 1. RECORD COUNT BY TABLE
# ============================================================

tables = [
    "customers",
    "policies",
    "claims",
    "payments",
    "repairs",
    "support"
]

counts = []

for table in tables:

    query = f'SELECT COUNT(*) AS count FROM "{table}"'

    df = pd.read_sql_query(query, connection)

    counts.append(df["count"].iloc[0])


count_df = pd.DataFrame({
    "table": tables,
    "records": counts
})


plt.figure(figsize=(10, 6))

plt.bar(
    count_df["table"],
    count_df["records"]
)

plt.title("InsureIQ360 - Records by Dataset")
plt.xlabel("Dataset")
plt.ylabel("Number of Records")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "records_by_dataset.png",
    dpi=300
)

plt.show()


# ============================================================
# 2. CLAIM STATUS
# ============================================================

try:

    query = """
        SELECT claim_status, COUNT(*) AS count
        FROM claims
        GROUP BY claim_status
        ORDER BY count DESC
    """

    claims_status = pd.read_sql_query(
        query,
        connection
    )

    if not claims_status.empty:

        plt.figure(figsize=(9, 6))

        plt.bar(
            claims_status["claim_status"].astype(str),
            claims_status["count"]
        )

        plt.title("Claims by Status")
        plt.xlabel("Claim Status")
        plt.ylabel("Number of Claims")

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig(
            OUTPUT_DIR / "claims_by_status.png",
            dpi=300
        )

        plt.show()

except Exception as error:

    print(f"\n⚠ Could not create claim status chart: {error}")


# ============================================================
# 3. POLICY STATUS
# ============================================================

try:

    query = """
        SELECT policy_status, COUNT(*) AS count
        FROM policies
        GROUP BY policy_status
        ORDER BY count DESC
    """

    policy_status = pd.read_sql_query(
        query,
        connection
    )

    if not policy_status.empty:

        plt.figure(figsize=(9, 6))

        plt.bar(
            policy_status["policy_status"].astype(str),
            policy_status["count"]
        )

        plt.title("Policies by Status")
        plt.xlabel("Policy Status")
        plt.ylabel("Number of Policies")

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig(
            OUTPUT_DIR / "policies_by_status.png",
            dpi=300
        )

        plt.show()

except Exception as error:

    print(f"\n⚠ Could not create policy status chart: {error}")


# ============================================================
# 4. PAYMENT STATUS
# ============================================================

try:

    query = """
        SELECT payment_status, COUNT(*) AS count
        FROM payments
        GROUP BY payment_status
        ORDER BY count DESC
    """

    payment_status = pd.read_sql_query(
        query,
        connection
    )

    if not payment_status.empty:

        plt.figure(figsize=(9, 6))

        plt.bar(
            payment_status["payment_status"].astype(str),
            payment_status["count"]
        )

        plt.title("Payments by Status")
        plt.xlabel("Payment Status")
        plt.ylabel("Number of Payments")

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig(
            OUTPUT_DIR / "payments_by_status.png",
            dpi=300
        )

        plt.show()

except Exception as error:

    print(f"\n⚠ Could not create payment status chart: {error}")


# ============================================================
# 5. CLAIM AMOUNT
# ============================================================

try:

    query = """
        SELECT claim_amount
        FROM claims
        WHERE claim_amount IS NOT NULL
    """

    claim_amount = pd.read_sql_query(
        query,
        connection
    )

    if not claim_amount.empty:

        plt.figure(figsize=(10, 6))

        plt.hist(
            claim_amount["claim_amount"],
            bins=30
        )

        plt.title("Claim Amount Distribution")
        plt.xlabel("Claim Amount")
        plt.ylabel("Number of Claims")

        plt.tight_layout()

        plt.savefig(
            OUTPUT_DIR / "claim_amount_distribution.png",
            dpi=300
        )

        plt.show()

except Exception as error:

    print(f"\n⚠ Could not create claim amount chart: {error}")


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

print("\n" + "=" * 60)
print("       VISUALIZATION COMPLETED")
print("=" * 60)

print(f"\nCharts saved in:")

print(OUTPUT_DIR)

print("\nGenerated charts:")
print("✓ records_by_dataset.png")
print("✓ claims_by_status.png")
print("✓ policies_by_status.png")
print("✓ payments_by_status.png")
print("✓ claim_amount_distribution.png")