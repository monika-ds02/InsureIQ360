import sqlite3
from pathlib import Path

# Get the InsureIQ360 project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Database folder
DATABASE_DIR = BASE_DIR / "database"

# Create database folder if it doesn't exist
DATABASE_DIR.mkdir(exist_ok=True)

# Database file
DATABASE_FILE = DATABASE_DIR / "insureiq360.db"

# Connect to SQLite
connection = sqlite3.connect(DATABASE_FILE)

cursor = connection.cursor()

# Create Customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    phone TEXT,
    date_of_birth TEXT,
    gender TEXT,
    city TEXT,
    state TEXT,
    pincode TEXT,
    customer_segment TEXT,
    income REAL,
    occupation TEXT,
    registration_date TEXT
)
""")

# Create Policies table
cursor.execute("""
CREATE TABLE IF NOT EXISTS policies (
    policy_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    policy_number TEXT,
    policy_type TEXT,
    policy_status TEXT,
    premium REAL,
    coverage_amount REAL,
    start_date TEXT,
    end_date TEXT,
    payment_frequency TEXT,
    agent_id TEXT
)
""")

# Create Claims table
cursor.execute("""
CREATE TABLE IF NOT EXISTS claims (
    claim_id INTEGER PRIMARY KEY,
    policy_id INTEGER,
    claim_number TEXT,
    claim_type TEXT,
    claim_status TEXT,
    claim_amount REAL,
    approved_amount REAL,
    claim_date TEXT,
    claim_location TEXT
)
""")

# Create Payments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    policy_id INTEGER,
    payment_amount REAL,
    payment_method TEXT,
    payment_status TEXT,
    payment_date TEXT,
    transaction_id TEXT
)
""")

# Create Repairs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS repairs (
    repair_id INTEGER PRIMARY KEY,
    claim_id INTEGER,
    repair_center TEXT,
    repair_type TEXT,
    repair_cost REAL,
    repair_status TEXT,
    repair_date TEXT,
    estimated_days INTEGER
)
""")

# Create Support table
cursor.execute("""
CREATE TABLE IF NOT EXISTS support (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    ticket_category TEXT,
    priority TEXT,
    ticket_status TEXT,
    channel TEXT,
    created_date TEXT,
    resolution_days REAL,
    satisfaction_score REAL
)
""")

# Save changes
connection.commit()

# Check tables
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name
""")

tables = cursor.fetchall()

print("\n==========================================")
print("INSUREIQ 360 DATABASE CREATED")
print("==========================================")

print("\nDatabase:")
print(DATABASE_FILE)

print("\nTables:")

for table in tables:
    print(" -", table[0])

# Close connection
connection.close()

print("\n==========================================")
print("COMPLETED SUCCESSFULLY")
print("==========================================")

