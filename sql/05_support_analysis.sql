-- =========================================================
-- 01. Overall Support Performance
-- =========================================================

SELECT
    COUNT(*) AS total_tickets,

    COUNT(*) FILTER (
        WHERE resolved_flag = 1
    ) AS resolved_tickets,

    COUNT(*) FILTER (
        WHERE resolved_flag = 0
    ) AS unresolved_tickets,

    ROUND(
        COUNT(*) FILTER (
            WHERE resolved_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS resolution_rate_percentage,

    ROUND(
        AVG(resolution_time)
        FILTER (WHERE resolved_flag = 1),
        2
    ) AS avg_resolution_time

FROM support_tickets;

-- =========================================================
-- 02. Support Issues by Type
-- =========================================================

SELECT
    issue_type,

    COUNT(*) AS total_tickets,

    COUNT(*) FILTER (
        WHERE resolved_flag = 1
    ) AS resolved_tickets,

    COUNT(*) FILTER (
        WHERE resolved_flag = 0
    ) AS unresolved_tickets,

    ROUND(
        COUNT(*) FILTER (
            WHERE resolved_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS resolution_rate_percentage,

    ROUND(
        AVG(resolution_time)
        FILTER (WHERE resolved_flag = 1),
        2
    ) AS avg_resolution_time

FROM support_tickets

GROUP BY issue_type

ORDER BY total_tickets DESC;

-- =========================================================
-- 03. Support Performance by Priority
-- =========================================================

SELECT
    priority,

    COUNT(*) AS total_tickets,

    COUNT(*) FILTER (
        WHERE resolved_flag = 1
    ) AS resolved_tickets,

    COUNT(*) FILTER (
        WHERE resolved_flag = 0
    ) AS unresolved_tickets,

    ROUND(
        COUNT(*) FILTER (
            WHERE resolved_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS resolution_rate_percentage,

    ROUND(
        AVG(resolution_time)
        FILTER (WHERE resolved_flag = 1),
        2
    ) AS avg_resolution_time

FROM support_tickets

GROUP BY priority

ORDER BY
    CASE priority
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
        ELSE 4
    END;

    -- =========================================================
-- 04. Unresolved Support Backlog by Issue Type
-- =========================================================

SELECT
    issue_type,

    COUNT(*) AS unresolved_tickets,

    ROUND(
        COUNT(*)::numeric
        / SUM(COUNT(*)) OVER () * 100,
        2
    ) AS percentage_of_unresolved_tickets,

    ROUND(
        AVG(resolution_time),
        2
    ) AS avg_resolution_time

FROM support_tickets

WHERE resolved_flag = 0

GROUP BY issue_type

ORDER BY unresolved_tickets DESC;


-- =========================================================
-- 05. Support Performance by Region
-- =========================================================

SELECT
    c.region,

    COUNT(*) AS total_tickets,

    COUNT(*) FILTER (
        WHERE st.resolved_flag = 1
    ) AS resolved_tickets,

    COUNT(*) FILTER (
        WHERE st.resolved_flag = 0
    ) AS unresolved_tickets,

    ROUND(
        COUNT(*) FILTER (
            WHERE st.resolved_flag = 1
        )::numeric
        / COUNT(*) * 100,
        2
    ) AS resolution_rate_percentage,

    ROUND(
        AVG(st.resolution_time)
        FILTER (WHERE st.resolved_flag = 1),
        2
    ) AS avg_resolution_time

FROM support_tickets st

JOIN customers c
    ON st.customer_id = c.customer_id

GROUP BY c.region

ORDER BY unresolved_tickets DESC;

-- =========================================================
-- 06. Delivery Complaints vs Delivery Performance
-- =========================================================

WITH delivery_support AS (
    SELECT
        c.region,
        COUNT(*) AS delivery_support_tickets
    FROM support_tickets st
    JOIN customers c
        ON st.customer_id = c.customer_id
    WHERE st.issue_type = 'Delivery'
    GROUP BY c.region
),

delivery_operations AS (
    SELECT
        c.region,
        COUNT(*) AS total_orders,
        COUNT(*) FILTER (
            WHERE o.delivery_status = 'Late'
        ) AS late_deliveries,
        ROUND(
            COUNT(*) FILTER (
                WHERE o.delivery_status = 'Late'
            )::numeric / COUNT(*) * 100,
            2
        ) AS late_delivery_percentage
    FROM operations o
    JOIN orders ord
        ON o.order_id = ord.order_id
    JOIN customers c
        ON ord.customer_id = c.customer_id
    GROUP BY c.region
)

SELECT
    d.region,
    d.total_orders,
    d.late_deliveries,
    d.late_delivery_percentage,
    COALESCE(s.delivery_support_tickets, 0)
        AS delivery_support_tickets

FROM delivery_operations d

LEFT JOIN delivery_support s
    ON d.region = s.region

ORDER BY d.late_delivery_percentage DESC;

-- =========================================================
-- 07. Delivery Complaint Rate by Region
-- =========================================================

WITH delivery_support AS (
    SELECT
        c.region,
        COUNT(*) AS delivery_support_tickets
    FROM support_tickets st
    JOIN customers c
        ON st.customer_id = c.customer_id
    WHERE st.issue_type = 'Delivery'
    GROUP BY c.region
),

delivery_orders AS (
    SELECT
        c.region,
        COUNT(*) AS total_orders
    FROM operations o
    JOIN orders ord
        ON o.order_id = ord.order_id
    JOIN customers c
        ON ord.customer_id = c.customer_id
    GROUP BY c.region
)

SELECT
    d.region,
    d.total_orders,
    COALESCE(s.delivery_support_tickets, 0)
        AS delivery_support_tickets,

    ROUND(
        COALESCE(s.delivery_support_tickets, 0)::numeric
        / d.total_orders * 1000,
        2
    ) AS delivery_complaints_per_1000_orders

FROM delivery_orders d

LEFT JOIN delivery_support s
    ON d.region = s.region

ORDER BY delivery_complaints_per_1000_orders DESC;

-- =========================================================
-- KEY BUSINESS FINDINGS
-- =========================================================
--
-- 1. ShopSphere handled 18,000 support tickets with a
--    93.94% overall resolution rate.
--
-- 2. Delivery was the largest support issue, generating
--    5,418 tickets (approximately 30.1% of all tickets).
--
-- 3. Delivery also represented the largest unresolved
--    support backlog, accounting for 30.80% of unresolved
--    tickets.
--
-- 4. Support resolution rates were relatively consistent
--    across issue types and priority levels, with no major
--    difference in resolution performance.
--
-- 5. South had the lowest regional support resolution rate
--    at 92.95%, while North had the highest at 94.53%.
--
-- 6. West had the highest late-delivery rate at 16.52% and
--    the highest absolute number of delivery complaints.
--
-- 7. South had the highest normalized delivery complaint
--    rate at 101.46 complaints per 1,000 orders, despite
--    having a much lower late-delivery rate than West.
--
-- 8. The difference between delivery performance and
--    complaint rates suggests that customer complaints
--    cannot be explained by late deliveries alone.
--
-- 9. West should be investigated for logistics performance,
--    while South should be investigated for broader
--    delivery-related customer experience issues.

