
-- ============================================================
-- INSUREIQ 360
-- SQL ANALYSIS
-- Database: SQLite
-- ============================================================


-- ============================================================
-- 1. TOTAL CUSTOMERS
-- ============================================================

SELECT
    COUNT(*) AS total_customers
FROM customers;


-- ============================================================
-- 2. CUSTOMERS BY SEGMENT
-- ============================================================

SELECT
    customer_segment,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_segment
ORDER BY customer_count DESC;


-- ============================================================
-- 3. CUSTOMERS BY CITY
-- ============================================================

SELECT
    city,
    COUNT(*) AS customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC;


-- ============================================================
-- 4. CUSTOMERS BY STATE
-- ============================================================

SELECT
    state,
    COUNT(*) AS customer_count
FROM customers
GROUP BY state
ORDER BY customer_count DESC;


-- ============================================================
-- 5. TOTAL POLICIES
-- ============================================================

SELECT
    COUNT(*) AS total_policies
FROM policies;


-- ============================================================
-- 6. POLICIES BY TYPE
-- ============================================================

SELECT
    policy_type,
    COUNT(*) AS policy_count
FROM policies
GROUP BY policy_type
ORDER BY policy_count DESC;


-- ============================================================
-- 7. POLICIES BY STATUS
-- ============================================================

SELECT
    policy_status,
    COUNT(*) AS policy_count
FROM policies
GROUP BY policy_status
ORDER BY policy_count DESC;


-- ============================================================
-- 8. PREMIUM SUMMARY
-- ============================================================

SELECT
    ROUND(SUM(premium), 2) AS total_premium,
    ROUND(AVG(premium), 2) AS average_premium,
    ROUND(MIN(premium), 2) AS minimum_premium,
    ROUND(MAX(premium), 2) AS maximum_premium
FROM policies;


-- ============================================================
-- 9. PREMIUM BY POLICY TYPE
-- ============================================================

SELECT
    policy_type,
    COUNT(*) AS policy_count,
    ROUND(SUM(premium), 2) AS total_premium,
    ROUND(AVG(premium), 2) AS average_premium
FROM policies
GROUP BY policy_type
ORDER BY total_premium DESC;


-- ============================================================
-- 10. TOTAL CLAIMS
-- ============================================================

SELECT
    COUNT(*) AS total_claims
FROM claims;


-- ============================================================
-- 11. CLAIMS BY STATUS
-- ============================================================

SELECT
    claim_status,
    COUNT(*) AS claim_count
FROM claims
GROUP BY claim_status
ORDER BY claim_count DESC;


-- ============================================================
-- 12. CLAIM AMOUNT SUMMARY
-- ============================================================

SELECT
    ROUND(SUM(claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(claim_amount), 2) AS average_claim_amount,
    ROUND(MIN(claim_amount), 2) AS minimum_claim_amount,
    ROUND(MAX(claim_amount), 2) AS maximum_claim_amount
FROM claims;


-- ============================================================
-- 13. CLAIMS BY TYPE
-- ============================================================

SELECT
    claim_type,
    COUNT(*) AS claim_count,
    ROUND(SUM(claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(claim_amount), 2) AS average_claim_amount
FROM claims
GROUP BY claim_type
ORDER BY total_claim_amount DESC;


-- ============================================================
-- 14. CLAIMS BY POLICY TYPE
-- ============================================================

SELECT
    p.policy_type,
    COUNT(c.claim_id) AS claim_count,
    ROUND(SUM(c.claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(c.claim_amount), 2) AS average_claim_amount
FROM policies p
JOIN claims c
    ON p.policy_id = c.policy_id
GROUP BY p.policy_type
ORDER BY total_claim_amount DESC;


-- ============================================================
-- 15. CLAIMS BY CUSTOMER SEGMENT
-- ============================================================

SELECT
    cu.customer_segment,
    COUNT(c.claim_id) AS claim_count,
    ROUND(SUM(c.claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(c.claim_amount), 2) AS average_claim_amount
FROM customers cu
JOIN policies p
    ON cu.customer_id = p.customer_id
JOIN claims c
    ON p.policy_id = c.policy_id
GROUP BY cu.customer_segment
ORDER BY total_claim_amount DESC;


-- ============================================================
-- 16. CLAIMS BY CITY
-- ============================================================

SELECT
    cu.city,
    COUNT(c.claim_id) AS claim_count,
    ROUND(SUM(c.claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(c.claim_amount), 2) AS average_claim_amount
FROM customers cu
JOIN policies p
    ON cu.customer_id = p.customer_id
JOIN claims c
    ON p.policy_id = c.policy_id
GROUP BY cu.city
ORDER BY total_claim_amount DESC;


-- ============================================================
-- 17. CLAIM APPROVAL RATE
-- ============================================================

SELECT
    COUNT(*) AS total_claims,

    SUM(
        CASE
            WHEN claim_status = 'Approved'
            THEN 1
            ELSE 0
        END
    ) AS approved_claims,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN claim_status = 'Approved'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS approval_rate
FROM claims;


-- ============================================================
-- 18. APPROVED CLAIM AMOUNT
-- ============================================================

SELECT
    ROUND(SUM(approved_amount), 2) AS total_approved_amount,
    ROUND(AVG(approved_amount), 2) AS average_approved_amount
FROM claims
WHERE claim_status = 'Approved';


-- ============================================================
-- 19. HIGH VALUE CLAIMS
-- ============================================================

SELECT
    claim_id,
    policy_id,
    claim_type,
    claim_status,
    claim_amount,
    approved_amount
FROM claims
WHERE claim_amount >= 250000
ORDER BY claim_amount DESC;


-- ============================================================
-- 20. PAYMENT STATUS ANALYSIS
-- ============================================================

SELECT
    payment_status,
    COUNT(*) AS payment_count,
    ROUND(SUM(payment_amount), 2) AS total_payment_amount,
    ROUND(AVG(payment_amount), 2) AS average_payment_amount
FROM payments
GROUP BY payment_status
ORDER BY total_payment_amount DESC;


-- ============================================================
-- 21. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    payment_method,
    COUNT(*) AS payment_count,
    ROUND(SUM(payment_amount), 2) AS total_payment_amount,
    ROUND(AVG(payment_amount), 2) AS average_payment_amount
FROM payments
GROUP BY payment_method
ORDER BY total_payment_amount DESC;


-- ============================================================
-- 22. PAYMENT SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_payments,
    ROUND(SUM(payment_amount), 2) AS total_payment_amount,
    ROUND(AVG(payment_amount), 2) AS average_payment,
    ROUND(MIN(payment_amount), 2) AS minimum_payment,
    ROUND(MAX(payment_amount), 2) AS maximum_payment
FROM payments;


-- ============================================================
-- 23. REPAIR STATUS ANALYSIS
-- ============================================================

SELECT
    repair_status,
    COUNT(*) AS repair_count,
    ROUND(SUM(repair_cost), 2) AS total_repair_cost,
    ROUND(AVG(repair_cost), 2) AS average_repair_cost
FROM repairs
GROUP BY repair_status
ORDER BY total_repair_cost DESC;


-- ============================================================
-- 24. REPAIR TYPE ANALYSIS
-- ============================================================

SELECT
    repair_type,
    COUNT(*) AS repair_count,
    ROUND(SUM(repair_cost), 2) AS total_repair_cost,
    ROUND(AVG(repair_cost), 2) AS average_repair_cost
FROM repairs
GROUP BY repair_type
ORDER BY total_repair_cost DESC;


-- ============================================================
-- 25. SUPPORT TICKET CATEGORY
-- ============================================================

SELECT
    ticket_category,
    COUNT(*) AS ticket_count
FROM support
GROUP BY ticket_category
ORDER BY ticket_count DESC;


-- ============================================================
-- 26. SUPPORT STATUS
-- ============================================================

SELECT
    ticket_status,
    COUNT(*) AS ticket_count
FROM support
GROUP BY ticket_status
ORDER BY ticket_count DESC;


-- ============================================================
-- 27. SUPPORT CHANNEL
-- ============================================================

SELECT
    channel,
    COUNT(*) AS ticket_count,
    ROUND(AVG(resolution_days), 2) AS average_resolution_days
FROM support
GROUP BY channel
ORDER BY ticket_count DESC;


-- ============================================================
-- 28. CUSTOMER SATISFACTION
-- ============================================================

SELECT
    satisfaction_score,
    COUNT(*) AS ticket_count
FROM support
GROUP BY satisfaction_score
ORDER BY satisfaction_score;


-- ============================================================
-- 29. AVERAGE SUPPORT RESOLUTION TIME
-- ============================================================

SELECT
    ROUND(AVG(resolution_days), 2)
        AS average_resolution_days
FROM support;


-- ============================================================
-- 30. CLAIM FREQUENCY
-- ============================================================

SELECT
    ROUND(
        CAST(COUNT(c.claim_id) AS REAL)
        / NULLIF(COUNT(DISTINCT p.policy_id), 0),
        4
    ) AS claim_frequency
FROM policies p
LEFT JOIN claims c
    ON p.policy_id = c.policy_id;


-- ============================================================
-- 31. CLAIM SEVERITY
-- ============================================================

SELECT
    ROUND(AVG(claim_amount), 2)
        AS claim_severity
FROM claims;


-- ============================================================
-- 32. LOSS RATIO
-- ============================================================

SELECT
    ROUND(
        SUM(c.claim_amount) * 100.0
        / NULLIF(SUM(p.premium), 0),
        2
    ) AS loss_ratio_percentage
FROM claims c
JOIN policies p
    ON c.policy_id = p.policy_id;


-- ============================================================
-- 33. LOSS RATIO BY POLICY TYPE
-- ============================================================

SELECT
    p.policy_type,

    ROUND(SUM(p.premium), 2)
        AS total_premium,

    ROUND(SUM(c.claim_amount), 2)
        AS total_claim_amount,

    ROUND(
        SUM(c.claim_amount) * 100.0
        / NULLIF(SUM(p.premium), 0),
        2
    ) AS loss_ratio_percentage

FROM policies p

LEFT JOIN claims c
    ON p.policy_id = c.policy_id

GROUP BY p.policy_type

ORDER BY loss_ratio_percentage DESC;


-- ============================================================
-- 34. PRODUCT PROFITABILITY
-- ============================================================

SELECT
    p.policy_type,

    ROUND(SUM(p.premium), 2)
        AS total_premium,

    ROUND(
        COALESCE(SUM(c.claim_amount), 0),
        2
    ) AS total_claim_amount,

    ROUND(
        SUM(p.premium)
        - COALESCE(SUM(c.claim_amount), 0),
        2
    ) AS estimated_profit

FROM policies p

LEFT JOIN claims c
    ON p.policy_id = c.policy_id

GROUP BY p.policy_type

ORDER BY estimated_profit DESC;


-- ============================================================
-- 35. CUSTOMER POLICY COUNT
-- ============================================================

SELECT
    cu.customer_id,
    cu.customer_name,
    cu.customer_segment,

    COUNT(p.policy_id) AS policy_count,

    ROUND(
        SUM(p.premium),
        2
    ) AS total_premium

FROM customers cu

LEFT JOIN policies p
    ON cu.customer_id = p.customer_id

GROUP BY
    cu.customer_id,
    cu.customer_name,
    cu.customer_segment

ORDER BY total_premium DESC;


-- ============================================================
-- 36. CUSTOMER CLAIM SUMMARY
-- ============================================================

SELECT
    cu.customer_id,
    cu.customer_name,

    COUNT(c.claim_id) AS claim_count,

    ROUND(
        COALESCE(SUM(c.claim_amount), 0),
        2
    ) AS total_claim_amount,

    ROUND(
        COALESCE(AVG(c.claim_amount), 0),
        2
    ) AS average_claim_amount

FROM customers cu

LEFT JOIN policies p
    ON cu.customer_id = p.customer_id

LEFT JOIN claims c
    ON p.policy_id = c.policy_id

GROUP BY
    cu.customer_id,
    cu.customer_name

ORDER BY total_claim_amount DESC;


-- ============================================================
-- 37. PRODUCT CLAIM ANALYSIS
-- ============================================================

SELECT
    p.policy_type,
    c.claim_type,

    COUNT(c.claim_id) AS claim_count,

    ROUND(
        SUM(c.claim_amount),
        2
    ) AS total_claim_amount,

    ROUND(
        AVG(c.claim_amount),
        2
    ) AS average_claim_amount

FROM policies p

JOIN claims c
    ON p.policy_id = c.policy_id

GROUP BY
    p.policy_type,
    c.claim_type

ORDER BY
    p.policy_type,
    total_claim_amount DESC;


-- ============================================================
-- 38. SEGMENT VS PRODUCT
-- ============================================================

SELECT
    cu.customer_segment,
    p.policy_type,

    COUNT(p.policy_id) AS policy_count,

    ROUND(
        SUM(p.premium),
        2
    ) AS total_premium,

    ROUND(
        AVG(p.premium),
        2
    ) AS average_premium

FROM customers cu

JOIN policies p
    ON cu.customer_id = p.customer_id

GROUP BY
    cu.customer_segment,
    p.policy_type

ORDER BY
    cu.customer_segment,
    policy_count DESC;


-- ============================================================
-- 39. CITY VS PRODUCT
-- ============================================================

SELECT
    cu.city,
    p.policy_type,

    COUNT(p.policy_id) AS policy_count,

    ROUND(
        SUM(p.premium),
        2
    ) AS total_premium

FROM customers cu

JOIN policies p
    ON cu.customer_id = p.customer_id

GROUP BY
    cu.city,
    p.policy_type

ORDER BY
    cu.city,
    total_premium DESC;


-- ============================================================
-- 40. EXECUTIVE KPI SUMMARY
-- ============================================================

SELECT

    (SELECT COUNT(*)
     FROM customers)
        AS total_customers,

    (SELECT COUNT(*)
     FROM policies)
        AS total_policies,

    (SELECT ROUND(SUM(premium), 2)
     FROM policies)
        AS total_premium,

    (SELECT COUNT(*)
     FROM claims)
        AS total_claims,

    (SELECT ROUND(SUM(claim_amount), 2)
     FROM claims)
        AS total_claim_amount,

    (SELECT ROUND(AVG(claim_amount), 2)
     FROM claims)
        AS average_claim_severity,

    (SELECT COUNT(*)
     FROM payments)
        AS total_payments,

    (SELECT ROUND(SUM(payment_amount), 2)
     FROM payments)
        AS total_payment_amount,

    (SELECT COUNT(*)
     FROM repairs)
        AS total_repairs,

    (SELECT ROUND(SUM(repair_cost), 2)
     FROM repairs)
        AS total_repair_cost,

    (SELECT COUNT(*)
     FROM support)
        AS total_support_tickets,

    (SELECT ROUND(AVG(resolution_days), 2)
     FROM support)
        AS average_resolution_days,

    (SELECT ROUND(AVG(satisfaction_score), 2)
     FROM support)
        AS average_satisfaction_score;

