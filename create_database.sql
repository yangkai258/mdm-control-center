
-- 创建数据库
CREATE DATABASE IF NOT EXISTS user_auth_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE user_auth_db;

-- 创建用户 (可选)
CREATE USER IF NOT EXISTS 'auth_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON user_auth_db.* TO 'auth_user'@'localhost';
FLUSH PRIVILEGES;

-- 查看数据库
SHOW DATABASES;
