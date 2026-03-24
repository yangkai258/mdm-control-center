-- =====================
-- 第4批：运营相关
-- =====================

-- notification_templates (通知模板) - 3条
INSERT INTO notification_templates (name, code, title_tpl, content_tpl, channel, priority, variables, enabled, created_at, updated_at) VALUES
('设备离线通知', 'DEVICE_OFFLINE', '您的宠物设备已离线', '亲爱的用户，您的设备 ${device_name} 已离线超过 ${offline_minutes} 分钟，请检查设备状态。', 'app', 2, 'device_name,offline_minutes', true, NOW(), NOW()),
('积分变动通知', 'POINTS_CHANGE', '积分变动提醒', '您的账户 ${points_change} 积分已到账，当前积分余额：${total_points}', 'app', 1, 'points_change,total_points', true, NOW(), NOW()),
('活动开始通知', 'PROMO_START', '促销活动开始了', '亲爱的会员，${promo_name} 活动已正式开启，快来参与吧！', 'app', 1, 'promo_name', true, NOW(), NOW());

-- notifications (通知) - 3条
INSERT INTO notifications (device_id, title, content, priority, channel, status, sent_at, delivered_at, created_by, created_at, updated_at) VALUES
('DEV001', '设备绑定成功', '恭喜！您的PetBot设备已成功绑定', 1, 'app', 'delivered', NOW(), NOW(), 'system', NOW(), NOW()),
('DEV002', '固件升级提醒', '新版本v1.2.4已发布，建议您及时升级', 2, 'app', 'sent', NOW(), NULL, 'system', NOW(), NOW()),
('DEV003', '设备离线告警', '您的PetBot设备已离线超过5分钟', 3, 'app', 'pending', NULL, NULL, 'system', NOW(), NOW());

-- announcements (公告) - 3条
INSERT INTO announcements (title, content, type, priority, target_type, target_id, status, start_time, end_time, created_by, published_by, published_at, created_at, updated_at) VALUES
('系统维护通知', '平台将于2026年3月25日凌晨2:00-6:00进行系统维护，届时部分功能暂停使用。', 'system', 2, 'all', NULL, 'published', '2026-03-24'::timestamp, '2026-03-26'::timestamp, 'admin', 'admin', NOW(), NOW(), NOW()),
('新功能上线公告', 'PetBot v1.2.4版本正式上线，新增智能陪伴模式，欢迎体验！', 'feature', 1, 'all', NULL, 'published', '2026-03-24'::timestamp, '2026-04-24'::timestamp, 'admin', 'admin', NOW(), NOW(), NOW()),
('会员日活动公告', '本月会员日将举办积分加倍活动，错过再等一个月！', 'event', 1, 'member', '1', 'published', '2026-03-25'::timestamp, '2026-03-31'::timestamp, 'admin', 'admin', NOW(), NOW(), NOW());

-- alert_settings (告警设置) - 3条
INSERT INTO alert_settings (alerts_enabled, email_enabled, sms_enabled, webhook_enabled, in_app_enabled, notify_on_critical, notify_on_high, notify_on_medium, notify_on_low, digest_enabled, digest_interval, quiet_hours_enabled, quiet_hours_start, quiet_hours_end, max_per_hour, auto_resolve_hours, created_at, updated_at) VALUES
(true, true, false, true, true, true, true, true, false, true, 60, true, '22:00', '08:00', 10, 24, NOW(), NOW()),
(true, false, true, false, true, true, true, false, false, false, NULL, false, NULL, NULL, 20, 12, NOW(), NOW()),
(true, true, true, true, true, true, true, true, true, true, 30, true, '23:00', '07:00', 5, 48, NOW(), NOW());

-- alert_history (告警历史) - 3条
INSERT INTO alert_history (original_id, rule_id, device_id, alert_type, severity, message, trigger_value, threshold, status, notified_channels, confirmed_at, confirmed_by, resolved_at, resolved_by, resolve_remark, created_at, tenant_id) VALUES
(1, 1, 'DEV001', 'battery_low', 2, '设备电池电量低于20%', '18.5', '20.0', 2, '["app", "email"]'::jsonb, NOW(), 1, NOW(), 1, '已更换电池', NOW(), (SELECT id FROM tenants LIMIT 1)),
(2, 2, 'DEV002', 'offline', 3, '设备离线超过5分钟', '300', '300', 1, '["app"]'::jsonb, NULL, NULL, NULL, NULL, NULL, NOW(), (SELECT id FROM tenants LIMIT 1)),
(3, 3, 'DEV003', 'temperature_high', 2, '设备温度过高', '75.0', '70.0', 0, '["app", "sms"]'::jsonb, NULL, NULL, NULL, NULL, NULL, NOW(), (SELECT id FROM tenants LIMIT 1));
