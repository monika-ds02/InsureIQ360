import pandas as pd


BASE = "data/bronze/"

# Load data
claims = pd.read_csv(BASE + "claims.csv")
policies = pd.read_csv(BASE + "policies.csv")
customers = pd.read_csv(BASE + "customers.csv")

# Convert dates
claims["claim_date"] = pd.to_datetime(claims["claim_date"])
policies["start_date"] = pd.to_datetime(policies["start_date"])
policies["end_date"] = pd.to_datetime(policies["end_date"])
customers["date_of_birth"] = pd.to_datetime(customers["date_of_birth"])
customers["registration_date"] = pd.to_datetime(
    customers["registration_date"]
)

# Join claims → policies
df = claims.merge(
    policies[
        [
            "policy_id",
            "customer_id",
            "policy_type",
            "policy_status",
            "premium",
            "coverage_amount",
            "payment_frequency",
            "start_date",
        ]
    ],
    on="policy_id",
    how="left",
)

# Join → customers
df = df.merge(
    customers[
        [
            "customer_id",
            "gender",
            "city",
            "state",
            "customer_segment",
            "income",
            "occupation",
            "date_of_birth",
            "registration_date",
        ]
    ],
    on="customer_id",
    how="left",
)

# Create claim-date features
df["claim_year"] = df["claim_date"].dt.year
df["claim_month"] = df["claim_date"].dt.month

# Customer age at claim
df["customer_age"] = (
    (df["claim_date"] - df["date_of_birth"]).dt.days / 365.25
)

# How long the customer had been registered
df["customer_tenure_days"] = (
    df["claim_date"] - df["registration_date"]
).dt.days

# How long the policy had existed before the claim
df["policy_age_days"] = (
    df["claim_date"] - df["start_date"]
).dt.days

# Remove impossible/invalid values
df = df[
    (df["customer_age"] >= 18) &
    (df["customer_age"] <= 100) &
    (df["policy_age_days"] >= 0)
].copy()

# Save feature dataset
output = "data/bronze/claims_ml_features.csv"

df.to_csv(output, index=False)

print("Feature engineering completed!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSaved:")
print(output)