USE ecommerce_analytics;


-- =========================================================
-- 1. OVERALL ORDER SUMMARY
-- =========================================================

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers
FROM orders;


-- =========================================================
-- 2. ORDER STATUS DISTRIBUTION
-- =========================================================

SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS order_percentage
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- =========================================================
-- 3. COMPLETED ORDERS
-- =========================================================

SELECT
    COUNT(*) AS delivered_orders
FROM orders
WHERE order_status = 'delivered';


-- =========================================================
-- 4. TOTAL REVENUE FROM DELIVERED ORDERS
-- =========================================================

SELECT
    ROUND(SUM(oi.price), 2) AS total_revenue
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';


-- =========================================================
-- 5. TOTAL FREIGHT VALUE
-- =========================================================

SELECT
    ROUND(SUM(oi.freight_value), 2) AS total_freight
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';


-- =========================================================
-- 6. AVERAGE ORDER VALUE
-- =========================================================

SELECT
    ROUND(
        SUM(oi.price) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';


-- =========================================================
-- 7. MONTHLY REVENUE
-- =========================================================

SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    ) AS order_month,

    ROUND(SUM(oi.price), 2) AS revenue,

    COUNT(DISTINCT o.order_id) AS orders

FROM orders o

INNER JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    )

ORDER BY order_month;


-- =========================================================
-- 8. TOP 10 PRODUCT CATEGORIES BY REVENUE
-- =========================================================

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

ORDER BY revenue DESC

LIMIT 10;


-- =========================================================
-- 9. TOP 10 PRODUCTS BY REVENUE
-- =========================================================

SELECT
    oi.product_id,

    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    ) AS category,

    ROUND(SUM(oi.price), 2) AS revenue,

    COUNT(*) AS units_sold,

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
    oi.product_id,
    COALESCE(
        ct.product_category_name_english,
        'Unknown'
    )

ORDER BY revenue DESC

LIMIT 10;


-- =========================================================
-- 10. MONTHLY REVENUE WITH ORDER VALUE
-- =========================================================

SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    ) AS order_month,

    COUNT(DISTINCT o.order_id) AS orders,

    ROUND(SUM(oi.price), 2) AS revenue,

    ROUND(
        SUM(oi.price) /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM orders o

INNER JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    )

ORDER BY order_month;