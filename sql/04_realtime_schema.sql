CREATE TABLE IF NOT EXISTS realtime_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL UNIQUE,

    customer_id VARCHAR(50) NOT NULL,

    product_category VARCHAR(100) NOT NULL,

    price DECIMAL(12, 2) NOT NULL,

    freight_value DECIMAL(12, 2) NOT NULL DEFAULT 0.00,

    customer_state VARCHAR(10) NOT NULL,

    payment_type VARCHAR(30) NOT NULL,

    quantity INT NOT NULL DEFAULT 1,

    order_timestamp DATETIME NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_realtime_order_timestamp (order_timestamp),
    INDEX idx_realtime_customer_id (customer_id),
    INDEX idx_realtime_category (product_category),
    INDEX idx_realtime_state (customer_state)
);