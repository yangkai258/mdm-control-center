-- notification_templates (通知模板) - 3条 (retry with ASCII-safe names)
INSERT INTO notification_templates (name, code, title_tpl, content_tpl, channel, priority, variables, enabled, created_at, updated_at) VALUES
('Device Offline Template', 'DEVICE_OFFLINE', 'PetBot Device Offline Alert', 'Dear user, your device ${device_name} has been offline for ${offline_minutes} minutes. Please check the device status.', 'app', 2, 'device_name,offline_minutes', true, NOW(), NOW());

INSERT INTO notification_templates (name, code, title_tpl, content_tpl, channel, priority, variables, enabled, created_at, updated_at) VALUES
('Points Change Template', 'POINTS_CHANGE', 'Points Change Notification', 'Your account has received ${points_change} points. Current balance: ${total_points}', 'app', 1, 'points_change,total_points', true, NOW(), NOW());

INSERT INTO notification_templates (name, code, title_tpl, content_tpl, channel, priority, variables, enabled, created_at, updated_at) VALUES
('Promotion Start Template', 'PROMO_START', 'Promotion Started', 'Dear member, the ${promo_name} promotion has officially started!', 'app', 1, 'promo_name', true, NOW(), NOW());
