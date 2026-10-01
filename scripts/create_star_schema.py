from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# INSUREIQ360 - STAR SCHEMA CREATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE = PROJECT_ROOT / "database" / "insureIQ360.db"


print("=" * 70)
print("             INSUREIQ360 STAR SCHEMA")
print("=" * 70)

print(f"\nDatabase:")
print(DATABASE)


# ============================================================
# CHECK DATABASE
# ============================================================

if not DATABASE.exists():
    print("\nERROR: Database does not exist!")
    print(DATABASE)
    raise SystemExit

connection = sqlite3.connect(DATABASE)

print("\n✓ Database connected")


# ============================================================
# CHECK SOURCE TABLES
# ============================================================

required_tables = [
    "customers",
    "policies",
    "claims",
    "payments",
    "repairs"
]

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

existing_tables = {
    row[0] for row in cursor.fetchall()
}

print("\nChecking source tables...")

for table in required_tables:
    if table in existing_tables:
        print(f"✓ {table}")
    else:
        print(f"✗ MISSING: {table}")


missing = [
    table
    for table in required_tables
    if table not in existing_tables
]

if missing:
    print("\nERROR: Required source tables are missing:")
    print(missing)
    connection.close()
    raise SystemExit


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_names):

    lower_columns = {
        column.lower(): column
        for column in df.columns
    }

    for name in possible_names:
        if name.lower() in lower_columns:
            return lower_columns[name.lower()]

    return None


def require_column(df, possible_names, table_name):

    column = find_column(df, possible_names)

    if column is None:

        print(
            f"\nERROR: Could not find required column in "
            f"{table_name}: {possible_names}"
        )

        print("Available columns:")
        print(list(df.columns))

        raise ValueError(
            f"Missing column in {table_name}"
        )

    return column


# ============================================================
# READ SOURCE TABLES
# ============================================================

print("\nReading warehouse tables...")

customers = pd.read_sql_query(
    "SELECT * FROM customers",
    connection
)

policies = pd.read_sql_query(
    "SELECT * FROM policies",
    connection
)

claims = pd.read_sql_query(
    "SELECT * FROM claims",
    connection
)

payments = pd.read_sql_query(
    "SELECT * FROM payments",
    connection
)

repairs = pd.read_sql_query(
    "SELECT * FROM repairs",
    connection
)

print(f"✓ Customers : {len(customers)}")
print(f"✓ Policies  : {len(policies)}")
print(f"✓ Claims    : {len(claims)}")
print(f"✓ Payments  : {len(payments)}")
print(f"✓ Repairs   : {len(repairs)}")


# ============================================================
# IDENTIFY IMPORTANT COLUMNS
# ============================================================

# ---------------- CUSTOMER ----------------

customer_id_customers = require_column(
    customers,
    ["customer_id"],
    "customers"
)

customer_segment = find_column(
    customers,
    ["segment", "customer_segment"]
)

customer_geography = find_column(
    customers,
    ["geography", "region", "location"]
)


# ---------------- POLICY ----------------

policy_id = require_column(
    policies,
    ["policy_id"],
    "policies"
)

policy_customer_id = require_column(
    policies,
    ["customer_id"],
    "policies"
)

policy_product = find_column(
    policies,
    ["product", "product_type", "policy_type"]
)

policy_premium = find_column(
    policies,
    ["premium", "premium_amount"]
)

policy_start_date = find_column(
    policies,
    ["start_date", "policy_start_date"]
)

policy_end_date = find_column(
    policies,
    ["end_date", "policy_end_date"]
)


# ---------------- CLAIM ----------------

claim_id = require_column(
    claims,
    ["claim_id"],
    "claims"
)

claim_policy_id = require_column(
    claims,
    ["policy_id"],
    "claims"
)

claim_date = require_column(
    claims,
    ["incident_date", "claim_date", "date"],
    "claims"
)

claim_amount = require_column(
    claims,
    ["claimed_amount", "claim_amount"],
    "claims"
)

claim_type = find_column(
    claims,
    ["type", "claim_type"]
)

claim_status = find_column(
    claims,
    ["status", "claim_status"]
)


# ---------------- PAYMENT ----------------
# IMPORTANT:
# Your actual payments table has:
# payment_id
# customer_id
# policy_id
# payment_amount
# payment_method
# payment_status
# payment_date
# transaction_id
#
# There is NO claim_id.

payment_id = require_column(
    payments,
    ["payment_id"],
    "payments"
)

payment_customer_id = require_column(
    payments,
    ["customer_id"],
    "payments"
)

payment_policy_id = require_column(
    payments,
    ["policy_id"],
    "payments"
)

payment_amount = require_column(
    payments,
    ["payment_amount"],
    "payments"
)

payment_date = require_column(
    payments,
    ["payment_date"],
    "payments"
)

payment_status = require_column(
    payments,
    ["payment_status"],
    "payments"
)


# ---------------- REPAIR ----------------

repair_id = require_column(
    repairs,
    ["repair_id"],
    "repairs"
)

repair_claim_id = require_column(
    repairs,
    ["claim_id"],
    "repairs"
)

repair_estimate = find_column(
    repairs,
    ["estimate", "repair_estimate", "estimated_amount"]
)

repair_approved = find_column(
    repairs,
    ["approved_amount", "approved_cost", "repair_cost"]
)


# ============================================================
# 1. DIM_CUSTOMER
# ============================================================

print("\n[1] Creating dim_customer...")

dim_customer = customers[
    [customer_id_customers]
].copy()

dim_customer.rename(
    columns={
        customer_id_customers: "customer_id"
    },
    inplace=True
)

if customer_segment:
    dim_customer["segment"] = customers[customer_segment]
else:
    dim_customer["segment"] = None

if customer_geography:
    dim_customer["geography"] = customers[customer_geography]
else:
    dim_customer["geography"] = None

dim_customer.insert(
    0,
    "customer_key",
    range(1, len(dim_customer) + 1)
)

dim_customer.to_sql(
    "dim_customer",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ dim_customer: {len(dim_customer)} rows")


# ============================================================
# 2. DIM_PRODUCT
# ============================================================

print("\n[2] Creating dim_product...")

if policy_product:

    products = (
        policies[[policy_product]]
        .drop_duplicates()
        .rename(
            columns={
                policy_product: "product"
            }
        )
        .reset_index(drop=True)
    )

else:

    products = pd.DataFrame({
        "product": ["Unknown"]
    })


products.insert(
    0,
    "product_key",
    range(1, len(products) + 1)
)

products.to_sql(
    "dim_product",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ dim_product: {len(products)} rows")


# ============================================================
# 3. DIM_GEOGRAPHY
# ============================================================

print("\n[3] Creating dim_geography...")

if customer_geography:

    geography = (
        customers[[customer_geography]]
        .drop_duplicates()
        .rename(
            columns={
                customer_geography: "geography"
            }
        )
        .reset_index(drop=True)
    )

else:

    geography = pd.DataFrame({
        "geography": ["Unknown"]
    })


geography.insert(
    0,
    "geography_key",
    range(1, len(geography) + 1)
)

geography.to_sql(
    "dim_geography",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ dim_geography: {len(geography)} rows")


# ============================================================
# 4. DIM_POLICY
# ============================================================

print("\n[4] Creating dim_policy...")

dim_policy = policies[
    [
        policy_id,
        policy_customer_id
    ]
].copy()

dim_policy.rename(
    columns={
        policy_id: "policy_id",
        policy_customer_id: "customer_id"
    },
    inplace=True
)

if policy_product:
    dim_policy["product"] = policies[policy_product]
else:
    dim_policy["product"] = "Unknown"

if policy_premium:
    dim_policy["premium"] = pd.to_numeric(
        policies[policy_premium],
        errors="coerce"
    )
else:
    dim_policy["premium"] = 0

if policy_start_date:
    dim_policy["start_date"] = policies[policy_start_date]
else:
    dim_policy["start_date"] = None

if policy_end_date:
    dim_policy["end_date"] = policies[policy_end_date]
else:
    dim_policy["end_date"] = None

dim_policy.insert(
    0,
    "policy_key",
    range(1, len(dim_policy) + 1)
)

dim_policy.to_sql(
    "dim_policy",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ dim_policy: {len(dim_policy)} rows")


# ============================================================
# 5. DIM_DATE
# ============================================================

print("\n[5] Creating dim_date...")

date_columns = []

for df, column in [
    (claims, claim_date),
    (payments, payment_date),
    (policies, policy_start_date),
    (policies, policy_end_date)
]:

    if column:

        dates = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        date_columns.extend(
            dates.dropna().dt.normalize().tolist()
        )


if date_columns:

    unique_dates = sorted(
        set(date_columns)
    )

else:

    unique_dates = []


dim_date = pd.DataFrame({
    "full_date": unique_dates
})

if not dim_date.empty:

    dim_date["full_date"] = pd.to_datetime(
        dim_date["full_date"]
    )

    dim_date.insert(
        0,
        "date_key",
        dim_date["full_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    dim_date["year"] = (
        dim_date["full_date"].dt.year
    )

    dim_date["quarter"] = (
        dim_date["full_date"].dt.quarter
    )

    dim_date["month"] = (
        dim_date["full_date"].dt.month
    )

    dim_date["month_name"] = (
        dim_date["full_date"].dt.month_name()
    )

    dim_date["day"] = (
        dim_date["full_date"].dt.day
    )

    dim_date["day_name"] = (
        dim_date["full_date"].dt.day_name()
    )

else:

    dim_date = pd.DataFrame(
        columns=[
            "date_key",
            "full_date",
            "year",
            "quarter",
            "month",
            "month_name",
            "day",
            "day_name"
        ]
    )


dim_date.to_sql(
    "dim_date",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ dim_date: {len(dim_date)} rows")


# ============================================================
# CREATE LOOKUPS
# ============================================================

customer_lookup = dict(
    zip(
        dim_customer["customer_id"],
        dim_customer["customer_key"]
    )
)

policy_lookup = dict(
    zip(
        dim_policy["policy_id"],
        dim_policy["policy_key"]
    )
)

product_lookup = dict(
    zip(
        products["product"],
        products["product_key"]
    )
)

geography_lookup = dict(
    zip(
        geography["geography"],
        geography["geography_key"]
    )
)


# ============================================================
# POLICY LOOKUPS
# ============================================================

policy_customer_lookup = dict(
    zip(
        policies[policy_id],
        policies[policy_customer_id]
    )
)

if policy_product:

    policy_product_lookup = dict(
        zip(
            policies[policy_id],
            policies[policy_product]
        )
    )

else:

    policy_product_lookup = {}


# ============================================================
# 6. FACT_CLAIM
# ============================================================

print("\n[6] Creating fact_claim...")

fact_claim = pd.DataFrame()

fact_claim["claim_id"] = claims[claim_id]

fact_claim["policy_key"] = (
    claims[claim_policy_id]
    .map(policy_lookup)
)

claim_customer_ids = (
    claims[claim_policy_id]
    .map(policy_customer_lookup)
)

fact_claim["customer_key"] = (
    claim_customer_ids
    .map(customer_lookup)
)


# Product

if policy_product:

    claim_products = (
        claims[claim_policy_id]
        .map(policy_product_lookup)
    )

    fact_claim["product_key"] = (
        claim_products.map(product_lookup)
    )

else:

    fact_claim["product_key"] = None


# Geography

if customer_geography:

    customer_geo_lookup = dict(
        zip(
            customers[customer_id_customers],
            customers[customer_geography]
        )
    )

    claim_geographies = (
        claim_customer_ids
        .map(customer_geo_lookup)
    )

    fact_claim["geography_key"] = (
        claim_geographies.map(geography_lookup)
    )

else:

    fact_claim["geography_key"] = None


# Date

claim_dates = pd.to_datetime(
    claims[claim_date],
    errors="coerce"
)

fact_claim["date_key"] = (
    claim_dates
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)

fact_claim["claim_amount"] = pd.to_numeric(
    claims[claim_amount],
    errors="coerce"
)

if claim_type:
    fact_claim["claim_type"] = claims[claim_type]
else:
    fact_claim["claim_type"] = None

if claim_status:
    fact_claim["claim_status"] = claims[claim_status]
else:
    fact_claim["claim_status"] = None


fact_claim.to_sql(
    "fact_claim",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ fact_claim: {len(fact_claim)} rows")


# ============================================================
# 7. FACT_PAYMENT
# ============================================================

print("\n[7] Creating fact_payment...")

fact_payment = pd.DataFrame()

fact_payment["payment_id"] = payments[payment_id]

# IMPORTANT:
# Payments contain policy_id and customer_id directly.
# There is no claim_id in the payments table.

fact_payment["policy_key"] = (
    payments[payment_policy_id]
    .map(policy_lookup)
)

fact_payment["customer_key"] = (
    payments[payment_customer_id]
    .map(customer_lookup)
)

fact_payment["amount"] = pd.to_numeric(
    payments[payment_amount],
    errors="coerce"
)


# Payment date

dates = pd.to_datetime(
    payments[payment_date],
    errors="coerce"
)

fact_payment["date_key"] = (
    dates
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)


fact_payment["payment_status"] = (
    payments[payment_status]
)


fact_payment.to_sql(
    "fact_payment",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ fact_payment: {len(fact_payment)} rows")


# ============================================================
# 8. FACT_REPAIR
# ============================================================

print("\n[8] Creating fact_repair...")

fact_repair = pd.DataFrame()

fact_repair["repair_id"] = repairs[repair_id]

fact_repair["claim_id"] = repairs[repair_claim_id]


# Repair → Claim → Policy

repair_policy_ids = (
    repairs[repair_claim_id]
    .map(
        dict(
            zip(
                claims[claim_id],
                claims[claim_policy_id]
            )
        )
    )
)

fact_repair["policy_key"] = (
    repair_policy_ids
    .map(policy_lookup)
)


if repair_estimate:

    fact_repair["estimate"] = pd.to_numeric(
        repairs[repair_estimate],
        errors="coerce"
    )

else:

    fact_repair["estimate"] = 0


if repair_approved:

    fact_repair["approved_amount"] = pd.to_numeric(
        repairs[repair_approved],
        errors="coerce"
    )

else:

    fact_repair["approved_amount"] = 0


fact_repair.to_sql(
    "fact_repair",
    connection,
    if_exists="replace",
    index=False
)

print(f"✓ fact_repair: {len(fact_repair)} rows")


# ============================================================
# COMMIT
# ============================================================

connection.commit()


# ============================================================
# FINAL STAR SCHEMA
# ============================================================

print("\n" + "=" * 70)
print("                 STAR SCHEMA CREATED")
print("=" * 70)

star_tables = [
    "dim_customer",
    "dim_policy",
    "dim_product",
    "dim_geography",
    "dim_date",
    "fact_claim",
    "fact_payment",
    "fact_repair"
]

print("\nStar Schema Tables:")

for table in star_tables:

    cursor.execute(
        f'SELECT COUNT(*) FROM "{table}"'
    )

    count = cursor.fetchone()[0]

    print(
        f"✓ {table:<20} {count:,} rows"
    )


connection.close()

print("\n" + "=" * 70)
print("              STAR SCHEMA COMPLETE")
print("=" * 70)