-- =========================================================
-- CUSTOMER & PRODUCT INTELLIGENCE
-- 03 - Funnel & Customer Behavior Analysis
-- =========================================================

-- 1. Traffic Source Performance
-- =========================================================

SELECT
    s.traffic_source,
    COUNT(DISTINCT s.session_id) AS total_sessions,
    COUNT(DISTINCT s.customer_id) AS unique_customers,
    ROUND(AVG(s.session_duration), 2) AS avg_session_duration,
    ROUND(AVG(s.pages_viewed), 2) AS avg_pages_viewed
FROM sessions s
GROUP BY s.traffic_source
ORDER BY total_sessions DESC;

-- =========================================================
-- 2. Traffic Source -> Orders -> Revenue
-- First-Touch Attribution
-- =========================================================

WITH first_touch AS (
    SELECT
        customer_id,
        traffic_source
    FROM (
        SELECT
            customer_id,
            traffic_source,
            session_date,
            ROW_NUMBER() OVER (
                PARTITION BY customer_id
                ORDER BY session_date
            ) AS rn
        FROM sessions
    ) s
    WHERE rn = 1
),

customer_revenue AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_revenue) AS total_revenue,
        SUM(total_profit) AS total_profit
    FROM orders
    GROUP BY customer_id
)

SELECT
    ft.traffic_source,
    COUNT(DISTINCT ft.customer_id) AS customers,
    SUM(COALESCE(cr.total_orders, 0)) AS total_orders,
    ROUND(SUM(COALESCE(cr.total_revenue, 0)), 2) AS total_revenue,
    ROUND(SUM(COALESCE(cr.total_profit, 0)), 2) AS total_profit
FROM first_touch ft
LEFT JOIN customer_revenue cr
    ON ft.customer_id = cr.customer_id
GROUP BY ft.traffic_source
ORDER BY total_revenue DESC;

-- =========================================================
-- 3. Traffic Source Conversion Rate
-- =========================================================

WITH first_touch AS (
    SELECT
        customer_id,
        traffic_source
    FROM (
        SELECT
            customer_id,
            traffic_source,
            session_date,
            ROW_NUMBER() OVER (
                PARTITION BY customer_id
                ORDER BY session_date
            ) AS rn
        FROM sessions
    ) s
    WHERE rn = 1
),

customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS orders
    FROM orders
    GROUP BY customer_id
)

SELECT
    ft.traffic_source,

    COUNT(DISTINCT ft.customer_id) AS customers,

    COUNT(DISTINCT co.customer_id) AS customers_with_orders,

    ROUND(
        COUNT(DISTINCT co.customer_id)::numeric
        / COUNT(DISTINCT ft.customer_id) * 100,
        2
    ) AS conversion_rate_percentage

FROM first_touch ft

LEFT JOIN customer_orders co
    ON ft.customer_id = co.customer_id

GROUP BY ft.traffic_source

ORDER BY conversion_rate_percentage DESC;

-- =========================================================
-- 4. Available User Event Types
-- =========================================================

SELECT
    event_type,
    COUNT(*) AS event_count,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM user_events
GROUP BY event_type
ORDER BY event_count DESC;

-- =========================================================
-- 5. Overall Funnel Conversion
-- =========================================================

WITH funnel AS (
    SELECT
        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Visit')
            AS visitors,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Product_View')
            AS product_viewers,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Add_to_Cart')
            AS cart_users,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Checkout')
            AS checkout_users,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Purchase')
            AS purchasers

    FROM user_events
)

SELECT
    visitors,
    product_viewers,
    cart_users,
    checkout_users,
    purchasers,

    ROUND(
        product_viewers::numeric / visitors * 100,
        2
    ) AS visit_to_product_percentage,

    ROUND(
        cart_users::numeric / product_viewers * 100,
        2
    ) AS product_to_cart_percentage,

    ROUND(
        checkout_users::numeric / cart_users * 100,
        2
    ) AS cart_to_checkout_percentage,

    ROUND(
        purchasers::numeric / checkout_users * 100,
        2
    ) AS checkout_to_purchase_percentage,

    ROUND(
        purchasers::numeric / visitors * 100,
        2
    ) AS overall_conversion_percentage

FROM funnel;

-- =========================================================
-- 6. Funnel Performance by Device
-- =========================================================

SELECT
    device,

    COUNT(DISTINCT customer_id)
        FILTER (WHERE event_type = 'Visit')
        AS visitors,

    COUNT(DISTINCT customer_id)
        FILTER (WHERE event_type = 'Product_View')
        AS product_viewers,

    COUNT(DISTINCT customer_id)
        FILTER (WHERE event_type = 'Add_to_Cart')
        AS cart_users,

    COUNT(DISTINCT customer_id)
        FILTER (WHERE event_type = 'Checkout')
        AS checkout_users,

    COUNT(DISTINCT customer_id)
        FILTER (WHERE event_type = 'Purchase')
        AS purchasers,

    ROUND(
        COUNT(DISTINCT customer_id)
        FILTER (WHERE event_type = 'Purchase')::numeric
        /
        NULLIF(
            COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Visit'),
            0
        ) * 100,
        2
    ) AS overall_conversion_percentage

FROM user_events

GROUP BY device

ORDER BY overall_conversion_percentage DESC;

-- =========================================================
-- 7. Funnel Drop-off by Device
-- =========================================================

WITH device_funnel AS (
    SELECT
        device,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Visit')
            AS visitors,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Product_View')
            AS product_viewers,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Add_to_Cart')
            AS cart_users,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Checkout')
            AS checkout_users,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE event_type = 'Purchase')
            AS purchasers

    FROM user_events
    GROUP BY device
)

SELECT
    device,
    visitors,
    product_viewers,
    cart_users,
    checkout_users,
    purchasers,

    ROUND(
        (visitors - product_viewers)::numeric
        / NULLIF(visitors, 0) * 100,
        2
    ) AS visit_drop_percentage,

    ROUND(
        (product_viewers - cart_users)::numeric
        / NULLIF(product_viewers, 0) * 100,
        2
    ) AS product_to_cart_drop_percentage,

    ROUND(
        (cart_users - checkout_users)::numeric
        / NULLIF(cart_users, 0) * 100,
        2
    ) AS cart_to_checkout_drop_percentage,

    ROUND(
        (checkout_users - purchasers)::numeric
        / NULLIF(checkout_users, 0) * 100,
        2
    ) AS checkout_to_purchase_drop_percentage

FROM device_funnel
ORDER BY checkout_to_purchase_drop_percentage DESC;

-- =========================================================
-- 8. A/B Test - Control vs Treatment
-- =========================================================

SELECT
    experiment_name,
    "group",

    COUNT(DISTINCT customer_id) AS customers,

    COUNT(DISTINCT customer_id)
        FILTER (WHERE converted = 1) AS converted_customers,

    ROUND(
        COUNT(DISTINCT customer_id)
        FILTER (WHERE converted = 1)::numeric
        / COUNT(DISTINCT customer_id) * 100,
        2
    ) AS conversion_rate_percentage

FROM experiments

GROUP BY
    experiment_name,
    "group"

ORDER BY
    experiment_name,
    "group";

-- =========================================================
-- 9. A/B Test Statistical Significance
-- =========================================================

WITH experiment_summary AS (
    SELECT
        "group",

        COUNT(DISTINCT customer_id) AS customers,

        COUNT(DISTINCT customer_id)
            FILTER (WHERE converted = 1) AS conversions

    FROM experiments

    GROUP BY "group"
),

rates AS (
    SELECT
        MAX(customers) FILTER (WHERE "group" = 'Control')
            AS control_n,

        MAX(conversions) FILTER (WHERE "group" = 'Control')
            AS control_conversions,

        MAX(customers) FILTER (WHERE "group" = 'Treatment')
            AS treatment_n,

        MAX(conversions) FILTER (WHERE "group" = 'Treatment')
            AS treatment_conversions

    FROM experiment_summary
),

calculations AS (
    SELECT
        *,
        control_conversions::numeric / control_n
            AS control_rate,

        treatment_conversions::numeric / treatment_n
            AS treatment_rate,

        (control_conversions + treatment_conversions)::numeric
        / (control_n + treatment_n)
            AS pooled_rate

    FROM rates
)

SELECT
    ROUND(control_rate * 100, 2)
        AS control_conversion_percentage,

    ROUND(treatment_rate * 100, 2)
        AS treatment_conversion_percentage,

    ROUND(
        (treatment_rate - control_rate) * 100,
        2
    ) AS absolute_lift_percentage_points,

    ROUND(
        ((treatment_rate - control_rate) / control_rate) * 100,
        2
    ) AS relative_lift_percentage,

    ROUND(
        (treatment_rate - control_rate)
        /
        SQRT(
            pooled_rate
            * (1 - pooled_rate)
            * (
                1.0 / control_n
                + 1.0 / treatment_n
            )
        ),
        4
    ) AS z_score

FROM calculations;


-- =========================================================
-- KEY BUSINESS FINDINGS
-- =========================================================
--
-- 1. Organic was the strongest first-touch acquisition
--    source by customers, orders, revenue and profit.
--
-- 2. Event-based customer conversion from Visit to Purchase
--    was 78.09% in the dataset.
--
-- 3. Mobile users showed the highest event-based conversion
--    rate at 62.24%.
--
-- 4. Tablet users showed substantially lower conversion,
--    with the highest drop-offs across the funnel.
--
-- 5. Tablet Product View to Add-to-Cart drop-off was 39.70%.
--
-- 6. Tablet Checkout to Purchase drop-off was 38.38%.
--
-- 7. The Treatment group showed a 3.32% relative conversion
--    lift over Control, but the difference was not statistically
--    significant.
--
-- 8. The tablet experience should be investigated as a
--    potential funnel optimization opportunity.