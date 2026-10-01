{{ config(materialized='view') }}

SELECT
    claim_id,
    customer_id,
    policy_id,
    CAST(claim_amount AS DOUBLE) AS claim_amount,
    status
FROM sqlite_scan(
    '../data/bronze/insureIQ360_bronze.db',
    'bronze_claims'
)