-- device_shadows (设备影子) - 3条
INSERT INTO device_shadows (device_id, is_online, battery_level, current_mode, last_ip, last_heartbeat, desired_config, is_jailbroken, root_status, latitude, longitude, desired_nrd_enabled, desired_nrd_start, desired_nrd_end, desired_dnd_enabled, desired_dnd_start, desired_dnd_end, desired_volume, desired_brightness, desired_power_save, desired_version) VALUES
('DEV001', true, 85, 'normal', '192.168.1.101', NOW(), '{"volume": 80, "brightness": 70}'::jsonb, false, 'secure', 31.2304, 121.4737, true, '22:00', '07:00', true, '22:00', '07:00', 80, 70, false, 'v1.2.4');

INSERT INTO device_shadows (device_id, is_online, battery_level, current_mode, last_ip, last_heartbeat, desired_config, is_jailbroken, root_status, latitude, longitude, desired_nrd_enabled, desired_nrd_start, desired_nrd_end, desired_dnd_enabled, desired_dnd_start, desired_dnd_end, desired_volume, desired_brightness, desired_power_save, desired_version) VALUES
('DEV002', true, 62, 'sleep', '192.168.1.102', NOW(), '{"volume": 60, "brightness": 50}'::jsonb, false, 'secure', 39.9042, 116.4074, false, NULL, NULL, true, '23:00', '08:00', 60, 50, true, 'v1.2.3');

INSERT INTO device_shadows (device_id, is_online, battery_level, current_mode, last_ip, last_heartbeat, desired_config, is_jailbroken, root_status, latitude, longitude, desired_nrd_enabled, desired_nrd_start, desired_nrd_end, desired_dnd_enabled, desired_dnd_start, desired_dnd_end, desired_volume, desired_brightness, desired_power_save, desired_version) VALUES
('DEV003', false, 15, 'normal', '192.168.1.103', NOW() - INTERVAL '10 minutes', '{"volume": 100, "brightness": 90}'::jsonb, false, 'secure', 30.5728, 104.0668, true, '21:00', '06:00', true, '21:00', '06:00', 100, 90, false, 'v1.1.1');

-- certificates (证书) - 3条
INSERT INTO certificates (cert_id, cert_name, cert_type, serial_number, subject, issuer, thumbprint, not_before, not_after, status, cert_file, key_file, tenant_id, description, created_at, updated_at) VALUES
('CERT001', '设备SSL证书', 'device', 'SN-CERT-001', 'CN=device.smartepet.com', 'CN=RootCA,O=SmartEpet', 'THUMBPRINT001ABCDEF1234567890', NOW() - INTERVAL '30 days', NOW() + INTERVAL '365 days', 'active', '/certs/device001.crt', '/certs/device001.key', NULL, '用于设备MQTT通信加密', NOW(), NOW());

INSERT INTO certificates (cert_id, cert_name, cert_type, serial_number, subject, issuer, thumbprint, not_before, not_after, status, cert_file, key_file, tenant_id, description, created_at, updated_at) VALUES
('CERT002', 'API签名证书', 'api', 'SN-CERT-002', 'CN=api.smartepet.com', 'CN=RootCA,O=SmartEpet', 'THUMBPRINT002ABCDEF1234567890', NOW() - INTERVAL '60 days', NOW() + INTERVAL '300 days', 'active', '/certs/api001.crt', '/certs/api001.key', NULL, '用于API接口签名', NOW(), NOW());

INSERT INTO certificates (cert_id, cert_name, cert_type, serial_number, subject, issuer, thumbprint, not_before, not_after, status, cert_file, key_file, tenant_id, description, created_at, updated_at) VALUES
('CERT003', '租户专属证书', 'tenant', 'SN-CERT-003', 'CN=smartepet.com', 'CN=RootCA,O=SmartEpet', 'THUMBPRINT003ABCDEF1234567890', NOW() - INTERVAL '90 days', NOW() + INTERVAL '275 days', 'active', '/certs/tenant001.crt', '/certs/tenant001.key', (SELECT id FROM tenants LIMIT 1), '租户TENANT001专属证书', NOW(), NOW());
