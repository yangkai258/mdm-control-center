DELETE FROM sys_users WHERE username='admin';
INSERT INTO sys_users (username, password, nickname, email, status, role_id, created_at, updated_at) VALUES ('admin', '$2b$10$40ziGf/Qp1eBw6HJ3yef/OZ6HW571T.ZLoNpBrC/0tBN2DHmt0E4C', '管理员', 'admin@example.com', 1, 1, NOW(), NOW());
