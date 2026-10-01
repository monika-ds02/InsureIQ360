import duckdb

DB_PATH = "dbt_insureiq360/dev.duckdb"


def run_quality_checks():

    try:
        con = duckdb.connect(DB_PATH)

        print("=" * 55)
        print(" INSUREIQ360 DATA QUALITY REPORT ")
        print("=" * 55)


        # Check tables
        tables = [
            "fact_claims",
            "customers",
            "policies"
        ]

        existing_tables = [
            row[0]
            for row in con.execute("SHOW TABLES").fetchall()
        ]

        for table in tables:
            if table not in existing_tables:
                print(f"Missing table: {table}")
                con.close()
                return


        # Total claims
        total_claims = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
        """).fetchone()[0]

        print("\nTotal Claims:", total_claims)


        # Duplicate claim IDs
        print("\n--- Duplicate Claim IDs ---")

        duplicate_claims = con.execute("""
            SELECT
                claim_id,
                COUNT(*) AS count
            FROM fact_claims
            GROUP BY claim_id
            HAVING COUNT(*) > 1
        """).fetchall()

        if duplicate_claims:
            print(duplicate_claims)
        else:
            print("No duplicate claims found")


        # Missing customer IDs
        print("\n--- Missing Customer IDs ---")

        missing_customer = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
            WHERE customer_id IS NULL
            OR TRIM(customer_id) = ''
        """).fetchone()[0]

        print("Missing customer IDs:", missing_customer)


        # Missing policy IDs
        print("\n--- Missing Policy IDs ---")

        missing_policy = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
            WHERE policy_id IS NULL
            OR TRIM(policy_id) = ''
        """).fetchone()[0]

        print("Missing policy IDs:", missing_policy)


        # Invalid amounts
        print("\n--- Invalid Claim Amounts ---")

        invalid_amounts = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims
            WHERE claim_amount IS NULL
            OR claim_amount < 0
        """).fetchone()[0]

        print("Invalid claim amounts:", invalid_amounts)


        # Status check
        print("\n--- Claim Status Values ---")

        statuses = con.execute("""
            SELECT DISTINCT status
            FROM fact_claims
            ORDER BY status
        """).fetchall()

        print(statuses)


        # Invalid customer references
        print("\n--- Invalid Customer References ---")

        invalid_customers = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims c
            LEFT JOIN customers cu
            ON c.customer_id = cu.customer_id
            WHERE c.customer_id IS NOT NULL
            AND cu.customer_id IS NULL
        """).fetchone()[0]

        print(
            "Claims with invalid customers:",
            invalid_customers
        )


        # Invalid policy references
        print("\n--- Invalid Policy References ---")

        invalid_policies = con.execute("""
            SELECT COUNT(*)
            FROM fact_claims c
            LEFT JOIN policies p
            ON c.policy_id = p.policy_id
            WHERE c.policy_id IS NOT NULL
            AND p.policy_id IS NULL
        """).fetchone()[0]

        print(
            "Claims with invalid policies:",
            invalid_policies
        )


        # Customer count
        print("\n--- Master Data Counts ---")

        customer_count = con.execute("""
            SELECT COUNT(*)
            FROM customers
        """).fetchone()[0]

        policy_count = con.execute("""
            SELECT COUNT(*)
            FROM policies
        """).fetchone()[0]

        print("Customers:", customer_count)
        print("Policies:", policy_count)


        con.close()


        print("\n" + "=" * 55)
        print(" QUALITY CHECK COMPLETED SUCCESSFULLY ")
        print("=" * 55)


    except Exception as e:
        print("\nERROR:", e)


if __name__ == "__main__":
    run_quality_checks()