-- สร้างฐานข้อมูล
CREATE DATABASE IF NOT EXISTS system_monitor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE system_monitor;

-- ตาราง benchmark_logs
CREATE TABLE IF NOT EXISTS benchmark_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_type VARCHAR(50),
    total_time FLOAT,
    avg_score FLOAT,
    device VARCHAR(50),
    mode VARCHAR(50),
    cpu_brand VARCHAR(255),
    cpu_info VARCHAR(255),
    scores_json TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
