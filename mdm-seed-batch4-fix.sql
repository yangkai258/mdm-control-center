-- MDM Database Test Data - Batch 4 Part 2 (Corrected Schemas)
-- Tables that need schema corrections based on actual DB structure

-- ============================================================================
-- GROUP A: Pet Related - Corrected
-- ============================================================================

-- pet_lost_reports (corrected schema)
INSERT INTO pet_lost_reports (id, report_uuid, pet_uuid, pet_name, species, breed, color, gender, age, last_location, lost_time, status, reward, contact_name, contact_phone, contact_wechat, description, photo_urls, reporter_id, spread_radius, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'RPT_LOST_001', 'PET001', 'Orange', 'cat', 'Tabby', 'Orange', 'male', '2 years', '{"lat": 31.2304, "lng": 121.4740, "address": "Century Park"}', '2024-03-15 14:00:00+08', 'searching', '500元', 'Zhang San', '13812345678', 'zhangsan', 'Orange tabby cat with blue collar, very friendly', ARRAY['https://photo.example.com/lost/001.jpg'], 1, 10.00, NULL, NOW(), NOW(), NULL),
(2, 'RPT_LOST_002', 'PET002', 'Max', 'dog', 'Golden Retriever', 'Golden', 'male', '3 years', '{"lat": 31.2204, "lng": 121.5440, "address": "Jing An Park"}', '2024-03-18 09:00:00+08', 'found', '1000元', 'Li Si', '13987654321', 'lisi123', 'Large golden retriever, well-trained', ARRAY['https://photo.example.com/lost/002.jpg'], 1, 15.00, NULL, NOW(), NOW(), NULL);

-- pet_finder_reports (corrected schema)
INSERT INTO pet_finder_reports (id, pet_id, user_id, report_type, title, description, last_seen_at, last_seen_lat, last_seen_lng, last_seen_addr, contact_name, contact_phone, reward, reward_memo, photos, status, resolved_at, view_count, alert_radius, created_at, updated_at) VALUES
(1, 1, 1, 'lost', 'Lost Orange Tabby Cat', 'Orange tabby cat with blue collar lost near Century Park', '2024-03-15 14:00:00+08', 31.2304, 121.4740, 'Century Park, Pudong', 'Zhang San', '13812345678', 500.00, 'Reward offered', ARRAY['photo1.jpg', 'photo2.jpg'], 'active', NULL, 150, 5.00, NOW(), NOW()),
(2, 2, 1, 'sighting', 'Sighting of Orange Cat', 'Orange cat spotted near metro station', '2024-03-16 10:00:00+08', 31.2254, 121.4540, 'Nanjing Road Metro', 'Wang Wu', '13711112222', 0.00, NULL, ARRAY['sighting1.jpg'], 'verified', NULL, 50, 3.00, NOW(), NOW());

-- pet_finder_sightings (corrected schema)
INSERT INTO pet_finder_sightings (id, report_id, reporter_id, sighted_at, sighted_lat, sighted_lng, sighted_addr, description, pet_status, photo_url, contact_name, contact_phone, is_verified, created_at) VALUES
(1, 1, 1, '2024-03-15 16:00:00+08', 31.2254, 121.4540, 'Jing An Park', 'Orange cat resting under bench', 'safe', 'https://photo.example.com/sight/001.jpg', 'John Doe', '13900001111', true, NOW()),
(2, 1, 1, '2024-03-15 18:30:00+08', 31.2304, 121.4740, 'West Nanjing Road', 'Orange cat chasing pigeons', 'active', 'https://photo.example.com/sight/002.jpg', 'Jane Smith', '13900002222', false, NOW());

-- pet_finder_alerts (corrected schema)
INSERT INTO pet_finder_alerts (id, report_id, alert_type, recipient_id, sent_at, status, error_msg, created_at) VALUES
(1, 1, 'sms', 1, NOW(), 'sent', NULL, NOW()),
(2, 1, 'app', 1, NOW(), 'sent', NULL, NOW());

-- pet_products (corrected schema)
INSERT INTO pet_products (id, product_uuid, name, brand, category_id, category_name, description, price, original_price, stock, unit, images, specs, tags, rating, sales_count, view_count, is_active, is_featured, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'PROD001', 'Premium Cat Food 400g', 'Royal Canin', 1, 'Cat Food', 'Complete nutrition for adult cats', 128.00, 158.00, 500, 'bag', 'https://img.example.com/food/001.jpg', '{"weight": "400g"}', 'cat,food,adult', 4.80, 1000, 5000, true, true, NULL, NOW(), NOW(), NULL),
(2, 'PROD002', 'Interactive Laser Toy', 'Catit', 2, 'Pet Toys', 'USB rechargeable laser toy for cats', 89.00, 99.00, 200, 'piece', 'https://img.example.com/toy/001.jpg', '{"color": "white"}', 'cat,toy,laser', 4.60, 500, 2500, true, false, NULL, NOW(), NOW(), NULL);

-- pet_shop_orders (corrected schema)
INSERT INTO pet_shop_orders (id, order_uuid, order_no, pet_uuid, total_amount, discount_amount, pay_amount, pay_method, pay_status, pay_at, status, shipping_address, shipping_name, shipping_phone, express_no, remarks, owner_id, household_id, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'ORD_UUID_001', 'ORD20240320001', 'PET001', 256.00, 0.00, 256.00, 'wechat_pay', 'paid', '2024-03-20 10:05:00+08', 'shipped', '123 Main St, Shanghai', 'Zhang San', '13812345678', 'SF123456789', NULL, 1, 1, NULL, NOW(), NOW(), NULL),
(2, 'ORD_UUID_002', 'ORD20240321001', 'PET001', 89.00, 0.00, 89.00, 'alipay', 'paid', '2024-03-21 15:35:00+08', 'pending', '123 Main St, Shanghai', 'Zhang San', '13812345678', NULL, NULL, 1, 1, NULL, NOW(), NOW(), NULL);

-- ============================================================================
-- GROUP B: Member Related - Corrected
-- ============================================================================

-- member_tag_records (corrected schema)
INSERT INTO member_tag_records (id, member_id, tag_id, action, operator, created_at) VALUES
(1, 1, 1, 'add', 'admin', NOW()),
(2, 1, 2, 'add', 'system', NOW());

-- member_operation_records (corrected schema)
INSERT INTO member_operation_records (id, member_id, operation, detail, operator, ip, created_at) VALUES
(1, 1, 'login', 'Member logged in successfully', 'system', '192.168.1.100', NOW()),
(2, 1, 'update_profile', 'Updated phone number', 'member', '192.168.1.100', NOW());

-- member_orders (corrected schema)
INSERT INTO member_orders (id, order_no, member_id, order_type, amount, points_earned, pay_type, status, remark, created_at, updated_at) VALUES
(1, 'MEM_ORD_001', 1, 1, 256.00, 256, 1, 4, 'First order', NOW(), NOW()),
(2, 'MEM_ORD_002', 1, 1, 158.00, 158, 2, 2, NULL, NOW(), NOW());

-- order_items (corrected schema)
INSERT INTO order_items (id, product_uuid, product_name, product_image, price, quantity, specs) VALUES
(1, 'PROD001', 'Premium Cat Food 400g', 'https://img.example.com/food/001.jpg', 128.00, 2, '{"weight": "400g"}'),
(2, 'PROD002', 'Interactive Laser Toy', 'https://img.example.com/toy/001.jpg', 89.00, 1, '{"color": "white"}');

-- member_upgrade_rules (corrected schema)
INSERT INTO member_upgrade_rules (id, from_level, to_level, points_threshold, amount_threshold, points_reward, status, created_at, updated_at) VALUES
(1, 1, 2, 5000, 0, 500, 1, NOW(), NOW()),
(2, 2, 3, 10000, 10000, 1000, 1, NOW(), NOW());

-- member_upgrade_records (corrected schema)
INSERT INTO member_upgrade_records (id, member_id, from_level, to_level, reason, operator, created_at) VALUES
(1, 1, 1, 2, 'Points threshold reached', 'system', NOW()),
(2, 1, 2, 3, 'Manual upgrade by admin', 'admin', NOW());

-- ============================================================================
-- GROUP C: Insurance - Corrected
-- ============================================================================

-- insurance_claims (corrected schema)
INSERT INTO insurance_claims (id, claim_uuid, claim_no, product_uuid, pet_uuid, owner_id, incident_date, incident_type, incident_desc, hospital_name, diagnosis, claim_amount, approved_amount, rejection_reason, status, reviewer_id, review_notes, paid_at, policy_no, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'CLM_UUID_001', 'CLM202403001', 'INS001', 'PET001', 1, '2024-03-10', 'illness', 'Respiratory infection', 'Happy Pet Hospital', 'Upper respiratory infection', 5000.00, 4500.00, NULL, 'approved', 1, 'Claim approved', '2024-03-18 00:00:00+08', 'POL_001', NULL, NOW(), NOW(), NULL),
(2, 'CLM_UUID_002', 'CLM202403002', 'INS001', 'PET001', 1, '2024-03-05', 'accident', 'Leg fracture from fall', 'City Vet Hospital', 'Fractured leg', 8000.00, 7200.00, NULL, 'approved', 1, 'Surgery claim approved', '2024-03-15 00:00:00+08', 'POL_001', NULL, NOW(), NOW(), NULL);

-- insurance_claim_documents (corrected schema)
INSERT INTO insurance_claim_documents (id, doc_uuid, claim_uuid, doc_type, file_name, file_url, file_size, mime_type, description, is_verified, verified_by, verified_at, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'DOC_UUID_001', 'CLM_UUID_001', 'invoice', 'invoice_001.pdf', 'https://docs.example.com/invoice/001.pdf', 1024000, 'application/pdf', 'Medical invoice', true, 1, NOW(), NULL, NOW(), NOW(), NULL),
(2, 'DOC_UUID_002', 'CLM_UUID_001', 'diagnosis', 'diagnosis_001.pdf', 'https://docs.example.com/diagnosis/001.pdf', 512000, 'application/pdf', 'Diagnosis report', true, 1, NOW(), NULL, NOW(), NOW(), NULL);

-- ============================================================================
-- GROUP D: OTA - Corrected
-- ============================================================================

-- firmware_optimization_configs (corrected schema)
INSERT INTO firmware_optimization_configs (id, device_id, optimization_type, config_json, is_enabled, is_applied, applied_at, applied_version, created_by, created_at, updated_at, deleted_at) VALUES
(1, 'DEV001', 'battery', '{"sleep_interval": 300, "power_mode": "aggressive"}', true, true, NOW(), 'v1.1.0', 'admin', NOW(), NOW(), NULL),
(2, 'DEV002', 'network', '{"max_retries": 5, "timeout_ms": 30000}', true, false, NULL, NULL, 'admin', NOW(), NOW(), NULL);

-- ============================================================================
-- GROUP E: AI - Corrected
-- ============================================================================

-- ai_training (corrected - removed columns that don't exist)
INSERT INTO ai_training (id, task_key, name, description, model_id, base_model_key, training_type, dataset_path, dataset_size, validation_path, hyper_params, resource_config, output_path, status, priority, progress, epoch, total_epochs, current_step, total_steps, loss, metrics, logs_path, error_message, started_at, completed_at, estimated_time, queued_at, org_id, create_user_id, created_at, updated_at, deleted_at) VALUES
(1, 'train_pet_emotion_v1', 'Pet Emotion Recognition v1', 'Train model to recognize pet emotions', 1, 'base_emotion_v3', 'transfer_learning', '/data/datasets/pet_emotion', 50000, '/data/val/pet_emotion', '{"lr": 0.001, "batch_size": 32}', '{"gpu": 2, "memory_gb": 32}', '/models/output/pet_emotion_v1', 'completed', 10, 100, 50, 50, 5000, 5000, 0.023, '{"accuracy": 0.95, "f1": 0.94}', '/logs/train_pet_emotion_v1', NULL, '2024-03-10 08:00:00+08', '2024-03-12 16:00:00+08', 180000, '2024-03-10 07:00:00+08', 1, 1, NOW(), NOW(), NULL),
(2, 'train_health_detection', 'Pet Health Anomaly Detection', 'Detect health anomalies from vital signs', 2, 'base_health_v2', 'fine_tuning', '/data/datasets/health_anomaly', 30000, '/data/val/health_anomaly', '{"lr": 0.0005, "batch_size": 16}', '{"gpu": 4, "memory_gb": 64}', '/models/output/health_detection', 'training', 8, 65, 30, 100, 3000, 10000, 0.045, '{"precision": 0.92, "recall": 0.89}', '/logs/train_health_detection', NULL, '2024-03-18 10:00:00+08', NULL, 360000, '2024-03-18 09:00:00+08', 1, 1, NOW(), NOW(), NULL);

-- ai_inference (corrected)
INSERT INTO ai_inference (id, inference_key, model_id, model_key, mode, input_tokens, output_tokens, total_tokens, input_data, output_data, prompt, response, error_message, status, latency_ms, cost, stream_enabled, extra, started_at, completed_at, device_id, user_id, org_id, create_user_id, created_at, updated_at, deleted_at) VALUES
(1, 'INF001', 1, 'emotion_v1', 'realtime', 100, 50, 150, '{"image": "/data/input/img_001.jpg"}', '{"emotion": "happy", "confidence": 0.95}', NULL, NULL, NULL, 'completed', 120, 0.05, false, NULL, NOW(), NOW(), 'DEV001', 1, 1, 1, NOW(), NOW(), NULL),
(2, 'INF002', 2, 'health_v2', 'batch', 200, 100, 300, '{"vitals": {"heart_rate": 120}}', '{"anomaly": false, "score": 0.12}', NULL, NULL, NULL, 'completed', 85, 0.08, false, NULL, NOW(), NOW(), 'DEV001', 1, 1, 1, NOW(), NOW(), NULL);

-- ai_audit_logs (corrected)
INSERT INTO ai_audit_logs (id, action, module, resource_type, resource_id, model_id, model_key, user_id, username, ip, user_agent, status, error_msg, request_method, request_path, request_body, response_code, duration, metadata, fairness_score, bias_detected, tenant_id, org_id, created_at) VALUES
(1, 'inference', 'ai_service', 'model', '1', 1, 'emotion_v1', 1, 'admin', '192.168.1.100', 'Mozilla/5.0', 1, NULL, 'POST', '/api/ai/inference', '{"model": "emotion_v1"}', 200, 120, NULL, 0.95, false, NULL, 1, NOW()),
(2, 'train', 'ai_service', 'model', '2', 2, 'health_v2', 1, 'admin', '192.168.1.100', 'Mozilla/5.0', 1, NULL, 'POST', '/api/ai/train', '{"model": "health_v2"}', 200, 5000, NULL, NULL, false, NULL, 1, NOW());

-- ai_audit_reports (corrected)
INSERT INTO ai_audit_reports (id, report_key, report_type, model_id, model_key, period_start, period_end, summary, findings, metrics, recommendations, risk_level, generated_by, generated_at, tenant_id, org_id, created_at) VALUES
(1, 'AUDIT_2024_W11', 'weekly', 1, 'emotion_v1', '2024-03-11', '2024-03-17', 'Weekly audit summary', '{"inference_count": 15000, "avg_latency": 120}', '{"accuracy": 0.95, "f1": 0.94}', 'Consider more training data', 'low', 1, NOW(), NULL, 1, NOW()),
(2, 'AUDIT_2024_W12', 'weekly', 2, 'health_v2', '2024-03-18', '2024-03-24', 'Health model audit', '{"inference_count": 8000, "anomaly_detected": 45}', '{"precision": 0.92, "recall": 0.89}', 'Monitor senior pet accuracy', 'medium', 1, NOW(), NULL, 1, NOW());

-- ai_fairness_tests (corrected)
INSERT INTO ai_fairness_tests (id, test_key, name, description, test_type, model_id, model_key, status, progress, config, test_data, results, metrics, report_path, error_message, started_at, completed_at, org_id, create_user_id, created_at, updated_at, deleted_at) VALUES
(1, 'FAIR_TEST_001', 'Demographic Parity Test', 'Test demographic parity across species', 'demographic_parity', 1, 'emotion_v1', 'completed', 100, '{"protected_attrs": ["species"]}', '{"sample_size": 1000}', '{"pass": true, "score": 0.98}', '{"parity_diff": 0.02}', '/reports/fairness/test001.pdf', NULL, NOW(), NOW(), 1, 1, NOW(), NOW(), NULL),
(2, 'FAIR_TEST_002', 'Equalized Odds Test', 'Test equalized odds across age groups', 'equalized_odds', 2, 'health_v2', 'running', 50, '{"protected_attrs": ["age"]}', '{"sample_size": 2000}', '{"pass": false, "score": 0.87}', '{"odds_diff": 0.07}', NULL, NULL, NOW(), NULL, 1, 1, NOW(), NOW(), NULL);

-- ai_fairness_metrics (need to check schema - might not have id column)
-- INSERT INTO ai_fairness_metrics VALUES...

-- ai_deploy_sharded (need to check schema)
-- INSERT INTO ai_deploy_sharded VALUES...

-- ai_model_deploy_history (need to check schema)
-- INSERT INTO ai_model_deploy_history VALUES...

-- ai_bias_detections (need to check schema)
-- INSERT INTO ai_bias_detections VALUES...

-- model_shards (need to check schema)
-- INSERT INTO model_shards VALUES...

-- ============================================================================
-- GROUP F: Digital Twin - These should already have correct schema from batch 1
-- ============================================================================

-- vital_trends
INSERT INTO vital_trends (pet_uuid, vital_type, current_value, avg_value, min_value, max_value, trend, trend_rate, is_abnormal, abnormal_level, last_updated) VALUES
('PET001', 'heart_rate', 85.5, 82.3, 65.0, 120.0, 'stable', 0.02, false, NULL, NOW()),
('PET001', 'temperature', 38.8, 38.5, 37.5, 39.5, 'rising', 0.05, false, NULL, NOW()),
('PET001', 'activity', 4500.0, 4200.0, 1000.0, 8000.0, 'increasing', 0.08, false, NULL, NOW());

-- health_alert_rules
INSERT INTO health_alert_rules (id, rule_uuid, pet_uuid, rule_name, alert_type, condition, alert_level, title_template, suggestion, cooldown_period, is_enabled, priority, notify_channels, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'RULE001', 'PET001', 'High Heart Rate Alert', 'heart_rate', '{"operator": ">", "value": 100, "duration": 300}', 'warning', 'Heart Rate Alert', 'Please check your pet immediately', 3600, true, 10, ARRAY['app', 'sms'], NULL, NOW(), NOW(), NULL),
(2, 'RULE002', 'PET001', 'Fever Alert', 'temperature', '{"operator": ">", "value": 39.5, "duration": 600}', 'critical', 'Fever Detected', 'Seek veterinary care', 1800, true, 5, ARRAY['app', 'sms', 'email'], NULL, NOW(), NOW(), NULL);

-- health_monitor_settings
INSERT INTO health_monitor_settings (id, profile_id, setting_id, heart_rate_monitor, heart_rate_min, heart_rate_max, bp_monitor, bp_systolic_min, bp_systolic_max, bp_diastolic_min, bp_diastolic_max, sleep_monitor, activity_monitor, step_goal, fall_detection, fall_alert_enabled, emergency_alert_enabled, alert_threshold, check_interval, report_frequency, enabled, created_at, updated_at, deleted_at) VALUES
(1, 'PROF001', 'SET001', true, 50, 120, true, 90, 140, 60, 90, true, true, 6000, true, true, true, 3, 60, 'daily', true, NOW(), NOW(), NULL),
(2, 'PROF002', 'SET002', true, 60, 100, false, 0, 0, 0, 0, true, true, 8000, true, true, false, 5, 120, 'weekly', true, NOW(), NOW(), NULL);

-- exercise_goals
INSERT INTO exercise_goals (id, goal_uuid, pet_uuid, goal_type, target_value, unit, start_date, end_date, current_value, progress, status, priority, notes, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'GOAL001', 'PET001', 'steps', 6000.00, 'steps', '2024-03-01', '2024-03-31', 4500.00, 75.00, 'active', 10, 'Daily step goal', NULL, NOW(), NOW(), NULL),
(2, 'GOAL002', 'PET001', 'distance', 5.00, 'km', '2024-03-01', '2024-03-31', 3.50, 70.00, 'active', 8, 'Monthly distance target', NULL, NOW(), NOW(), NULL);

-- exercise_summaries
INSERT INTO exercise_summaries (id, pet_uuid, summary_date, total_duration, total_steps, total_distance, total_calories, avg_heart_rate, exercise_count, walk_count, run_count, swim_count, play_count, training_count, other_count, active_minutes, goal_achieved_count, goal_total_count, goal_achievement_rate, intensity_distribution, tenant_id, created_at, updated_at) VALUES
(1, 'PET001', '2024-03-20', 3600, 5500, 4.50, 380.00, 95.50, 4, 2, 1, 0, 1, 0, 0, 45, 2, 3, 66.67, '{"low": 30, "medium": 50, "high": 20}', NULL, NOW(), NOW()),
(2, 'PET001', '2024-03-19', 4200, 6200, 5.20, 420.00, 98.00, 5, 2, 2, 0, 1, 0, 0, 55, 3, 3, 100.00, '{"low": 20, "medium": 40, "high": 40}', NULL, NOW(), NOW());

-- exercise_trends
INSERT INTO exercise_trends (date, total_duration, total_steps, total_distance, total_calories) VALUES
('2024-03-20 00:00:00+08', 3600, 5500, 4.50, 380.00),
('2024-03-19 00:00:00+08', 4200, 6200, 5.20, 420.00),
('2024-03-18 00:00:00+08', 3000, 4800, 3.80, 320.00);

-- ============================================================================
-- GROUP G: Simulation
-- ============================================================================

-- simulation_environments
INSERT INTO simulation_environments (id, env_id, name, description, scene_type, scene_config, parameters, status, tags, create_user_id, org_id, created_at, updated_at, deleted_at) VALUES
(1, 'ENV001', 'Living Room Simulation', 'Virtual living room environment', 'indoor', '{"room_size": "20x15"}', '{"temperature": 25}', 'active', 'indoor', 1, 1, NOW(), NOW(), NULL),
(2, 'ENV002', 'Garden Exploration', 'Outdoor garden with zones', 'outdoor', '{"area": "50x50"}', '{"temperature": 22}', 'idle', 'outdoor', 1, 1, NOW(), NOW(), NULL);

-- simulation_metrics
INSERT INTO simulation_metrics (id, metric_id, run_id, pet_id, env_id, metric_type, metric_name, metric_value, unit, tags, snapshots, org_id, created_at, updated_at, deleted_at) VALUES
(1, 'MET001', 'RUN001', 'PET001', 'ENV001', 'performance', 'success_rate', 0.95, '%', 'navigation', NULL, 1, NOW(), NOW(), NULL),
(2, 'MET002', 'RUN001', 'PET001', 'ENV001', 'performance', 'avg_time', 12.5, 'seconds', 'navigation', NULL, 1, NOW(), NOW(), NULL);

-- exploration_sessions - skip as it already has data
-- INSERT INTO exploration_sessions VALUES...

-- ============================================================================
-- GROUP H: App Store - Skip for now as schema is complex
-- ============================================================================

-- ============================================================================
-- GROUP I: Analytics
-- ============================================================================

-- analytics_records
INSERT INTO analytics_records (id, tenant_id, analysis_type, period_start, period_end, dimensions, metrics, summary, created_at, updated_at, deleted_at) VALUES
(1, NULL, 'user_activity', '2024-03-01 00:00:00+08', '2024-03-31 23:59:59+08', '{"region": "Shanghai"}', '{"dau": 5000, "mau": 15000}', 'Monthly active users increased', NOW(), NOW(), NULL),
(2, NULL, 'device_usage', '2024-03-01 00:00:00+08', '2024-03-31 23:59:59+08', '{"device_model": "M5Stack_Pet"}', '{"total_devices": 1000, "active_devices": 850}', 'Device engagement stable', NOW(), NOW(), NULL);

-- custom_reports
INSERT INTO custom_reports (id, tenant_id, name, description, report_config, chart_type, is_scheduled, cron_expr, last_run_at, next_run_at, is_public, created_by, updated_by, created_at, updated_at, deleted_at) VALUES
(1, NULL, 'Weekly Sales Report', 'Weekly breakdown of sales', '{"data_source": "orders"}', 'bar', true, '0 2 * * 1', NOW(), '2024-03-25 02:00:00+08', true, 1, 1, NOW(), NOW(), NULL);

-- export_jobs
INSERT INTO export_jobs (id, tenant_id, export_type, data_source, filters, status, file_path, file_size, record_count, error_msg, started_at, completed_at, expires_at, created_by, created_at, updated_at, deleted_at) VALUES
(1, NULL, 'full_export', 'members', '{"created_after": "2024-01-01"}', 'completed', '/exports/members_20240320.csv', 1048576, 5000, NULL, '2024-03-20 10:00:00+08', '2024-03-20 10:15:00+08', '2024-04-19 10:15:00+08', 1, NOW(), NOW(), NULL);

-- ============================================================================
-- GROUP J: Security
-- ============================================================================

-- encryption_keys (corrected)
INSERT INTO encryption_keys (id, key_id, key_version, encrypted_key, is_primary, status, algorithm, rotated_at, expires_at, rotated_by, created_at, updated_at) VALUES
(1, 'KEY001', 1, 'encrypted_key_content_placeholder_1', true, 1, 'AES-256-GCM', NOW(), '2025-03-20 00:00:00+08', 1, NOW(), NOW()),
(2, 'KEY001', 2, 'encrypted_key_content_placeholder_2', false, 1, 'AES-256-GCM', NULL, '2026-03-20 00:00:00+08', NULL, NOW(), NOW());

-- data_anonymization_records
INSERT INTO data_anonymization_records (id, record_id, original_data, anonymized_data, anonymize_type, fields, user_id, username, purpose, export_format, status, created_at, completed_at) VALUES
(1, 'ANON001', '{"phone": "13812345678"}', '{"phone": "138****5678"}', 'partial_mask', 'phone', 1, 'admin', 'GDPR data export', 'json', 1, NOW(), NOW());

-- data_scopes
INSERT INTO data_scopes (id, role_id, scope_type, dept_ids, store_ids, created_at, updated_at) VALUES
(1, 1, 1, '1,2,3', NULL, NOW(), NOW()),
(2, 2, 2, '1,2', '1,2,3', NOW(), NOW());

-- data_permission_rules
INSERT INTO data_permission_rules (id, name, rule_name, rule_type, resource_type, resource_ids, permission_expr, description, priority, is_active, tenant_id, created_by, created_at, updated_at) VALUES
(1, 'Department Data Access', 'dept_data', 'department', 'orders', NULL, '{"dept_ids": [1, 2]}', 'Allow department access', 50, true, NULL, 1, NOW(), NOW()),
(2, 'Own Records Only', 'own_data', 'owner', 'pets', NULL, '{"owner_id": "current_user"}', 'Users access own records', 100, true, NULL, 1, NOW(), NOW());

-- user_data_permissions
INSERT INTO user_data_permissions (id, user_id, role_id, resource_type, rule_type, column_fields, data_scope, filter_expr, priority, is_active, tenant_id, created_by, created_at, updated_at) VALUES
(1, 1, 1, 'orders', 'department', NULL, '{"dept_ids": [1]}', NULL, 50, true, NULL, 1, NOW(), NOW());

-- ============================================================================
-- GROUP K: Other Config
-- ============================================================================

-- translations
INSERT INTO translations (id, locale, key, namespace, value, context, tags, is_active, created_at, updated_at) VALUES
(1, 'en-US', 'common.save', 'common', 'Save', 'Button', 'button', true, NOW(), NOW()),
(2, 'en-US', 'common.cancel', 'common', 'Cancel', 'Button', 'button', true, NOW(), NOW()),
(3, 'zh-CN', 'common.save', 'common', '保存', '按钮', 'button', true, NOW(), NOW());

-- sys_user_exts (corrected - no duplicate)
INSERT INTO sys_user_exts (id, user_id, employee_id, dept_id, company_id, role_ids, data_scope, created_at, updated_at) VALUES
(1, 1, 10001, 1, 1, '1,2', 1, NOW(), NOW());

-- position_templates
INSERT INTO position_templates (id, tenant_id, name, code, description, permissions, status, inherited_from, parent_id, created_at, updated_at, deleted_at) VALUES
(1, NULL, 'Admin Template', 'ADMIN', 'System administrator template', '["user:*,device:*,order:*"]', 1, NULL, NULL, NOW(), NOW(), NULL),
(2, NULL, 'Manager Template', 'MANAGER', 'Department manager template', '["user:read,device:*,order:*"]', 1, NULL, NULL, NOW(), NOW(), NULL);

-- product_categories
INSERT INTO product_categories (id, name, parent_id, icon_url, sort_order, description, is_active, tenant_id, created_at, updated_at) VALUES
(1, 'Pet Food', NULL, 'https://img.example.com/cat/food.png', 1, 'All types of pet food', true, NULL, NOW(), NOW()),
(2, 'Pet Toys', NULL, 'https://img.example.com/cat/toys.png', 2, 'Toys and accessories', true, NULL, NOW(), NOW()),
(3, 'Dry Food', 1, 'https://img.example.com/cat/dry.png', 1, 'Dry pet food', true, NULL, NOW(), NOW());

-- usage_limits
INSERT INTO usage_limits (id, profile_id, limit_id, daily_time_limit, weekly_time_limit, max_single_session, allowed_start_time, allowed_end_time, allowed_days, break_interval, break_duration, eye_protection_enabled, eye_protection_interval, posture_reminder_enabled, enabled, created_at, updated_at, deleted_at) VALUES
(1, 'PROF001', 'LIM001', 120, 480, 30, '08:00', '22:00', '[1,2,3,4,5]', 10, 5, true, 30, true, true, NOW(), NOW(), NULL);

-- subscription_changes
INSERT INTO subscription_changes (id, change_id, user_id, sub_id, change_type, from_plan_id, to_plan_id, amount, change_reason, effective_at, created_at, updated_at, deleted_at) VALUES
(1, 'CHANGE001', 1, 'SUB001', 'upgrade', 'PLAN_BASIC', 'PLAN_PREMIUM', 100.00, 'Want more features', '2024-03-15 00:00:00+08', NOW(), NOW(), NULL);

-- wipe_history
INSERT INTO wipe_history (id, device_id, operator_id, operator_name, wipe_type, status, confirm_token, confirmed_at, executed_at, completed_at, result, reason, tenant_id, created_at, updated_at) VALUES
(1, 'DEV001', 1, 'Admin', 'factory_reset', 'completed', 'token123', '2024-03-10 10:00:00+08', '2024-03-10 10:01:00+08', '2024-03-10 10:05:00+08', 'Device wiped successfully', 'Device reported stolen', NULL, NOW(), NOW());

-- finder_alerts
INSERT INTO finder_alerts (id, alert_uuid, user_id, species, latitude, longitude, radius_km, notify_email, notify_sms, notify_app, is_active, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'ALERT001', 1, 'cat', 31.2304, 121.4740, 10.00, true, false, true, true, NULL, NOW(), NOW(), NULL);

-- sighting_reports
INSERT INTO sighting_reports (id, sighting_uuid, report_uuid, location, sighting_time, description, photo_url, reporter_name, contact_phone, is_credible, reporter_id, tenant_id, created_at) VALUES
(1, 'SIGHT001', 'RPT001', '{"lat": 31.2304, "lng": 121.4740, "address": "Nanjing Road"}', '2024-03-15 16:00:00+08', 'Orange tabby cat resting under bench', 'https://photo.example.com/sight/001.jpg', 'John Doe', '13900001111', true, 1, NULL, NOW());

-- vaccination_reminders
INSERT INTO vaccination_reminders (id, vaccination_id, pet_id, user_id, remind_at, remind_type, is_sent, is_completed, memo, created_at) VALUES
(1, 1, 1, 1, '2025-01-10 10:00:00+08', 'email', false, false, 'Annual rabies booster', NOW());

-- ============================================================================
-- GROUP L: GDPR/Compliance
-- ============================================================================

-- gdpr_requests
INSERT INTO gdpr_requests (id, request_id, request_type, requester_email, requester_name, user_id, status, request_reason, processed_by, processed_at, completed_at, rejected_reason, export_path, response_data, tenant_id, created_at, updated_at) VALUES
(1, 'GDPR001', 'data_export', 'user@example.com', 'Zhang San', 1, 2, 'Want to download my data', 1, NOW(), NOW(), NULL, '/exports/gdpr/GDPR001.zip', '{"profile": {}}', 1, NOW(), NOW());

-- content_filter_rules
INSERT INTO content_filter_rules (id, profile_id, rule_id, rule_name, filter_level, block_adult, block_violence, block_gambling, block_ads, block_games, allowed_categories, blocked_keywords, allowed_apps, blocked_apps, whitelist_mode, enabled, created_at, updated_at, deleted_at) VALUES
(1, 'PROF001', 'RULE_CF001', 'Child Safe Filter', 2, true, true, true, true, false, NULL, NULL, NULL, NULL, false, true, NOW(), NOW(), NULL);

-- compliance_violations
INSERT INTO compliance_violations (id, policy_id, device_id, policy_type, expected_value, actual_value, severity, action_taken, status, resolved_at, resolved_by, created_at) VALUES
(1, 1, 'DEV001', 'firmware_version', 'v2.0.0', 'v1.5.0', 2, 'notified', 1, NULL, NULL, NOW());