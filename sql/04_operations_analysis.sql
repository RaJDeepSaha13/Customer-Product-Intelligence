-- =========================================================
-- 01. Overall Delivery Performance
-- =========================================================

SELECT
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'On Time'
    ) AS on_time_deliveries,

    COUNT(*) FILTER (
        WHERE delivery_status = 'Late'
    ) AS late_deliveries,

    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,

    ROUND(
        COUNT(*) FILTER (
            WHERE delivery_status = 'Late'
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS late_delivery_percentage

FROM operations;

-- =========================================================
-- 02. Delivery Performance by Region
-- =========================================================

SELECT
    c.region,

    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE o.delivery_status = 'On Time'
    ) AS on_time_deliveries,

    COUNT(*) FILTER (
        WHERE o.delivery_status = 'Late'
    ) AS late_deliveries,

    ROUND(AVG(o.delivery_days), 2) AS avg_delivery_days,

    ROUND(
        COUNT(*) FILTER (
            WHERE o.delivery_status = 'Late'
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS late_delivery_percentage

FROM operations o

JOIN orders ord
    ON o.order_id = ord.order_id

JOIN customers c
    ON ord.customer_id = c.customer_id

GROUP BY c.region

ORDER BY late_delivery_percentage DESC;

-- =========================================================
-- 03. Delivery Status vs Returns & Cancellations
-- =========================================================

SELECT
    o.delivery_status,

    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE o.return_flag = 1
    ) AS returned_orders,

    COUNT(*) FILTER (
        WHERE o.cancellation_flag = 1
    ) AS cancelled_orders,

    ROUND(
        COUNT(*) FILTER (
            WHERE o.return_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS return_rate_percentage,

    ROUND(
        COUNT(*) FILTER (
            WHERE o.cancellation_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS cancellation_rate_percentage

FROM operations o

GROUP BY o.delivery_status

ORDER BY o.delivery_status;

-- =========================================================
-- 04. Return Reasons
-- =========================================================

SELECT
    return_reason,
    COUNT(*) AS returned_orders,
    ROUND(
        COUNT(*)::numeric
        / SUM(COUNT(*)) OVER () * 100,
        2
    ) AS percentage_of_returns
FROM operations
WHERE return_flag = 1
GROUP BY return_reason
ORDER BY returned_orders DESC;

-- =========================================================
-- 05. Returns by Product Category
-- =========================================================

SELECT
    p.category,

    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE o.return_flag = 1
    ) AS returned_orders,

    ROUND(
        COUNT(*) FILTER (
            WHERE o.return_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS return_rate_percentage

FROM operations o

JOIN orders ord
    ON o.order_id = ord.order_id

JOIN order_items oi
    ON ord.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

GROUP BY p.category

ORDER BY return_rate_percentage DESC;

-- =========================================================
-- 06. Cancellation Performance by Region
-- =========================================================

SELECT
    c.region,

    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE o.cancellation_flag = 1
    ) AS cancelled_orders,

    ROUND(
        COUNT(*) FILTER (
            WHERE o.cancellation_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS cancellation_rate_percentage

FROM operations o

JOIN orders ord
    ON o.order_id = ord.order_id

JOIN customers c
    ON ord.customer_id = c.customer_id

GROUP BY c.region

ORDER BY cancellation_rate_percentage DESC;

-- =========================================================
-- 07. Overall Returns & Cancellation Impact
-- =========================================================

SELECT
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE cancellation_flag = 1
    ) AS cancelled_orders,

    COUNT(*) FILTER (
        WHERE return_flag = 1
    ) AS returned_orders,

    COUNT(*) FILTER (
        WHERE cancellation_flag = 0
          AND return_flag = 0
    ) AS completed_without_return,

    ROUND(
        COUNT(*) FILTER (
            WHERE cancellation_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS cancellation_rate_percentage,

    ROUND(
        COUNT(*) FILTER (
            WHERE return_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS return_rate_percentage

FROM operations;

-- =========================================================
-- 08. Revenue & Profit Impact of Returns & Cancellations
-- =========================================================

SELECT
    CASE
        WHEN cancellation_flag = 1 THEN 'Cancelled'
        WHEN return_flag = 1 THEN 'Returned'
        ELSE 'Completed'
    END AS order_outcome,

    COUNT(*) AS orders,

    ROUND(SUM(ord.total_revenue), 2) AS total_revenue,

    ROUND(SUM(ord.total_profit), 2) AS total_profit,

    ROUND(
        AVG(ord.total_revenue), 2
    ) AS avg_order_value

FROM operations o

JOIN orders ord
    ON o.order_id = ord.order_id

GROUP BY
    CASE
        WHEN cancellation_flag = 1 THEN 'Cancelled'
        WHEN return_flag = 1 THEN 'Returned'
        ELSE 'Completed'
    END

ORDER BY total_revenue DESC;

-- =========================================================
-- KEY BUSINESS FINDINGS
-- =========================================================
--
-- 1. 55,000 orders were analyzed with an overall late
--    delivery rate of 11.54%.
--
-- 2. West had the highest late-delivery rate at 16.52%
--    and the longest average delivery time at 4.24 days.
--
-- 3. Late deliveries did not show a higher return rate
--    than on-time deliveries in the available data.
--
-- 4. Damaged, Wrong Item and Quality issues represented
--    approximately 74.46% of recorded returns.
--
-- 5. Beauty had the highest category return rate at 7.65%,
--    although category differences were relatively small.
--
-- 6. Overall cancellation rate was 5.95% and return rate
--    was 7.54%.
--
-- 7. Returned and cancelled orders represented approximately
--    13.5% of all orders and were associated with 27.1M
--    in recorded order revenue.
--
-- 8. Product quality, item accuracy and damage prevention
--    should be investigated as key return-reduction areas. 
