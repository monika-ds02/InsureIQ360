import pandas as pd
import os

# --------------------------------------------------
# FOLDERS
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

BRONZE_FOLDER = os.path.join(BASE_DIR, "bronze")
SILVER_FOLDER = os.path.join(BASE_DIR, "silver")

# Create silver folder if it doesn't exist
os.makedirs(SILVER_FOLDER, exist_ok=True)

print("Bronze folder:", BRONZE_FOLDER)
print("Silver folder:", SILVER_FOLDER)


# --------------------------------------------------
# CLEANING FUNCTION
# --------------------------------------------------

def clean_data(filename):

    print("\n" + "=" * 60)
    print("Cleaning:", filename)
    print("=" * 60)

    bronze_path = os.path.join(BRONZE_FOLDER, filename)

    # Read raw data
    df = pd.read_csv(bronze_path)

    print("Original rows:", len(df))
    print("Original columns:", len(df.columns))

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Remove leading/trailing spaces from text columns
    text_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    # Convert empty strings to missing values
    df = df.replace("", pd.NA)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Convert date columns
    for column in df.columns:

        if "date" in column.lower():

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    # Save cleaned data
    output_filename = filename.replace(
        ".csv",
        "_cleaned.csv"
    )

    silver_path = os.path.join(
        SILVER_FOLDER,
        output_filename
    )

    df.to_csv(
        silver_path,
        index=False
    )

    print("Cleaned rows:", len(df))
    print("Saved:", silver_path)


# --------------------------------------------------
# FILES TO CLEAN
# --------------------------------------------------

files = [
    "customers.csv",
    "policies.csv",
    "claims.csv",
    "payments.csv",
    "repairs.csv",
    "support.csv"
]


# --------------------------------------------------
# RUN CLEANING
# --------------------------------------------------

for file in files:
    clean_data(file)


print("\n" + "=" * 60)
print("SILVER / CLEANED DATA CREATED SUCCESSFULLY")
print("=" * 60)