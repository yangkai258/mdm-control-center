-- =====================
-- 第6批：AI/健康
-- =====================

-- ai_models (AI模型) - 3条
INSERT INTO ai_models (model_key, name, description, provider, model_type, model_size, file_path, file_size, checksum, config, capabilities, quota_daily, quota_monthly, price_per1_k, status, deployed_at, deployed_by, org_id, create_user_id, created_at, updated_at) VALUES
('pet_emotion_v1', '宠物情绪识别模型', '基于深度学习的宠物情绪识别模型，支持识别开心、悲伤、愤怒、恐惧等情绪', 'openai', 'emotion_detection', '1.2G', '/models/pet_emotion_v1.pt', 1288490188, 'sha256:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2', '{"temperature": 0.7, "max_tokens": 512}'::jsonb, '{"emotion_detection": true, "sentiment_analysis": true}'::jsonb, 10000, 100000, 0.01, 'deployed', NOW() - INTERVAL '7 days', 1, 1, 1, NOW(), NOW()),
('pet_health_v2', '宠物健康分析模型', '宠物健康状况分析模型，通过生命体征数据评估宠物健康指数', 'anthropic', 'health_analysis', '2.5G', '/models/pet_health_v2.pt', 2684354560, 'sha256:b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d', '{"temperature": 0.5, "max_tokens": 1024}'::jsonb, '{"health_scoring": true, "disease_prediction": true}'::jsonb, 5000, 50000, 0.02, 'deployed', NOW() - INTERVAL '14 days', 1, 1, 1, NOW(), NOW()),
('pet_conversation_v1', '宠物对话生成模型', '用于生成宠物陪伴对话的大语言模型', 'openai', 'conversation', '7B', '/models/pet_conv_v1.bin', 7516192768, 'sha256:c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e', '{"temperature": 0.9, "max_tokens": 2048}'::jsonb, '{"dialogue_generation": true, "personality_adaptation": true}'::jsonb, 20000, 200000, 0.015, 'training', NULL, NULL, 1, 1, NOW(), NOW());

-- ai_model_versions_v2 (模型版本) - 3条
INSERT INTO ai_model_versions_v2 (model_id, version, model_name, description, status, model_path, config, metrics, total_shards, verified_shards, is_sharded, rollback_from, rollback_to, published_by, published_at, org_id, create_user_id, created_at, updated_at) VALUES
(1, 'v1.0.0', 'Pet Emotion v1.0', '宠物情绪识别模型正式版', 'published', '/models/pet_emotion_v1/v1.0.0/', '{"batch_size": 32, "learning_rate": 0.001}'::jsonb, '{"accuracy": 0.92, "f1_score": 0.89}'::jsonb, 4, 4, true, NULL, NULL, 1, NOW() - INTERVAL '7 days', 1, 1, NOW(), NOW()),
(2, 'v2.0.0', 'Pet Health v2.0', '宠物健康分析模型升级版', 'published', '/models/pet_health_v2/v2.0.0/', '{"batch_size": 16, "learning_rate": 0.0005}'::jsonb, '{"accuracy": 0.88, "f1_score": 0.85}'::jsonb, 8, 8, true, NULL, NULL, 1, NOW() - INTERVAL '14 days', 1, 1, NOW(), NOW()),
(3, 'v0.9.0', 'Pet Conv v0.9', '宠物对话生成模型测试版', 'draft', '/models/pet_conv_v1/v0.9.0/', '{"batch_size": 8, "learning_rate": 0.0001}'::jsonb, '{"perplexity": 12.5}'::jsonb, 16, 0, true, NULL, 'v1.0.0', NULL, NULL, 1, 1, NOW(), NOW());

-- pet_health_records (宠物健康记录) - 3条
INSERT INTO pet_health_records (record_uuid, pet_uuid, record_type, record_date, title, hospital, vet_name, diagnosis, treatment, prescription, medications, cost, vaccine_name, next_due_date, weight, notes, attachments, is_insured, insurance_claim_uuid, tenant_id, created_at, updated_at) VALUES
('HR001', 'DEV001', 'checkup', '2026-03-10'::date, '年度体检报告', '宠物中心医院', '陈医生', '健康状况良好', '建议增加运动量', '常规营养补充剂', ARRAY['维生素片', '钙片'], 350.00, '狂犬疫苗', '2027-03-10'::timestamp, 8.5, '体重略偏轻，建议调整饮食', ARRAY[]::text[], false, NULL, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('HR002', 'DEV002', 'vaccination', '2026-02-15'::date, '疫苗接种记录', '爱心宠物诊所', '林医生', '正常', '完成疫苗接种', '无', ARRAY['妙三多疫苗'], 180.00, '妙三多疫苗', '2027-02-15'::timestamp, 4.2, '疫苗接种顺利完成', ARRAY[]::text[], true, NULL, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('HR003', 'DEV003', 'surgery', '2026-01-20'::date, '绝育手术记录', '宠物中心医院', '王医生', '手术顺利完成', '术后护理观察3天', '消炎药、止痛药', ARRAY['消炎针', '止痛药'], 1200.00, NULL, NULL, 12.3, '恢复良好', ARRAY[]::text[], true, 'CLM001', (SELECT id FROM tenants LIMIT 1), NOW(), NOW());

-- vital_records (生命体征) - 3条
INSERT INTO vital_records (record_uuid, pet_uuid, device_id, vital_type, value, unit, min_value, max_value, avg_value, normal_range_min, normal_range_max, is_abnormal, abnormal_level, severity, recorded_at, data_source, metadata, tenant_id, created_at, updated_at) VALUES
('VR001', 'DEV001', 'DEV001', 'heart_rate', 85.0, 'bpm', 60.0, 120.0, 82.5, 60.0, 120.0, false, NULL, 0, NOW(), 'device', '{"activity": "resting"}'::jsonb, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('VR002', 'DEV002', 'DEV002', 'body_temperature', 38.5, 'celsius', 37.5, 39.5, 38.5, 37.5, 39.5, false, NULL, 0, NOW(), 'device', '{"activity": "normal"}'::jsonb, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('VR003', 'DEV003', 'DEV003', 'heart_rate', 145.0, 'bpm', 60.0, 120.0, 130.0, 60.0, 120.0, true, 'high', 2, NOW(), 'device', '{"activity": "excited"}'::jsonb, (SELECT id FROM tenants LIMIT 1), NOW(), NOW());

-- exercise_records (运动记录) - 3条
INSERT INTO exercise_records (record_uuid, pet_uuid, device_id, exercise_type, start_time, end_time, duration, duration_minutes, steps, distance, distance_unit, calories_burned, avg_heart_rate, max_heart_rate, min_heart_rate, avg_speed, max_speed, elevation_gain, route_data, intensity, intensity_score, quality_score, weather, temperature, notes, tags, data_source, is_goal_achieved, goal_id, tenant_id, created_at, updated_at) VALUES
('ER001', 'DEV001', 'DEV001', 'walk', '2026-03-24 08:00:00'::timestamp, '2026-03-24 08:45:00'::timestamp, 2700, 45, 3500, 2.5, 'km', 120.5, 95, 120, 75, 3.3, 5.2, 50, '{"points": []}'::jsonb, 'moderate', 75, 88, 'sunny', 18.5, '上午散步，状态良好', 'morning,walk,outdoor', 'device', true, NULL, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('ER002', 'DEV002', 'DEV002', 'play', '2026-03-24 14:00:00'::timestamp, '2026-03-24 14:30:00'::timestamp, 1800, 30, 0, 0, 'km', 80.0, 110, 130, 90, 0, 0, 0, NULL, 'light', 60, 82, 'cloudy', 22.0, '室内玩耍', 'indoor,play', 'device', false, NULL, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('ER003', 'DEV003', 'DEV003', 'run', '2026-03-24 17:00:00'::timestamp, '2026-03-24 17:20:00'::timestamp, 1200, 20, 5000, 3.0, 'km', 200.0, 140, 160, 120, 9.0, 12.0, 80, '{"points": []}'::jsonb, 'vigorous', 85, 90, 'clear', 20.0, '户外跑步训练', 'outdoor,run,training', 'device', true, NULL, (SELECT id FROM tenants LIMIT 1), NOW(), NOW());
