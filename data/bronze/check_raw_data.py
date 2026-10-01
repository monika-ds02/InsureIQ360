import pandas as pd
import numpy as np
import os
from faker import Faker

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

NUM_CUSTOMERS = 50000
NUM_POLICIES = 60000
NUM_CLAIMS = 30000
NUM_PAYMENTS = 70000
NUM_REPAIRS = 20000
NUM_SUPPORT = 40000

fake = Faker("en_IN")
np.random.seed(42)

# Bronze folder
folder = os.path.dirname(os.path.abspath(__file__))

print("Creating raw insurance data...")
print("Folder:", folder)

# --------------------------------------------------
# 1. CUSTOMERS
# --------------------------------------------------

print("\nCreating customers...")

customers = pd.DataFrame({
    "customer_id": range(1, NUM_CUSTOMERS + 1),

    "customer_name": [
        fake.name() for _ in range(NUM_CUSTOMERS)
    ],

    "email": [
        fake.email() for _ in range(NUM_CUSTOMERS)
    ],

    "phone": [
        fake.phone_number() for _ in range(NUM_CUSTOMERS)
    ],

    "date_of_birth": [
        fake.date_of_birth(minimum_age=18, maximum_age=70)
        for _ in range(NUM_CUSTOMERS)
    ],

    "gender": np.random.choice(
        ["Male", "Female", "Other"],
        NUM_CUSTOMERS
    ),

    "city": np.random.choice(
        [
            "Bengaluru",
            "Mumbai",
            "Delhi",
            "Hyderabad",
            "Chennai",
            "Pune",
            "Kolkata",
            "Ahmedabad",
            "Jaipur",
            "Kochi"
        ],
        NUM_CUSTOMERS
    ),

    "state": np.random.choice(
        [
            "Karnataka",
            "Maharashtra",
            "Delhi",
            "Telangana",
            "Tamil Nadu",
            "Maharashtra",
            "West Bengal",
            "Gujarat",
            "Rajasthan",
            "Kerala"
        ],
        NUM_CUSTOMERS
    ),

    "pincode": [
        fake.postcode() for _ in range(NUM_CUSTOMERS)
    ],

    "customer_segment": np.random.choice(
        ["Individual", "Corporate", "SME"],
        NUM_CUSTOMERS
    ),

    "income": np.random.randint(
        200000,
        3000000,
        NUM_CUSTOMERS
    ),

    "occupation": np.random.choice(
        [
            "Engineer",
            "Doctor",
            "Teacher",
            "Business",
            "Manager",
            "Developer",
            "Student",
            "Consultant",
            "Government",
            "Other"
        ],
        NUM_CUSTOMERS
    ),

    "registration_date": [
        fake.date_between(
            start_date="-10y",
            end_date="today"
        )
        for _ in range(NUM_CUSTOMERS)
    ]
})

customers.to_csv(
    os.path.join(folder, "customers.csv"),
    index=False
)

print("customers.csv created:", len(customers))


# --------------------------------------------------
# 2. POLICIES
# --------------------------------------------------

print("\nCreating policies...")

policy_customer_ids = np.random.randint(
    1,
    NUM_CUSTOMERS + 1,
    NUM_POLICIES
)

policies = pd.DataFrame({
    "policy_id": range(1, NUM_POLICIES + 1),

    "customer_id": policy_customer_ids,

    "policy_number": [
        f"POL{100000 + i}"
        for i in range(NUM_POLICIES)
    ],

    "policy_type": np.random.choice(
        ["Auto", "Health", "Life", "Home", "Travel"],
        NUM_POLICIES
    ),

    "policy_status": np.random.choice(
        ["Active", "Expired", "Cancelled", "Pending"],
        NUM_POLICIES,
        p=[0.70, 0.15, 0.08, 0.07]
    ),

    "premium": np.round(
        np.random.uniform(5000, 100000, NUM_POLICIES),
        2
    ),

    "coverage_amount": np.round(
        np.random.uniform(100000, 10000000, NUM_POLICIES),
        2
    ),

    "start_date": [
        fake.date_between(
            start_date="-5y",
            end_date="today"
        )
        for _ in range(NUM_POLICIES)
    ],

    "payment_frequency": np.random.choice(
        ["Monthly", "Quarterly", "Half-Yearly", "Yearly"],
        NUM_POLICIES
    ),

    "agent_id": np.random.randint(
        1000,
        5000,
        NUM_POLICIES
    )
})

policies["end_date"] = pd.to_datetime(
    policies["start_date"]
) + pd.DateOffset(years=1)

policies.to_csv(
    os.path.join(folder, "policies.csv"),
    index=False
)

print("policies.csv created:", len(policies))


# --------------------------------------------------
# 3. CLAIMS
# --------------------------------------------------

print("\nCreating claims...")

claim_policy_ids = np.random.randint(
    1,
    NUM_POLICIES + 1,
    NUM_CLAIMS
)

claims = pd.DataFrame({
    "claim_id": range(1, NUM_CLAIMS + 1),

    "policy_id": claim_policy_ids,

    "claim_number": [
        f"CLM{100000 + i}"
        for i in range(NUM_CLAIMS)
    ],

    "claim_type": np.random.choice(
        [
            "Accident",
            "Theft",
            "Medical",
            "Fire",
            "Damage",
            "Natural Disaster"
        ],
        NUM_CLAIMS
    ),

    "claim_status": np.random.choice(
        [
            "Approved",
            "Pending",
            "Rejected",
            "Under Review",
            "Settled"
        ],
        NUM_CLAIMS
    ),

    "claim_amount": np.round(
        np.random.uniform(5000, 500000, NUM_CLAIMS),
        2
    ),

    "approved_amount": np.round(
        np.random.uniform(1000, 450000, NUM_CLAIMS),
        2
    ),

    "claim_date": [
        fake.date_between(
            start_date="-3y",
            end_date="today"
        )
        for _ in range(NUM_CLAIMS)
    ],

    "claim_location": np.random.choice(
        [
            "Bengaluru",
            "Mumbai",
            "Delhi",
            "Hyderabad",
            "Chennai",
            "Pune",
            "Kolkata"
        ],
        NUM_CLAIMS
    )
})

claims.to_csv(
    os.path.join(folder, "claims.csv"),
    index=False
)

print("claims.csv created:", len(claims))


# --------------------------------------------------
# 4. PAYMENTS
# --------------------------------------------------

print("\nCreating payments...")

payment_customer_ids = np.random.randint(
    1,
    NUM_CUSTOMERS + 1,
    NUM_PAYMENTS
)

payments = pd.DataFrame({
    "payment_id": range(1, NUM_PAYMENTS + 1),

    "customer_id": payment_customer_ids,

    "policy_id": np.random.randint(
        1,
        NUM_POLICIES + 1,
        NUM_PAYMENTS
    ),

    "payment_amount": np.round(
        np.random.uniform(1000, 100000, NUM_PAYMENTS),
        2
    ),

    "payment_method": np.random.choice(
        ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"],
        NUM_PAYMENTS
    ),

    "payment_status": np.random.choice(
        ["Successful", "Pending", "Failed", "Refunded"],
        NUM_PAYMENTS
    ),

    "payment_date": [
        fake.date_between(
            start_date="-3y",
            end_date="today"
        )
        for _ in range(NUM_PAYMENTS)
    ],

    "transaction_id": [
        f"TXN{10000000 + i}"
        for i in range(NUM_PAYMENTS)
    ]
})

payments.to_csv(
    os.path.join(folder, "payments.csv"),
    index=False
)

print("payments.csv created:", len(payments))


# --------------------------------------------------
# 5. REPAIRS
# --------------------------------------------------

print("\nCreating repairs...")

repairs = pd.DataFrame({
    "repair_id": range(1, NUM_REPAIRS + 1),

    "claim_id": np.random.randint(
        1,
        NUM_CLAIMS + 1,
        NUM_REPAIRS
    ),

    "repair_center": np.random.choice(
        [
            "Bengaluru Service Center",
            "Mumbai Service Center",
            "Delhi Service Center",
            "Hyderabad Service Center",
            "Chennai Service Center",
            "Pune Service Center"
        ],
        NUM_REPAIRS
    ),

    "repair_type": np.random.choice(
        [
            "Engine",
            "Body",
            "Electrical",
            "Glass",
            "Mechanical",
            "Other"
        ],
        NUM_REPAIRS
    ),

    "repair_cost": np.round(
        np.random.uniform(1000, 300000, NUM_REPAIRS),
        2
    ),

    "repair_status": np.random.choice(
        [
            "Completed",
            "In Progress",
            "Pending",
            "Cancelled"
        ],
        NUM_REPAIRS
    ),

    "repair_date": [
        fake.date_between(
            start_date="-3y",
            end_date="today"
        )
        for _ in range(NUM_REPAIRS)
    ],

    "estimated_days": np.random.randint(
        1,
        45,
        NUM_REPAIRS
    )
})

repairs.to_csv(
    os.path.join(folder, "repairs.csv"),
    index=False
)

print("repairs.csv created:", len(repairs))


# --------------------------------------------------
# 6. SUPPORT
# --------------------------------------------------

print("\nCreating support tickets...")

support = pd.DataFrame({
    "ticket_id": range(1, NUM_SUPPORT + 1),

    "customer_id": np.random.randint(
        1,
        NUM_CUSTOMERS + 1,
        NUM_SUPPORT
    ),

    "ticket_category": np.random.choice(
        [
            "Payment",
            "Policy",
            "Claim",
            "Renewal",
            "Account",
            "Technical",
            "Complaint"
        ],
        NUM_SUPPORT
    ),

    "priority": np.random.choice(
        ["Low", "Medium", "High", "Critical"],
        NUM_SUPPORT
    ),

    "ticket_status": np.random.choice(
        ["Open", "In Progress", "Resolved", "Closed"],
        NUM_SUPPORT
    ),

    "channel": np.random.choice(
        ["Phone", "Email", "Chat", "Website", "App"],
        NUM_SUPPORT
    ),

    "created_date": [
        fake.date_between(
            start_date="-2y",
            end_date="today"
        )
        for _ in range(NUM_SUPPORT)
    ],

    "resolution_days": np.random.randint(
        0,
        15,
        NUM_SUPPORT
    ),

    "satisfaction_score": np.random.randint(
        1,
        6,
        NUM_SUPPORT
    )
})

support.to_csv(
    os.path.join(folder, "support.csv"),
    index=False
)

print("support.csv created:", len(support))


# --------------------------------------------------
# FINAL MESSAGE
# --------------------------------------------------

print("\n" + "=" * 60)
print("RAW DATA GENERATION COMPLETED")
print("=" * 60)

print("Customers :", NUM_CUSTOMERS)
print("Policies  :", NUM_POLICIES)
print("Claims    :", NUM_CLAIMS)
print("Payments  :", NUM_PAYMENTS)
print("Repairs   :", NUM_REPAIRS)
print("Support   :", NUM_SUPPORT)

print("\nFiles saved to:")
print(folder)
