DELETE FROM sys_users WHERE username = 'admin';
INSERT INTO sys_users (id, username, password, nickname, email, status, role_id) 
VALUES (1, 'admin', '$2b$12$BGFXpAuSoS4LhlFXL2U54uH8wIyBSW7Vt.NiAChuI8MYPRhzAdj0W', '管理员', 'admin@example.com', 1, 1);
