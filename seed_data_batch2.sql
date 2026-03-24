-- 21. compliance_policies
INSERT INTO compliance_policies (name, description, policy_type, target_value, condition, severity, remediation_action, enabled, enforce_scope) VALUES
('Temp Monitor Policy', 'Pet body temp above 39.5C alert', 'temperature', '39.5', 'max', 3, 'vet_contact', true, 'all'),
('Heart Rate Policy', 'Pet heart rate above 180bpm alert', 'heart_rate', '180', 'max', 2, 'alert_owner', true, 'all'),
('Sleep Quality Policy', 'Daily sleep below 6 hours alert', 'sleep_hours', '6', 'min', 1, 'suggest_rest', true, 'all');

-- 22. geofence_rules
INSERT INTO geofence_rules (name, device_id, center_lat, center_lng, radius_meters, alert_on, severity, enabled, notify_ways) VALUES
('Home Area Fence', 'DEV001', 31.2304160, 121.4737010, 50.00, 'enter', 2, true, 'push,sms'),
('Office Area Fence', 'DEV002', 31.2350000, 121.4800000, 30.00, 'exit', 1, true, 'push'),
('Park Area Fence', 'DEV001', 31.2200000, 121.4600000, 100.00, 'both', 3, true, 'push,email');

-- 23. health_alerts
INSERT INTO health_alerts (alert_uuid, pet_uuid, device_id, alert_type, alert_level, title, description, trigger_value, threshold_value, unit, normal_range, suggestion, urgency, related_vitals, status, occurred_at, tenant_id) VALUES
(gen_random_uuid()::varchar, gen_random_uuid()::varchar, 'DEV001', 'temperature', 'critical', 'High Temperature Alert', 'Pet body temperature exceeded safe threshold', 40.2, 39.5, 'C', '36.5-39.0', 'Contact vet immediately', 9, '{"temp": 40.2, "timestamp": "2026-03-24T10:00:00Z"}', 'active', NOW() - INTERVAL '2 hours', 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
(gen_random_uuid()::varchar, gen_random_uuid()::varchar, 'DEV002', 'heart_rate', 'warning', 'Elevated Heart Rate', 'Pet heart rate above normal range', 185, 180, 'bpm', '60-140', 'Monitor and rest', 6, '{"hr": 185, "activity": "running"}', 'active', NOW() - INTERVAL '5 hours', 'a4b230b8-6ba4-42f5-978a-1bc17b01b956'),
(gen_random_uuid()::varchar, gen_random_uuid()::varchar, 'DEV003', 'activity', 'info', 'Low Activity Alert', 'Pet activity level below target', 1200, 3000, 'steps', '3000-8000', 'Encourage more play', 3, '{"steps": 1200, "goal": 3000}', 'acknowledged', NOW() - INTERVAL '1 day', '94d1c65e-426c-49c1-beac-c3c9dec69538');

-- 24. health_warnings
INSERT INTO health_warnings (warning_uuid, pet_uuid, device_id, category, level, title, description, symptoms, suggestions, trigger_data, source_type, status, priority, severity, start_time, tenant_id) VALUES
(gen_random_uuid()::varchar, gen_random_uuid()::varchar, 'DEV001', 'behavior', 'mild', 'Unusual Sleeping Pattern', 'Pet sleeping more than usual', '["excessive_sleep", "low_energy"]', '["monitor_sleep", "check_health"]', '{"hours_slept": 14, "normal": 8}', 'device_sensor', 'active', 3, 2, NOW() - INTERVAL '6 hours', 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
(gen_random_uuid()::varchar, gen_random_uuid()::varchar, 'DEV002', 'nutrition', 'moderate', 'Decreased Water Intake', 'Pet drinking less water today', '["reduced_thirst", "dry_mouth"]', '["fresh_water", "wet_food"]', '{"water_ml": 150, "normal": 400}', 'device_sensor', 'active', 5, 3, NOW() - INTERVAL '3 hours', 'a4b230b8-6ba4-42f5-978a-1bc17b01b956'),
(gen_random_uuid()::varchar, gen_random_uuid()::varchar, 'DEV001', 'behavior', 'mild', 'Reduced Appetite', 'Pet showing less interest in food', '["food_left", "weight_loss"]', '["try_different_food", "vet_consult"]', '{"food_g": 50, "normal": 200}', 'device_sensor', 'resolved', 2, 1, NOW() - INTERVAL '1 day', 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2');

-- 25. emotion_records
INSERT INTO emotion_records (subject_type, subject_id, emotion_type, intensity, source, confidence, context, trigger_event, recorded_at) VALUES
('pet', 1, 'happy', 0.85, 'ai_inference', 0.92, '{"activity": "play", "duration_min": 30}', 'Active play session', NOW() - INTERVAL '30 minutes'),
('pet', 2, 'anxious', 0.65, 'ai_inference', 0.78, '{"trigger": "loud_noise", "location": "living_room"}', 'Loud noise from outside', NOW() - INTERVAL '2 hours'),
('pet', 1, 'curious', 0.70, 'ai_inference', 0.85, '{"exploration": "new_area", "location": "garden"}', 'Exploring new environment', NOW() - INTERVAL '1 hour');

-- 26. emotion_response_configs (pet_id is bigint referencing device id from devices table)
INSERT INTO emotion_response_configs (pet_id, emotion_type, strategy, action_code, action_param, response_delay, enabled, threshold, cooldown) VALUES
(1, 'happy', 'reward', 'play_music', '{"music_type": "cheerful", "volume": 70}', 5000, true, 0.6, 120000),
(1, 'anxious', 'comfort', 'play_calm', '{"music_type": "classical", "volume": 50}', 2000, true, 0.5, 60000),
(2, 'sad', 'comfort', 'speak_kindly', '{"voice": "warm", "message": "You are loved"}', 3000, true, 0.4, 180000);

-- 27. embodied_ai_states (last_seen_objects and nearby_entities are text[])
INSERT INTO embodied_ai_states (state_key, entity_type, entity_id, position_x, position_y, position_z, orientation, location_name, perception_mode, alert_level, energy_level, mood, mood_intensity, current_goal, goal_progress, last_seen_objects, nearby_entities, environment_tags, capabilities, sensory_status, tenant_id) VALUES
('DEV001-living_room', 'pet', 'DEV001', 12.5000, 8.3000, 0.0000, 90.0000, 'Living Room', 'active', 'normal', 85.50, 'happy', 0.75, 'Explore kitchen area', 35.00, ARRAY['sofa:near', 'door:south'], ARRAY['human:owner', 'cat:neighbor'], ARRAY['indoor', 'familiar'], '{"navigation": true, "recognition": true}'::jsonb, '{"vision": "good", "audio": "excellent"}'::jsonb, 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
('DEV002-bedroom', 'pet', 'DEV002', 5.0000, 3.0000, 0.0000, 180.0000, 'Bedroom', 'active', 'normal', 92.00, 'relaxed', 0.60, 'Rest and sleep', 80.00, ARRAY['bed:under', 'window:east'], ARRAY['human:absent'], ARRAY['indoor', 'quiet'], '{"navigation": true, "recognition": true}'::jsonb, '{"vision": "good", "audio": "good"}'::jsonb, 'a4b230b8-6ba4-42f5-978a-1bc17b01b956'),
('DEV003-garden', 'pet', 'DEV003', 20.0000, 15.0000, 0.5000, 45.0000, 'Garden', 'exploring', 'low', 70.00, 'curious', 0.80, 'Map new area', 15.00, ARRAY['tree:north', 'pond:east'], ARRAY['bird:sparrow', 'insect:bee'], ARRAY['outdoor', 'familiar'], '{"navigation": true, "tracking": true}'::jsonb, '{"vision": "excellent", "audio": "good"}'::jsonb, '94d1c65e-426c-49c1-beac-c3c9dec69538');

-- 28. environment_maps
INSERT INTO environment_maps (map_key, entity_id, entity_type, map_name, map_type, resolution, scale, origin_x, origin_y, width, height, grid_data, obstacles, landmarks, regions, semantic_labels, room_names, confidence, explored_ratio, is_active, version, tenant_id) VALUES
('DEV001-home', 'DEV001', 'pet', 'Home Environment Map', '2d_grid', 0.5000, 100.00, 0.0000, 0.0000, 25.00, 20.00, '{"grid": [[0,0,0,1],[0,1,0,0]]}'::jsonb, '{"wall": [[0,0],[5,0]]}'::jsonb, '{"sofa": [2,3], "bed": [5,8]}'::jsonb, '{"living": [[0,0],[10,10]], "bedroom": [[10,10],[25,20]]}'::jsonb, ARRAY['living_room', 'bedroom', 'kitchen'], ARRAY['Living Room', 'Bedroom', 'Kitchen'], 0.92, 85.00, true, 3, 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
('DEV002-office', 'DEV002', 'pet', 'Office Environment Map', '2d_grid', 0.5000, 100.00, 0.0000, 0.0000, 15.00, 12.00, '{"grid": [[0,0,1],[1,0,0]]}'::jsonb, '{"desk": [[3,2],[7,5]]}'::jsonb, '{"chair": [5,4], "window": [1,1]}'::jsonb, '{"work_area": [[0,0],[15,12]]}'::jsonb, ARRAY['office', 'corridor'], ARRAY['Office', 'Corridor'], 0.88, 70.00, true, 2, 'a4b230b8-6ba4-42f5-978a-1bc17b01b956'),
('DEV003-garden-map', 'DEV003', 'pet', 'Garden Environment Map', '2d_grid', 1.0000, 50.00, -10.0000, -10.0000, 40.00, 30.00, '{"grid": [[0,0,0,0]]}'::jsonb, '{"pond": [[15,10],[20,15]]}'::jsonb, '{"tree": [5,5], "fountain": [20,20]}'::jsonb, '{"grass": [[0,0],[40,30]]}'::jsonb, ARRAY['grass', 'pond', 'path'], ARRAY['Grass Area', 'Pond Area', 'Path'], 0.75, 45.00, true, 1, '94d1c65e-426c-49c1-beac-c3c9dec69538');

-- 29. exploration_sessions (waypoints, visited_areas, discovered_objects are text[])
INSERT INTO exploration_sessions (session_key, entity_id, entity_type, strategy, exploration_goal, max_duration, max_distance, start_x, start_y, boundary_min_x, boundary_max_x, boundary_min_y, boundary_max_y, waypoints, visited_areas, discovered_objects, coverage_rate, path_length, new_discovery_count, status, progress, started_at, tenant_id) VALUES
(gen_random_uuid()::varchar, 'DEV001', 'pet', 'random_walk', 'Map living room area', 3600, 50.00, 0.0000, 0.0000, -5.0000, 25.0000, -5.0000, 20.0000, ARRAY['Living Room:2:3', 'Kitchen:8:5'], ARRAY['Living Room:full', 'Kitchen:partial'], ARRAY['toys:3', 'furniture:5'], 65.00, 35.50, 2, 'completed', 100.00, NOW() - INTERVAL '2 hours', 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
(gen_random_uuid()::varchar, 'DEV002', 'pet', 'boundary', 'Explore bedroom boundaries', 1800, 30.00, 5.0000, 3.0000, 0.0000, 15.0000, 0.0000, 12.0000, ARRAY['Bedroom:5:3', 'Corridor:12:6'], ARRAY['Bedroom:full'], ARRAY['window:1', 'door:2'], 45.00, 22.00, 1, 'completed', 100.00, NOW() - INTERVAL '5 hours', 'a4b230b8-6ba4-42f5-978a-1bc17b01b956'),
(gen_random_uuid()::varchar, 'DEV003', 'pet', 'frontier', 'Discover new garden areas', 7200, 200.00, 20.0000, 15.0000, -10.0000, 40.0000, -10.0000, 30.0000, ARRAY['Grass:10:10', 'Pond:17:12'], ARRAY['Grass:partial'], ARRAY['flower:5', 'insect:8'], 30.00, 85.00, 5, 'active', 30.00, NOW() - INTERVAL '30 minutes', '94d1c65e-426c-49c1-beac-c3c9dec69538');

-- 30. simulation_runs
INSERT INTO simulation_runs (run_id, name, env_id, pet_id, scenario_config, result_data, status, duration, metrics_summary, create_user_id, started_at, completed_at) VALUES
(gen_random_uuid()::varchar, 'Indoor Navigation Test', gen_random_uuid()::varchar, 'DEV001', '{"scenario": "obstacle_avoidance", "difficulty": "medium"}', '{"success_rate": 0.85, "avg_time": 120}', 'completed', 180000, '{"path_efficiency": 0.82, "collision_count": 2}', 1, NOW() - INTERVAL '1 day', NOW() - INTERVAL '23 hours'),
(gen_random_uuid()::varchar, 'Outdoor Exploration Sim', gen_random_uuid()::varchar, 'DEV002', '{"scenario": "exploration", "area": "garden", "duration": 3600}', '{"coverage": 0.72, "discoveries": 8}', 'completed', 3600000, '{"exploration_rate": 0.72, "new_areas": 5}', 3, NOW() - INTERVAL '3 days', NOW() - INTERVAL '2 days 23 hours'),
(gen_random_uuid()::varchar, 'Multi-Agent Interaction', gen_random_uuid()::varchar, 'DEV003', '{"scenario": "social", "agents": 2}', '{"interaction_count": 15, "cooperation_score": 0.78}', 'running', 0, '{"current_phase": "exploration", "team_score": 0.65}', 4, NOW() - INTERVAL '1 hour', NULL);

-- 31. policy_configs
INSERT INTO policy_configs (name, config_type, sub_type, description, config_data, enabled, version) VALUES
('Data Retention Policy', 'data', 'retention', 'Pet data retention period configuration', '{"retention_days": 365, "archive_after": 90}'::jsonb, true, 1),
('Notification Throttle', 'notification', 'throttle', 'Max notifications per hour per device', '{"max_per_hour": 10, "burst": 20}'::jsonb, true, 2),
('AI Model Update Policy', 'ai', 'model_update', 'AI model auto-update configuration', '{"auto_update": true, "min_confidence": 0.85, "staging_days": 7}'::jsonb, true, 1);

-- 32. notification_channels
INSERT INTO notification_channels (channel_type, name, enabled, smtp_host, smtp_port, smtp_user, smtp_from, priority, webhook_url, webhook_method, health_status, is_default) VALUES
('email', 'Main Email Channel', true, 'smtp.example.com', 587, 'notifications@petmdm.com', 'noreply@petmdm.com', 10, NULL, NULL, 'healthy', true),
('webhook', 'Alert Webhook', true, NULL, NULL, NULL, NULL, 5, 'https://api.example.com/webhooks/alerts', 'POST', 'healthy', false),
('sms', 'Emergency SMS', false, NULL, NULL, NULL, NULL, 20, NULL, NULL, 'unknown', false);

-- 33. alert_notifications (needs alert_id from health_alerts)
INSERT INTO alert_notifications (alert_id, alert_type, status, recipient, subject, content, sent_at)
SELECT id, 'health_alert', 'sent', 'owner@example.com', 'High Temperature Alert', 'Your pet body temperature is 40.2C, please check immediately.', NOW() - INTERVAL '1 hour'
FROM health_alerts LIMIT 1;

INSERT INTO alert_notifications (alert_id, alert_type, status, recipient, subject, content, sent_at)
SELECT id, 'health_alert', 'pending', 'operator1@example.com', 'Elevated Heart Rate', 'Pet heart rate at 185bpm, above normal range.', NULL
FROM health_alerts WHERE alert_type = 'heart_rate' LIMIT 1;

INSERT INTO alert_notifications (alert_id, alert_type, status, recipient, subject, content, error_msg, sent_at)
SELECT id, 'health_alert', 'failed', 'admin@example.com', 'Low Activity Alert', 'Pet activity below target for today.', 'SMTP connection timeout', NOW() - INTERVAL '30 minutes'
FROM health_alerts WHERE alert_type = 'activity' LIMIT 1;

-- 34. api_permissions
INSERT INTO api_permissions (api_path, api_name, method, permission_code, menu_id, status, tenant_id) VALUES
('/api/v1/devices', 'Device Management', 'GET', 'device:read', 1, 1, 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
('/api/v1/devices/:id/command', 'Device Command', 'POST', 'device:command', 1, 1, 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
('/api/v1/health/alerts', 'Health Alerts', 'GET', 'health:read', 2, 1, 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
('/api/v1/simulation/runs', 'Simulation Runs', 'POST', 'simulation:write', 3, 1, 'a4b230b8-6ba4-42f5-978a-1bc17b01b956'),
('/api/v1/emotion/records', 'Emotion Records', 'GET', 'emotion:read', 4, 1, 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2');

-- 35. permission_groups
INSERT INTO permission_groups (name, code, description, permissions, status) VALUES
('Device Operators', 'device_operator', 'Can manage devices and send commands', '["device:read", "device:write", "device:command"]'::jsonb, 1),
('Health Monitors', 'health_monitor', 'Can view health data and receive alerts', '["health:read", "alert:receive", "notification:manage"]'::jsonb, 1),
('Simulation Users', 'simulation_user', 'Can run simulations and view results', '["simulation:read", "simulation:write", "environment:read"]'::jsonb, 1);

-- 36. ldap_configs
INSERT INTO ldap_configs (config_name, host, port, base_dn, bind_dn, use_ssl, use_tls, user_filter, group_filter, sync_interval, is_enabled, status, tenant_id) VALUES
('Corporate LDAP', 'ldap.corp.example.com', 636, 'dc=corp,dc=example,dc=com', 'cn=admin,dc=corp,dc=example,dc=com', true, false, '(uid=%s)', '(member=%s)', 3600, true, 'active', 'e6cbcb82-9bd6-4803-8bf7-b4b1af8eaec2'),
('Demo LDAP', 'ldap.demo.local', 389, NULL, NULL, false, true, '(sAMAccountName=%s)', '(cn=%s)', 7200, false, 'inactive', 'a4b230b8-6ba4-42f5-978a-1bc17b01b956');

-- 37. child_mode_configs
INSERT INTO child_mode_configs (user_id, device_id, is_enabled, content_filter_level, allowed_categories, daily_time_limit, session_duration, break_duration, allowed_start_time, allowed_end_time, emergency_contact, pin_code) VALUES
(3, 'DEV002', true, 'strict', 'education,entertainment', 120, 30, 10, '08:00', '20:00', '13800001002', '1234'),
(4, 'DEV003', true, 'moderate', 'education,entertainment,games', 180, 45, 15, '09:00', '18:00', '13800001003', '5678');

-- 38. elderly_care_configs
INSERT INTO elderly_care_configs (user_id, device_id, is_enabled, health_monitor_enabled, heart_rate_alert_high, heart_rate_alert_low, activity_goal, sleep_monitoring, medication_reminders, medication_times, medication_names, companion_enabled, interaction_frequency, fall_detection_enabled, emergency_contact_name, emergency_contact_phone) VALUES
(3, 'DEV001', true, true, 110, 55, 5000, true, true, '08:00,12:00,20:00', 'Vitamin D,Omega-3', true, 'frequent', true, 'Zhang Wei', '13800001002'),
(4, 'DEV002', true, true, 105, 50, 4000, true, false, '09:00,21:00', 'Blood Pressure Med', true, 'normal', true, 'Li Hua', '13800001003');

-- 39. sys_configs
INSERT INTO sys_configs (config_key, config_val, config_type, remark, status) VALUES
('system_version', 'v2.1.0', 'system', 'Current system version', 1),
('max_devices_per_user', '10', 'business', 'Maximum devices allowed per user account', 1),
('data_retention_days', '365', 'data', 'Default data retention period in days', 1),
('session_timeout_minutes', '30', 'security', 'User session timeout in minutes', 1),
('mqtt_broker_url', 'tcp://mqtt:1883', 'mqtt', 'MQTT broker connection URL', 1);

-- 40. sys_dictionaries (unique on type column only - one row per type)
INSERT INTO sys_dictionaries (type, name, label, value, sort, status, remark) VALUES
('device_status', 'Device Status', 'device_status', 'online', 1, 1, 'Device is online'),
('alert_level_critical', 'Alert Level Critical', 'alert_level_critical', 'critical', 1, 1, 'Critical alert level'),
('emotion_type_happy', 'Emotion Happy', 'emotion_type_happy', 'happy', 1, 1, 'Pet is happy'),
('content_filter_strict', 'Content Filter Strict', 'content_filter_strict', 'strict', 1, 1, 'Strict content filter'),
('simulation_status', 'Simulation Status', 'simulation_status', 'running', 1, 1, 'Simulation is running');
