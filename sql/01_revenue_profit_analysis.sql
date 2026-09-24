-- =========================================================
-- CUSTOMER & PRODUCT INTELLIGENCE
-- 01 - Revenue & Profit Analysis
-- =========================================================

-- 1. Overall Business KPIs

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(total_revenue) AS total_revenue,
    SUM(total_profit) AS total_profit,
    ROUND(AVG(total_revenue), 2) AS average_order_value,
    ROUND(
        SUM(total_profit) / NULLIF(SUM(total_revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM orders; 

-- 2. Monthly Revenue & Profit

SELECT
    DATE_TRUNC('month', order_date)::date AS month,
    COUNT(DISTINCT order_id) AS orders,
    SUM(total_revenue) AS revenue,
    SUM(total_profit) AS profit,
    ROUND(
        SUM(total_profit) / NULLIF(SUM(total_revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;

-- 3. Regional Performance

SELECT
    c.region,
    COUNT(DISTINCT o.order_id) AS orders,
    COUNT(DISTINCT o.customer_id) AS customers,
    SUM(o.total_revenue) AS revenue,
    SUM(o.total_profit) AS profit,
    ROUND(
        SUM(o.total_profit) /
        NULLIF(SUM(o.total_revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.region
ORDER BY revenue DESC;

-- 4. Product Performance

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.revenue) AS revenue,
    SUM(oi.profit) AS profit,
    ROUND(
        SUM(oi.profit) /
        NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC;

-- 5. Loss-Making Products

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.revenue) AS revenue,
    SUM(oi.profit) AS profit
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
HAVING SUM(oi.profit) < 0
ORDER BY profit ASC;

-- =========================================================
-- 6. Category Performance
-- =========================================================

SELECT
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.revenue), 2) AS revenue,
    ROUND(SUM(oi.profit), 2) AS profit,
    ROUND(
        SUM(oi.profit) /
        NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- =========================================================
-- 7. Discount vs Profitability
-- =========================================================

SELECT
    p.category,
    ROUND(AVG(oi.discount), 2) AS avg_discount,
    ROUND(SUM(oi.revenue), 2) AS revenue,
    ROUND(SUM(oi.profit), 2) AS profit,
    ROUND(
        SUM(oi.profit) /
        NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY avg_discount DESC;

-- =========================================================
-- 8. Lowest-Margin Products
-- =========================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.revenue), 2) AS revenue,
    ROUND(SUM(oi.profit), 2) AS profit,
    ROUND(
        SUM(oi.profit) /
        NULLIF(SUM(oi.revenue), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
HAVING SUM(oi.revenue) > 0
ORDER BY profit_margin_percentage ASC
LIMIT 10;

-- =========================================================
-- 9. Loss-Making Products
-- =========================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(*) AS loss_making_items,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.revenue), 2) AS revenue,
    ROUND(SUM(oi.profit), 2) AS total_loss
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
WHERE oi.profit < 0
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_loss ASC
LIMIT 10;

-- =========================================================
-- 10. Loss-Making Transactions and Discount Impact
-- =========================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(*) AS loss_making_items,
    ROUND(AVG(oi.discount), 2) AS avg_discount,
    ROUND(AVG(oi.unit_price), 2) AS avg_unit_price,
    ROUND(SUM(oi.revenue), 2) AS revenue,
    ROUND(SUM(oi.profit), 2) AS total_loss
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
WHERE oi.profit < 0
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_loss ASC
LIMIT 10;

-- =========================================================
-- 11. Profitability Comparison by Product
-- =========================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,

    COUNT(*) AS total_items,

    COUNT(*) FILTER (WHERE oi.profit < 0)
        AS loss_making_items,

    COUNT(*) FILTER (WHERE oi.profit >= 0)
        AS profitable_items,

    ROUND(AVG(oi.discount), 2)
        AS overall_avg_discount,

    ROUND(
        AVG(oi.discount) FILTER (WHERE oi.profit < 0),
        2
    ) AS loss_avg_discount,

    ROUND(
        AVG(oi.discount) FILTER (WHERE oi.profit >= 0),
        2
    ) AS profitable_avg_discount,

    ROUND(AVG(oi.profit), 2)
        AS avg_profit_per_item

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category

HAVING COUNT(*) FILTER (WHERE oi.profit < 0) > 0

ORDER BY loss_making_items DESC;

-- =========================================================
-- 12. Discount Threshold Analysis
-- =========================================================

SELECT
    CASE
        WHEN discount < 25 THEN '0-24'
        WHEN discount < 50 THEN '25-49'
        WHEN discount < 75 THEN '50-74'
        WHEN discount < 100 THEN '75-99'
        WHEN discount < 125 THEN '100-124'
        ELSE '125+'
    END AS discount_band,

    COUNT(*) AS total_items,

    COUNT(*) FILTER (WHERE profit < 0)
        AS loss_making_items,

    ROUND(
        COUNT(*) FILTER (WHERE profit < 0)::numeric
        / COUNT(*) * 100,
        2
    ) AS loss_rate_percentage,

    ROUND(SUM(revenue), 2) AS revenue,

    ROUND(SUM(profit), 2) AS profit

FROM order_items

GROUP BY
    CASE
        WHEN discount < 25 THEN '0-24'
        WHEN discount < 50 THEN '25-49'
        WHEN discount < 75 THEN '50-74'
        WHEN discount < 100 THEN '75-99'
        WHEN discount < 125 THEN '100-124'
        ELSE '125+'
    END

ORDER BY MIN(discount);

-- =========================================================
-- KEY BUSINESS FINDINGS
-- =========================================================
--
-- 1. The business generated 203.9M in revenue and
--    99.5M in profit across 55,000 orders.
--
-- 2. Profit margin remained relatively stable throughout
--    2025 at approximately 48.5%-49.0%.
--
-- 3. West generated the highest revenue and total profit,
--    while South had the highest profit margin.
--
-- 4. Fashion generated the highest category revenue and
--    profit, while Beauty had the lowest category margin.
--
-- 5. Several products showed recurring loss-making
--    transactions.
--
-- 6. Loss-making transactions showed substantially higher
--    average discounts than profitable transactions.
--
-- 7. Discounts of 125+ had a 4.59% observed loss rate,
--    compared with 0% for discounts below 75.
--
-- 8. Deep discounting should be investigated as a potential
--    profitability risk and controlled through product-level
--    discount guardrails.