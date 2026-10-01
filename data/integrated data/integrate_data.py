import pandas as pd
import os

# --------------------------------------------------
# FOLDERS
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SILVER_FOLDER = os.path.join(BASE_DIR, "silver")

print("Silver folder:", SILVER_FOLDER)


# --------------------------------------------------
# LOAD CLEANED DATA
# --------------------------------------------------

print("\nLoading cleaned datasets...")

customers = pd.read_csv(
    os.path.join(SILVER_FOLDER, "customers_cleaned.csv")
)

policies = pd.read_csv(
    os.path.join(SILVER_FOLDER, "policies_cleaned.csv")
)

claims = pd.read_csv(
    os.path.join(SILVER_FOLDER, "claims_cleaned.csv")
)

payments = pd.read_csv(
    os.path.join(SILVER_FOLDER, "payments_cleaned.csv")
)

repairs = pd.read_csv(
    os.path.join(SILVER_FOLDER, "repairs_cleaned.csv")
)

support = pd.read_csv(
    os.path.join(SILVER_FOLDER, "support_cleaned.csv")
)


# --------------------------------------------------
# CUSTOMERS + POLICIES
# --------------------------------------------------

print("\nIntegrating customers + policies...")

customer_policies = customers.merge(
    policies,
    on="customer_id",
    how="left",
    suffixes=("_customer", "_policy")
)


# --------------------------------------------------
# POLICIES + CLAIMS
# --------------------------------------------------

print("Integrating claims...")

customer_policies_claims = customer_policies.merge(
    claims,
    on="policy_id",
    how="left"
)


# --------------------------------------------------
# CLAIMS + REPAIRS
# --------------------------------------------------

print("Integrating repairs...")

integrated_data = customer_policies_claims.merge(
    repairs,
    on="claim_id",
    how="left",
    suffixes=("_claim", "_repair")
)


# --------------------------------------------------
# PAYMENTS
# --------------------------------------------------

print("Integrating payments...")

integrated_data = integrated_data.merge(
    payments,
    on=["customer_id", "policy_id"],
    how="left",
    suffixes=("", "_payment")
)


# --------------------------------------------------
# SUPPORT
# --------------------------------------------------

print("Integrating support...")

integrated_data = integrated_data.merge(
    support,
    on="customer_id",
    how="left",
    suffixes=("", "_support")
)


# --------------------------------------------------
# REMOVE DUPLICATE COLUMNS
# --------------------------------------------------

integrated_data = integrated_data.loc[
    :,
    ~integrated_data.columns.duplicated()
]


# --------------------------------------------------
# SAVE INTEGRATED DATA IN SILVER
# --------------------------------------------------

output_path = os.path.join(
    SILVER_FOLDER,
    "integrated_insurance_data.csv"
)

integrated_data.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# FINAL OUTPUT
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA INTEGRATION COMPLETED")
print("=" * 60)

print("Rows:", len(integrated_data))
print("Columns:", len(integrated_data.columns))

print("\nIntegrated Data Preview:")
print(integrated_data.head())

print("\nSaved to:")
print(output_path)

print("\n" + "=" * 60)