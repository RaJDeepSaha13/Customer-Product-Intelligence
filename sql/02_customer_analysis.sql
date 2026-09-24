-- =========================================================
-- CUSTOMER & PRODUCT INTELLIGENCE
-- 02 - Customer Analysis
-- =========================================================

-- 1. Customer KPIs

SELECT
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (
        WHERE customer_id IN (
            SELECT DISTINCT customer_id
            FROM orders
        )
    ) AS customers_with_orders,
    COUNT(*) FILTER (
        WHERE customer_id NOT IN (
            SELECT DISTINCT customer_id
            FROM orders
        )
    ) AS customers_without_orders
FROM customers;

-- =========================================================
-- 2. Customer Purchase Frequency
-- =========================================================

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)

SELECT
    CASE
        WHEN order_count = 1 THEN 'One-time Customer'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Repeat Customer'
        ELSE 'High-frequency Customer'
    END AS customer_segment,

    COUNT(*) AS customers,

    SUM(order_count) AS total_orders,

    ROUND(AVG(order_count), 2) AS avg_orders_per_customer

FROM customer_orders

GROUP BY
    CASE
        WHEN order_count = 1 THEN 'One-time Customer'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Repeat Customer'
        ELSE 'High-frequency Customer'
    END

ORDER BY
    avg_orders_per_customer DESC;

    -- =========================================================
-- 3. Revenue & Profit by Customer Segment
-- =========================================================

WITH customer_summary AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count,
        SUM(total_revenue) AS revenue,
        SUM(total_profit) AS profit
    FROM orders
    GROUP BY customer_id
),

segmented_customers AS (
    SELECT
        customer_id,
        order_count,
        revenue,
        profit,
        CASE
            WHEN order_count = 1 THEN 'One-time Customer'
            WHEN order_count BETWEEN 2 AND 5 THEN 'Repeat Customer'
            ELSE 'High-frequency Customer'
        END AS customer_segment
    FROM customer_summary
)

SELECT
    customer_segment,
    COUNT(*) AS customers,
    SUM(order_count) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(revenue), 2) AS avg_revenue_per_customer,
    ROUND(AVG(profit), 2) AS avg_profit_per_customer
FROM segmented_customers
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- =========================================================
-- 4. Top 20 Customers by Revenue
-- =========================================================

SELECT
    c.customer_id,
    c.city,
    c.region,
    c.subscription_type,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_revenue), 2) AS total_revenue,
    ROUND(SUM(o.total_profit), 2) AS total_profit,
    ROUND(
        SUM(o.total_profit) /
        NULLIF(SUM(o.total_revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.city,
    c.region,
    c.subscription_type
ORDER BY total_revenue DESC
LIMIT 20;

-- =========================================================
-- 5. Subscription Type Performance
-- =========================================================

SELECT
    c.subscription_type,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.total_revenue), 2) AS total_revenue,
    ROUND(SUM(o.total_profit), 2) AS total_profit,
    ROUND(
        SUM(o.total_revenue) /
        NULLIF(COUNT(DISTINCT c.customer_id), 0),
        2
    ) AS revenue_per_customer,
    ROUND(
        SUM(o.total_profit) /
        NULLIF(COUNT(DISTINCT c.customer_id), 0),
        2
    ) AS profit_per_customer
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.subscription_type
ORDER BY total_revenue DESC;

-- =========================================================
-- 6. High-Value Non-Premium Customers
-- =========================================================

SELECT
    c.customer_id,
    c.subscription_type,
    c.city,
    c.region,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_revenue), 2) AS total_revenue,
    ROUND(SUM(o.total_profit), 2) AS total_profit
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE c.subscription_type IN ('Free', 'Basic')
GROUP BY
    c.customer_id,
    c.subscription_type,
    c.city,
    c.region
HAVING
    SUM(o.total_revenue) > 50000
ORDER BY total_revenue DESC
LIMIT 20;

-- =========================================================
-- 7. Customer Recency
-- =========================================================

WITH customer_recency AS (
    SELECT
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_revenue) AS total_revenue,
        SUM(total_profit) AS total_profit
    FROM orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    last_order_date,
    CURRENT_DATE - last_order_date::date AS days_since_last_order,
    total_orders,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit
FROM customer_recency
ORDER BY days_since_last_order DESC
LIMIT 20;

-- =========================================================
-- 8. Customer Recency - Fixed Analysis Date
-- =========================================================

WITH customer_recency AS (
    SELECT
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_revenue) AS total_revenue,
        SUM(total_profit) AS total_profit
    FROM orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    last_order_date,
    DATE '2026-01-01' - last_order_date::date
        AS days_since_last_order,
    total_orders,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit
FROM customer_recency
ORDER BY days_since_last_order DESC
LIMIT 20;

-- =========================================================
-- 9. RFM Customer Segmentation
-- =========================================================

WITH customer_rfm AS (
    SELECT
        customer_id,

        DATE '2026-01-01'
            - MAX(order_date)::date AS recency_days,

        COUNT(DISTINCT order_id) AS frequency,

        SUM(total_revenue) AS monetary_value

    FROM orders

    GROUP BY customer_id
),

rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_value,

        NTILE(5) OVER (
            ORDER BY recency_days DESC
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary_value
        ) AS monetary_score

    FROM customer_rfm
)

SELECT
    customer_id,
    recency_days,
    frequency,
    ROUND(monetary_value, 2) AS monetary_value,

    recency_score,
    frequency_score,
    monetary_score,

    CASE
        WHEN recency_score >= 4
             AND frequency_score >= 4
             AND monetary_score >= 4
            THEN 'Champions'

        WHEN recency_score >= 3
             AND frequency_score >= 3
             AND monetary_score >= 3
            THEN 'Loyal Customers'

        WHEN recency_score <= 2
             AND frequency_score >= 3
             AND monetary_score >= 3
            THEN 'At Risk High Value'

        WHEN recency_score <= 2
             AND frequency_score <= 2
             AND monetary_score <= 2
            THEN 'Dormant / Low Value'

        ELSE 'Potential / Developing'

    END AS customer_segment

FROM rfm_scores
ORDER BY monetary_value DESC;

-- =========================================================
-- 10. RFM Segment Summary
-- =========================================================

WITH customer_rfm AS (
    SELECT
        customer_id,

        DATE '2026-01-01'
            - MAX(order_date)::date AS recency_days,

        COUNT(DISTINCT order_id) AS frequency,

        SUM(total_revenue) AS monetary_value,

        SUM(total_profit) AS profit

    FROM orders

    GROUP BY customer_id
),

rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary_value,
        profit,

        NTILE(5) OVER (
            ORDER BY recency_days DESC
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary_value
        ) AS monetary_score

    FROM customer_rfm
),

segmented AS (
    SELECT
        *,
        CASE
            WHEN recency_score >= 4
                 AND frequency_score >= 4
                 AND monetary_score >= 4
                THEN 'Champions'

            WHEN recency_score >= 3
                 AND frequency_score >= 3
                 AND monetary_score >= 3
                THEN 'Loyal Customers'

            WHEN recency_score <= 2
                 AND frequency_score >= 3
                 AND monetary_score >= 3
                THEN 'At Risk High Value'

            WHEN recency_score <= 2
                 AND frequency_score <= 2
                 AND monetary_score <= 2
                THEN 'Dormant / Low Value'

            ELSE 'Potential / Developing'
        END AS customer_segment

    FROM rfm_scores
)

SELECT
    customer_segment,
    COUNT(*) AS customers,
    SUM(frequency) AS total_orders,
    ROUND(SUM(monetary_value), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(monetary_value), 2) AS avg_customer_revenue,
    ROUND(AVG(profit), 2) AS avg_customer_profit

FROM segmented

GROUP BY customer_segment

ORDER BY total_revenue DESC;

-- =========================================================
-- 11. Customer Churn Risk
-- =========================================================

WITH customer_activity AS (
    SELECT
        customer_id,
        MAX(order_date)::date AS last_order_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_revenue) AS total_revenue,
        SUM(total_profit) AS total_profit
    FROM orders
    GROUP BY customer_id
),

churn_classification AS (
    SELECT
        *,
        DATE '2026-01-01' - last_order_date AS days_since_last_order,

        CASE
            WHEN DATE '2026-01-01' - last_order_date <= 30
                THEN 'Active'

            WHEN DATE '2026-01-01' - last_order_date <= 90
                THEN 'At Risk'

            WHEN DATE '2026-01-01' - last_order_date <= 180
                THEN 'Churn Risk'

            ELSE 'Dormant'
        END AS churn_status

    FROM customer_activity
)

SELECT
    churn_status,
    COUNT(*) AS customers,
    SUM(total_orders) AS total_orders,
    ROUND(SUM(total_revenue), 2) AS historical_revenue,
    ROUND(SUM(total_profit), 2) AS historical_profit,
    ROUND(
        COUNT(*)::numeric /
        SUM(COUNT(*)) OVER () * 100,
        2
    ) AS customer_percentage

FROM churn_classification

GROUP BY churn_status

ORDER BY
    CASE churn_status
        WHEN 'Active' THEN 1
        WHEN 'At Risk' THEN 2
        WHEN 'Churn Risk' THEN 3
        WHEN 'Dormant' THEN 4
    END;

-- =========================================================
-- 12. High-Value At-Risk Customers
-- =========================================================

WITH customer_activity AS (
    SELECT
        customer_id,
        MAX(order_date)::date AS last_order_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_revenue) AS total_revenue,
        SUM(total_profit) AS total_profit
    FROM orders
    GROUP BY customer_id
),

at_risk_customers AS (
    SELECT
        *,
        DATE '2026-01-01' - last_order_date AS days_since_last_order
    FROM customer_activity
    WHERE DATE '2026-01-01' - last_order_date BETWEEN 31 AND 90
)

SELECT
    a.customer_id,
    c.subscription_type,
    c.city,
    c.region,
    a.days_since_last_order,
    a.total_orders,
    ROUND(a.total_revenue, 2) AS historical_revenue,
    ROUND(a.total_profit, 2) AS historical_profit
FROM at_risk_customers a
JOIN customers c
    ON a.customer_id = c.customer_id
ORDER BY a.total_revenue DESC
LIMIT 20;

-- =========================================================
-- KEY BUSINESS FINDINGS
-- =========================================================
--
-- 1. High-frequency customers represented approximately
--    44.7% of purchasing customers but contributed roughly
--    66% of total revenue and profit.
--
-- 2. Premium customers generated the highest revenue and
--    profit per customer, despite having a smaller customer
--    base than Free and Basic customers.
--
-- 3. Several Free and Basic customers demonstrated
--    high-value purchasing behavior, creating potential
--    Premium upgrade opportunities.
--
-- 4. RFM analysis identified 1,703 Champions and 1,975
--    Loyal Customers as high-value customer segments.
--
-- 5. 1,221 customers were classified as At Risk High Value,
--    representing approximately 33.7M in historical revenue
--    and 16.6M in historical profit.
--
-- 6. 3,669 customers were classified as At Risk based on
--    31-90 days of purchase inactivity.
--
-- 7. At-Risk customers represented approximately 37% of the
--    purchasing customer base and 78.5M in historical revenue.
--
-- 8. High-value at-risk customers should be prioritized
--    for targeted retention campaigns.
