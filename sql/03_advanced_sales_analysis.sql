USE ecommerce_analytics;


-- =========================================================
-- 1. MONTHLY REVENUE + MONTH-OVER-MONTH GROWTH
-- =========================================================

WITH monthly_sales AS (

    SELECT
        DATE_FORMAT(
            o.order_purchase_timestamp,
            '%Y-%m'
        ) AS order_month,

        COUNT(DISTINCT o.order_id) AS orders,

        ROUND(SUM(oi.price), 2) AS revenue

    FROM orders o

    INNER JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'delivered'

    GROUP BY
        DATE_FORMAT(
            o.order_purchase_timestamp,
            '%Y-%m'
        )
),

monthly_comparison AS (

    SELECT
        order_month,
        orders,
        revenue,

        LAG(revenue) OVER (
            ORDER BY order_month
        ) AS previous_month_revenue

    FROM monthly_sales
)

SELECT
    order_month,
    orders,
    revenue,
    previous_month_revenue,

    ROUND(
        revenue - previous_month_revenue,
        2
    ) AS revenue_change,

    ROUND(
        (
            (revenue - previous_month_revenue)
            / NULLIF(previous_month_revenue, 0)
        ) * 100,
        2
    ) AS mom_growth_percentage

FROM monthly_comparison

ORDER BY order_month;


-- =========================================================
-- 2. TOP CATEGORIES WITH REVENUE RANK
-- =========================================================

WITH category_sales AS (

    SELECT
        COALESCE(
            ct.product_category_name_english,
            'Unknown'
        ) AS category,

        ROUND(SUM(oi.price), 2) AS revenue,

        COUNT(*) AS items_sold,

        COUNT(DISTINCT oi.order_id) AS orders

    FROM orders o

    INNER JOIN order_items oi
        ON o.order_id = oi.order_id

    INNER JOIN products p
        ON oi.product_id = p.product_id

    LEFT JOIN category_translation ct
        ON p.product_category_name =
           ct.product_category_name

    WHERE o.order_status = 'delivered'

    GROUP BY
        COALESCE(
            ct.product_category_name_english,
            'Unknown'
        )
)

SELECT
    category,
    revenue,
    items_sold,
    orders,

    RANK() OVER (
        ORDER BY revenue DESC
    ) AS revenue_rank

FROM category_sales

ORDER BY revenue_rank;



-- =========================================================
-- 3. TOP CUSTOMERS BY SPENDING
-- =========================================================

WITH customer_sales AS (

    SELECT
        c.customer_unique_id,

        COUNT(DISTINCT o.order_id) AS total_orders,

        ROUND(SUM(oi.price), 2) AS total_spent

    FROM customers c

    INNER JOIN orders o
        ON c.customer_id = o.customer_id

    INNER JOIN order_items oi
        ON o.order_id = oi.order_id

    WHERE o.order_status = 'delivered'

    GROUP BY
        c.customer_unique_id
)

SELECT
    customer_unique_id,
    total_orders,
    total_spent,

    RANK() OVER (
        ORDER BY total_spent DESC
    ) AS spending_rank

FROM customer_sales

ORDER BY spending_rank

LIMIT 20;



