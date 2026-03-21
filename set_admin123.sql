DELETE FROM sys_users WHERE username = 'admin';
INSERT INTO sys_users (id, username, password, nickname, email, status, role_id) 
VALUES (1, 'admin', $$$2b$12$lc1SpD2Bwht13byRZzEH7uByMLrdso3LP1Vvwti.xH9Ngcc/iM/gK$$, '管理员', 'admin@example.com', 1, 1);
