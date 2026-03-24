-- =====================
-- 第1批：核心业务表
-- =====================

-- tenants (租户) - 3条
INSERT INTO tenants (id, tenant_code, name, contact_name, contact_phone, contact_email, plan, status, logo_url, domain, expires_at, settings, created_at, updated_at) VALUES
(gen_random_uuid(), 'TENANT001', '智慧宠物科技', '张明', '13800138001', 'zhangming@smartepet.com', 'enterprise', 'active', 'https://cdn.example.com/logos/tenant001.png', 'smartepet.com', '2027-03-24'::timestamp, '{"max_devices": 1000, "max_members": 5000}'::jsonb, NOW(), NOW()),
(gen_random_uuid(), 'TENANT002', '宠物生活馆', '李娜', '13900139002', 'lina@petlife.com', 'professional', 'active', 'https://cdn.example.com/logos/tenant002.png', 'petlife.com', '2026-12-31'::timestamp, '{"max_devices": 500, "max_members": 2000}'::jsonb, NOW(), NOW()),
(gen_random_uuid(), 'TENANT003', '萌宠王国', '王芳', '13700137003', 'wangfang@cutepet.com', 'free', 'active', 'https://cdn.example.com/logos/tenant003.png', 'cutepet.com', '2026-06-30'::timestamp, '{"max_devices": 50, "max_members": 200}'::jsonb, NOW(), NOW());

-- stores (门店) - 3条
INSERT INTO stores (store_code, store_name, store_type, province, city, district, address, contact, phone, status, created_at, updated_at) VALUES
('STORE001', '智慧宠物上海旗舰店', 1, '上海市', '上海市', '浦东新区', '浦东新区世纪大道100号', '陈店长', '021-88880001', 1, NOW(), NOW()),
('STORE002', '宠物生活馆北京店', 2, '北京市', '北京市', '朝阳区', '朝阳区建国路88号', '刘店长', '010-66660002', 1, NOW(), NOW()),
('STORE003', '萌宠王国成都店', 1, '四川省', '成都市', '武侯区', '武侯区科华北路66号', '赵店长', '028-88880003', 1, NOW(), NOW());

-- members (会员) - 3条
INSERT INTO members (member_code, member_name, phone, gender, birth_date, email, avatar, member_level, points, balance, card_id, store_id, status, source, remark, created_at, updated_at) VALUES
('MB001', '张小明', '13600001001', 'male', '1990-05-15'::timestamp, 'zhangxm@example.com', 'https://cdn.example.com/avatars/mb001.jpg', 2, 5800, 500.00, NULL, 1, 1, '门店注册', 'VIP会员', NOW(), NOW()),
('MB002', '李婷婷', '13600001002', 'female', '1995-08-20'::timestamp, 'liting@example.com', 'https://cdn.example.com/avatars/mb002.jpg', 3, 12000, 1200.00, NULL, 2, 1, '线上注册', '高级会员', NOW(), NOW()),
('MB003', '王建国', '13600001003', 'male', '1985-12-03'::timestamp, 'wangjg@example.com', 'https://cdn.example.com/avatars/mb003.jpg', 1, 1500, 0.00, NULL, 3, 1, '门店注册', '新会员', NOW(), NOW());

-- devices (设备) - 3条
INSERT INTO devices (device_id, mac_address, sn_code, hardware_model, firmware_version, bind_user_id, lifecycle_status, org_id, create_user_id, desired_state, created_at, updated_at) VALUES
('DEV001', 'AA:BB:CC:DD:EE:01', 'SN20260324001', 'M5Stack-PetBot-v2', 'v1.2.3', '13600001001', 1, 1, 1, '{"volume": 80, "brightness": 70}'::text, NOW(), NOW()),
('DEV002', 'AA:BB:CC:DD:EE:02', 'SN20260324002', 'M5Stack-PetBot-v2', 'v1.2.3', '13600001002', 1, 1, 1, '{"volume": 60, "brightness": 50}'::text, NOW(), NOW()),
('DEV003', 'AA:BB:CC:DD:EE:03', 'SN20260324003', 'M5Stack-PetBot-v1', 'v1.1.0', '13600001003', 1, 2, 2, '{"volume": 100, "brightness": 90}'::text, NOW(), NOW());

-- pet_profiles (宠物) - 3条 (pet_profiles uses device_id as primary key)
INSERT INTO pet_profiles (device_id, pet_name, personality, interaction_freq, dnd_start_time, dnd_end_time, custom_rules, created_at, updated_at) VALUES
('DEV001', '小旺', '活泼好动', 'high', '22:00', '07:00', '{"feed_reminder": true, "walk_reminder": true}'::jsonb, NOW(), NOW()),
('DEV002', '咪咪', '安静乖巧', 'medium', '23:00', '08:00', '{"feed_reminder": true, "walk_reminder": false}'::jsonb, NOW(), NOW()),
('DEV003', '豆豆', '调皮捣蛋', 'low', '21:00', '06:00', '{"feed_reminder": false, "walk_reminder": true}'::jsonb, NOW(), NOW());
