import pandas as pd
from pathlib import Path

# --------------------------------------------------
# INSUREIQ360 - GOLD DATA CREATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

BRONZE_DIR = BASE_DIR / "data" / "bronze"
GOLD_DIR = BASE_DIR / "data" / "gold"

# Create Gold folder if it doesn't exist
GOLD_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(filename):
    """Load a CSV file from Bronze."""
    path = BRONZE_DIR / filename

    if not path.exists():
        print(f"WARNING: {filename} not found")
        return None

    df = pd.read_csv(path)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def save_gold(df, filename):
    """Save dataframe to Gold."""
    if df is not None:
        output = GOLD_DIR / filename
        df.to_csv(output, index=False)
        print(f"Created: {output}")


# --------------------------------------------------
# LOAD BRONZE DATA
# --------------------------------------------------

customers = load_csv("customers.csv")
policies = load_csv("policies.csv")
claims = load_csv("claims.csv")
payments = load_csv("payments.csv")
repairs = load_csv("repairs.csv")
support = load_csv("support.csv")


# --------------------------------------------------
# CUSTOMERS GOLD
# --------------------------------------------------

if customers is not None:

    customers_gold = customers.drop_duplicates()

    save_gold(
        customers_gold,
        "customers_gold.csv"
    )


# --------------------------------------------------
# POLICIES GOLD
# --------------------------------------------------

if policies is not None:

    policies_gold = policies.drop_duplicates()

    save_gold(
        policies_gold,
        "policies_gold.csv"
    )


# --------------------------------------------------
# CLAIMS GOLD
# --------------------------------------------------

if claims is not None:

    claims_gold = claims.drop_duplicates()

    save_gold(
        claims_gold,
        "claims_gold.csv"
    )


# --------------------------------------------------
# PAYMENTS GOLD
# --------------------------------------------------

if payments is not None:

    payments_gold = payments.drop_duplicates()

    save_gold(
        payments_gold,
        "payments_gold.csv"
    )


# --------------------------------------------------
# REPAIRS GOLD
# --------------------------------------------------

if repairs is not None:

    repairs_gold = repairs.drop_duplicates()

    save_gold(
        repairs_gold,
        "repairs_gold.csv"
    )


# --------------------------------------------------
# SUPPORT GOLD
# --------------------------------------------------

if support is not None:

    support_gold = support.drop_duplicates()

    save_gold(
        support,
        "support_gold.csv"
    )


# --------------------------------------------------
# INSURANCE KPI
# --------------------------------------------------

kpi = {}

if customers is not None:
    kpi["total_customers"] = len(customers)

if policies is not None:
    kpi["total_policies"] = len(policies)

if claims is not None:
    kpi["total_claims"] = len(claims)

if payments is not None:
    kpi["total_payments"] = len(payments)

if repairs is not None:
    kpi["total_repairs"] = len(repairs)

if support is not None:
    kpi["total_support_tickets"] = len(support)


# Create KPI dataframe
kpi_df = pd.DataFrame([kpi])

save_gold(
    kpi_df,
    "insurance_kpis.csv"
)


print("\n====================================")
print("INSUREIQ360 GOLD DATA CREATED")
print("====================================")
print(f"Gold folder: {GOLD_DIR}")