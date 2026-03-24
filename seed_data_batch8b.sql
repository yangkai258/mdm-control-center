-- sys_roles (系统角色) - 3条 (retry with ASCII-safe names)
INSERT INTO sys_roles (name, code, description, sort, status, created_at, updated_at) VALUES
('Super Admin', 'SUPER_ADMIN', 'Super administrator with all permissions', 1, 1, NOW(), NOW());

INSERT INTO sys_roles (name, code, description, sort, status, created_at, updated_at) VALUES
('Operations Admin', 'OP_ADMIN', 'Daily operations administrator', 2, 1, NOW(), NOW());

INSERT INTO sys_roles (name, code, description, sort, status, created_at, updated_at) VALUES
('Normal User', 'NORMAL_USER', 'Regular user role', 3, 1, NOW(), NOW());

-- sys_users - add 2 more users (admin already exists)
INSERT INTO sys_users (username, password, nickname, email, phone, status, role_id, tenant_id, created_at, updated_at) VALUES
('operator1', '$2a$10$abcdefghijklmnopqrstuv', 'Operator One', 'op1@smartepet.com', '13800000001', 1, 1, (SELECT id FROM tenants LIMIT 1), NOW(), NOW());

INSERT INTO sys_users (username, password, nickname, email, phone, status, role_id, tenant_id, created_at, updated_at) VALUES
('operator2', '$2a$10$abcdefghijklmnopqrstuv', 'Operator Two', 'op2@smartepet.com', '13800000002', 1, 1, (SELECT id FROM tenants LIMIT 1), NOW(), NOW());
