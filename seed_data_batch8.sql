-- =====================
-- 第8批：系统配置
-- =====================

-- sys_roles (系统角色) - 3条
INSERT INTO sys_roles (name, code, description, sort, status, created_at, updated_at) VALUES
('超级管理员', 'SUPER_ADMIN', '系统超级管理员，拥有所有权限', 1, 1, NOW(), NOW()),
('运营管理员', 'OP_ADMIN', '负责日常运营管理的管理员', 2, 1, NOW(), NOW()),
('普通用户', 'NORMAL_USER', '普通用户角色', 3, 1, NOW(), NOW());

-- sys_permissions (权限) - 3条
INSERT INTO sys_permissions (parent_id, name, code, type, path, component, icon, sort, visible, permission, status, created_at, updated_at) VALUES
(NULL, '设备管理', 'device', 1, '/device', 'Layout', 'icon-device', 1, 1, 'device:manage', 1, NOW(), NOW()),
(NULL, '会员管理', 'member', 1, '/member', 'Layout', 'icon-user', 2, 1, 'member:manage', 1, NOW(), NOW()),
(NULL, '系统设置', 'system', 1, '/system', 'Layout', 'icon-setting', 3, 1, 'system:manage', 1, NOW(), NOW());

-- menus (菜单) - 3条
INSERT INTO menus (parent_id, menu_name, menu_code, icon, route_path, component, permission, menu_type, sort, status, tenant_id, created_at, updated_at) VALUES
(NULL, '仪表盘', 'dashboard', 'icon-dashboard', '/dashboard', 'Dashboard', 'dashboard:view', 1, 1, 1, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
(NULL, '设备列表', 'device_list', 'icon-device', '/devices', 'DeviceList', 'device:list', 1, 2, 1, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
(NULL, '会员管理', 'member_mgmt', 'icon-user', '/members', 'MemberMgmt', 'member:list', 1, 3, 1, (SELECT id FROM tenants LIMIT 1), NOW(), NOW());

-- sys_users (系统用户) - 3条
INSERT INTO sys_users (username, password, nickname, email, phone, status, role_id, tenant_id, created_at, updated_at) VALUES
('admin', '$2a$10$abcdefghijklmnopqrstuv', '系统管理员', 'admin@smartepet.com', '13800000000', 1, 1, NULL, NOW(), NOW()),
('operator1', '$2a$10$abcdefghijklmnopqrstuv', '运营人员甲', 'op1@smartepet.com', '13800000001', 1, 2, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('operator2', '$2a$10$abcdefghijklmnopqrstuv', '运营人员乙', 'op2@smartepet.com', '13800000002', 1, 2, (SELECT id FROM tenants LIMIT 1), NOW(), NOW());

-- tenants config (tenant_applications / tenant_quotas) - 使用 tenants 表的 settings 字段
-- 额外插入两条 tenants 记录
INSERT INTO tenants (id, tenant_code, name, contact_name, contact_phone, contact_email, plan, status, logo_url, domain, expires_at, settings, created_at, updated_at) VALUES
(gen_random_uuid(), 'TENANT004', '测试租户', '测试管理员', '13700000004', 'test@test.com', 'trial', 'active', 'https://cdn.example.com/logos/tenant004.png', 'test.com', '2026-04-24'::timestamp, '{"max_devices": 10, "max_members": 50}'::jsonb, NOW(), NOW()),
(gen_random_uuid(), 'TENANT005', '演示租户', '演示用户', '13700000005', 'demo@demo.com', 'demo', 'active', 'https://cdn.example.com/logos/tenant005.png', 'demo.com', '2026-05-24'::timestamp, '{"max_devices": 20, "max_members": 100}'::jsonb, NOW(), NOW());
