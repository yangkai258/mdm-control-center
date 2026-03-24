-- =====================
-- 第3批：会员相关
-- =====================

-- member_levels (会员等级) - 3条
INSERT INTO member_levels (level_name, level_code, min_points, max_points, discount, points_rate, sort, created_at, updated_at) VALUES
('普通会员', 'LV1', 0, 999, 0.95, 1.0, 1, NOW(), NOW()),
('VIP会员', 'LV2', 1000, 4999, 0.90, 1.2, 2, NOW(), NOW()),
('钻石会员', 'LV3', 5000, 999999, 0.85, 1.5, 3, NOW(), NOW());

-- member_cards (会员卡) - 3条
INSERT INTO member_cards (card_code, card_name, card_type, group_id, discount, points_rate, init_points, init_balance, valid_days, status, created_at, updated_at) VALUES
('CARD001', '宠物体验卡', 1, NULL, 0.95, 1.0, 0, 100.00, 365, 1, NOW(), NOW()),
('CARD002', '宠物年卡', 2, NULL, 0.90, 1.2, 500, 500.00, 730, 1, NOW(), NOW()),
('CARD003', '宠物钻石卡', 3, NULL, 0.85, 1.5, 2000, 2000.00, 1095, 1, NOW(), NOW());

-- member_points_records (积分记录) - 3条
INSERT INTO member_points_records (member_id, points, points_type, source_type, source_id, order_no, before_balance, after_balance, operator, remark, created_at) VALUES
(1, 100, 1, 'order', 'ORD001', 'ORD20260324001', 5700, 5800, 'system', '订单消费奖励积分', NOW()),
(2, -500, 2, 'redeem', 'RDM001', NULL, 12500, 12000, 'member', '积分兑换优惠券', NOW()),
(3, 200, 1, 'signin', 'SIG001', NULL, 1300, 1500, 'system', '每日签到奖励', NOW());

-- coupons (优惠券) - 3条
INSERT INTO coupons (coupon_code, coupon_name, coupon_type, face_value, min_amount, discount_rate, total_stock, remain_stock, valid_days, start_time, end_time, status, created_at, updated_at) VALUES
('CPN001', '新人专享券', 1, 20.00, 100.00, NULL, 1000, 850, 30, NOW(), NOW() + INTERVAL '30 days', 1, NOW(), NOW()),
('CPN002', '满减优惠券', 2, 50.00, 300.00, NULL, 500, 420, 15, NOW(), NOW() + INTERVAL '15 days', 1, NOW(), NOW()),
('CPN003', '95折折扣券', 3, NULL, 200.00, 0.95, 300, 280, 7, NOW(), NOW() + INTERVAL '7 days', 1, NOW(), NOW());

-- promotions (促销活动) - 3条
INSERT INTO promotions (promo_code, promo_name, promo_type, start_time, end_time, rule_config, status, created_at, updated_at) VALUES
('PROMO001', '春季大促', 1, '2026-03-01'::timestamp, '2026-03-31'::timestamp, '{"discount_type": "percentage", "discount": 0.85, "max_discount": 100}'::jsonb, 1, NOW(), NOW()),
('PROMO002', '新品首发', 2, '2026-03-20'::timestamp, '2026-04-20'::timestamp, '{"discount_type": "fixed", "discount": 50, "min_amount": 200}'::jsonb, 1, NOW(), NOW()),
('PROMO003', '会员日活动', 3, '2026-03-15'::timestamp, '2026-03-31'::timestamp, '{"points_multiplier": 3, "free_shipping": true}'::jsonb, 1, NOW(), NOW());
