-- =====================
-- 第5批：订阅/计费
-- =====================

-- subscription_plans (订阅套餐) - 3条
INSERT INTO subscription_plans (plan_id, plan_name, plan_type, price, currency, duration_days, features, quotas, status, sort_order, created_at, updated_at) VALUES
('PLAN_ENT', '企业版', 'enterprise', 999.00, 'CNY', 30, '{"ai_models": true, "unlimited_devices": true, "priority_support": true, "custom_branding": true}'::jsonb, '{"devices": -1, "members": -1, "stores": 100}'::jsonb, 'active', 1, NOW(), NOW()),
('PLAN_PRO', '专业版', 'professional', 299.00, 'CNY', 30, '{"ai_models": true, "unlimited_devices": false, "priority_support": false, "custom_branding": false}'::jsonb, '{"devices": 100, "members": 1000, "stores": 10}'::jsonb, 'active', 2, NOW(), NOW()),
('PLAN_FREE', '免费版', 'free', 0.00, 'CNY', 365, '{"ai_models": false, "unlimited_devices": false, "priority_support": false, "custom_branding": false}'::jsonb, '{"devices": 5, "members": 50, "stores": 1}'::jsonb, 'active', 3, NOW(), NOW());

-- plans (计划) - 3条
INSERT INTO plans (plan_name, plan_code, price_monthly, price_yearly, user_quota, device_quota, dept_quota, store_quota, features, sort_order, is_active, created_at, updated_at) VALUES
('企业计划', 'ENT_PLAN', 999.00, 9990.00, -1, -1, 50, 100, '{"unlimited_devices": true, "unlimited_users": true, "ai_analysis": true}'::jsonb, 1, true, NOW(), NOW()),
('专业计划', 'PRO_PLAN', 299.00, 2990.00, -1, 100, 10, 10, '{"unlimited_devices": false, "ai_analysis": false}'::jsonb, 2, true, NOW(), NOW()),
('基础计划', 'BASIC_PLAN', 0.00, 0.00, 5, 10, 1, 1, '{"basic_monitoring": true}'::jsonb, 3, true, NOW(), NOW());

-- user_subscriptions (用户订阅) - 3条
INSERT INTO user_subscriptions (sub_id, user_id, plan_id, status, start_time, expire_time, auto_renew, created_at, updated_at) VALUES
('SUB001', 1, 'PLAN_ENT', 'active', NOW() - INTERVAL '15 days', NOW() + INTERVAL '15 days', true, NOW(), NOW()),
('SUB002', 2, 'PLAN_PRO', 'active', NOW() - INTERVAL '7 days', NOW() + INTERVAL '23 days', true, NOW(), NOW()),
('SUB003', 3, 'PLAN_FREE', 'active', NOW() - INTERVAL '30 days', NOW() + INTERVAL '335 days', false, NOW(), NOW());

-- billing_records - 这个表不存在，跳过

-- api_keys (API密钥) - 3条
INSERT INTO api_keys (user_id, app_id, key_id, key_prefix, key_hash, name, scopes, rate_limit, status, last_used_at, expires_at, created_at, updated_at) VALUES
(1, 1, 'key_a0eebc999c0b4ef8bb6d6bb9bd380a11', 'mdm_live_', 'hash_key_001_xxxxxxxxxxxxxx', '生产环境API密钥', '["device:read", "device:write", "member:read"]'::jsonb, 1000, 1, NOW() - INTERVAL '1 hour', NOW() + INTERVAL '365 days', NOW(), NOW()),
(2, 1, 'key_b1eebc999c0b4ef8bb6d6bb9bd380b22', 'mdm_live_', 'hash_key_002_xxxxxxxxxxxxxx', '测试环境API密钥', '["device:read", "member:read"]'::jsonb, 100, 1, NOW() - INTERVAL '1 day', NOW() + INTERVAL '180 days', NOW(), NOW()),
(1, 1, 'key_c2eebc999c0b4ef8bb6d6bb9bd380c33', 'mdm_live_', 'hash_key_003_xxxxxxxxxxxxxx', '移动端API密钥', '["device:read", "device:write", "member:read", "pet:read"]'::jsonb, 500, 1, NOW() - INTERVAL '2 hours', NOW() + INTERVAL '90 days', NOW(), NOW());
