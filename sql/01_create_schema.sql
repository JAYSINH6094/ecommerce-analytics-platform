CREATE DATABASE IF NOT EXISTS ecommerce_analytics;

USE ecommerce_analytics;


-- =========================================================
-- 1. CUSTOMERS
-- =========================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32) NOT NULL,
    customer_zip_code_prefix INT NOT NULL,
    customer_city VARCHAR(100) NOT NULL,
    customer_state CHAR(2) NOT NULL,

    INDEX idx_customer_unique_id (customer_unique_id),
    INDEX idx_customer_state (customer_state)
);


-- =========================================================
-- 2. SELLERS
-- =========================================================

CREATE TABLE IF NOT EXISTS sellers (
    seller_id VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix INT NOT NULL,
    seller_city VARCHAR(100) NOT NULL,
    seller_state CHAR(2) NOT NULL,

    INDEX idx_seller_state (seller_state)
);


-- =========================================================
-- 3. PRODUCTS
-- =========================================================

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(32) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g DECIMAL(10,2),
    product_length_cm DECIMAL(10,2),
    product_height_cm DECIMAL(10,2),
    product_width_cm DECIMAL(10,2),

    INDEX idx_product_category (product_category_name)
);


-- =========================================================
-- 4. CATEGORY TRANSLATION
-- =========================================================

CREATE TABLE IF NOT EXISTS category_translation (
    product_category_name VARCHAR(100) PRIMARY KEY,
    product_category_name_english VARCHAR(100) NOT NULL
);


-- =========================================================
-- 5. ORDERS
-- =========================================================

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL,
    order_status VARCHAR(20) NOT NULL,

    order_purchase_timestamp DATETIME NOT NULL,
    order_approved_at DATETIME NULL,
    order_delivered_carrier_date DATETIME NULL,
    order_delivered_customer_date DATETIME NULL,
    order_estimated_delivery_date DATETIME NULL,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    INDEX idx_orders_customer (customer_id),
    INDEX idx_orders_status (order_status),
    INDEX idx_orders_purchase_date (order_purchase_timestamp)
);


-- =========================================================
-- 6. ORDER ITEMS
-- =========================================================

CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR(32) NOT NULL,
    order_item_id INT NOT NULL,
    product_id VARCHAR(32) NOT NULL,
    seller_id VARCHAR(32) NOT NULL,

    shipping_limit_date DATETIME NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    freight_value DECIMAL(12,2) NOT NULL,

    PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_items_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id),

    INDEX idx_items_product (product_id),
    INDEX idx_items_seller (seller_id)
);


-- =========================================================
-- 7. PAYMENTS
-- =========================================================

CREATE TABLE IF NOT EXISTS payments (
    order_id VARCHAR(32) NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR(30) NOT NULL,
    payment_installments INT NOT NULL,
    payment_value DECIMAL(12,2) NOT NULL,

    PRIMARY KEY (order_id, payment_sequential),

    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    INDEX idx_payments_type (payment_type)
);


-- =========================================================
-- 8. REVIEWS
-- =========================================================

CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(32) NOT NULL,
    order_id VARCHAR(32) NOT NULL,
    review_score INT NOT NULL,
    review_comment_title TEXT NULL,
    review_comment_message TEXT NULL,
    review_creation_date DATETIME NULL,
    review_answer_timestamp DATETIME NULL,

    PRIMARY KEY (review_id, order_id),

    CONSTRAINT fk_reviews_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    INDEX idx_reviews_order (order_id),
    INDEX idx_reviews_score (review_score)
);


-- =========================================================
-- 9. GEOLOCATION
-- =========================================================

CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix INT NOT NULL,
    geolocation_lat DECIMAL(10,7) NOT NULL,
    geolocation_lng DECIMAL(10,7) NOT NULL,
    geolocation_city VARCHAR(100) NOT NULL,
    geolocation_state CHAR(2) NOT NULL,

    INDEX idx_geo_zip (geolocation_zip_code_prefix),
    INDEX idx_geo_state (geolocation_state)
);


-- =========================================================
-- VERIFY TABLES
-- =========================================================

SHOW TABLES;