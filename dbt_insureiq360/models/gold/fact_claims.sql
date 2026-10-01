{{ config(materialized='table') }}

SELECT
    claim_id,
    customer_id,
    policy_id,
    claim_amount,
    status
FROM {{ ref('stg_claims') }}