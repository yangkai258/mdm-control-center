-- MDM Database Test Data - Batch 4 (Remaining Tables)
-- Generated for tables not covered in batches 1-3

-- ============================================================================
-- GROUP A: Pet Related Tables
-- ============================================================================

-- pet_vaccinations (references pet_id -> pet_profiles.device_id, user_id -> sys_users.id)
INSERT INTO pet_vaccinations (pet_id, user_id, vaccine_name, vaccine_type, lot_number, manufacturer, inoculation_date, inoculation_age, inoculation_site, inoculator, vet_clinic, next_dose_date, next_dose_memo, adverse_reactions, adverse_detail, certificate_url, remark, created_at, updated_at) VALUES
(1, 1, 'Rabies Vaccine', 'rabies', 'RAB2024001', 'Zoetis', '2024-01-15 10:30:00+08', '3 months', 'Left shoulder', 'Dr. Wang', 'Happy Pet Clinic', '2025-01-15 10:30:00+08', 'Annual booster required', 'none', NULL, 'https://cert.example.com/vac/001.pdf', 'First rabies vaccination', NOW(), NOW()),
(1, 1, 'Distemper Vaccine', 'distemper', 'DIS2024002', 'Merck', '2024-02-20 14:00:00+08', '4 months', 'Right thigh', 'Dr. Li', 'Happy Pet Clinic', '2024-08-20 14:00:00+08', 'Booster in 6 months', 'none', NULL, 'https://cert.example.com/vac/002.pdf', 'Distemper shot completed', NOW(), NOW()),
(1, 1, 'Parvovirus Vaccine', 'parvovirus', 'PAR2024003', 'Boehringer', '2024-03-10 09:00:00+08', '5 months', 'Left hind leg', 'Dr. Zhang', 'City Veterinary Hospital', '2025-03-10 09:00:00+08', 'Annual booster', 'mild_swelling', 'Slight swelling at injection site, resolved in 2 days', 'https://cert.example.com/vac/003.pdf', 'Parvo protection started', NOW(), NOW());

-- pet_diet_records
INSERT INTO pet_diet_records (pet_id, user_id, device_id, meal_type, food_name, food_brand, food_type, amount, amount_unit, calories, feeding_method, auto_feeder_id, eat_time, planned_time, duration, status, left_over, appetite_score, health_note, photo_url, created_at, updated_at) VALUES
(1, 1, 'DEV001', 'breakfast', 'Premium Dry Food', 'Royal Canin', 'dry', 80.00, 'g', 280, 'automatic', 'AF001', '2024-03-20 08:00:00+08', '2024-03-20 08:00:00+08', 300, 'completed', 5.00, 9, 'Good appetite today', 'https://photo.example.com/meal/001.jpg', NOW(), NOW()),
(1, 1, 'DEV001', 'lunch', 'Wet Food Pate', 'Hill''s Science', 'wet', 150.00, 'g', 180, 'manual', NULL, '2024-03-20 12:30:00+08', '2024-03-20 12:00:00+08', 600, 'completed', 10.00, 7, 'Ate slowly, left some', 'https://photo.example.com/meal/002.jpg', NOW(), NOW()),
(1, 1, 'DEV001', 'dinner', 'Dental Chews', 'Greenies', 'treat', 30.00, 'g', 80, 'manual', NULL, '2024-03-20 18:00:00+08', '2024-03-20 18:00:00+08', 180, 'completed', 0.00, 10, 'Loved the dental chew', 'https://photo.example.com/meal/003.jpg', NOW(), NOW());

-- pet_lost_reports
INSERT INTO pet_lost_reports (id, pet_id, user_id, report_type, report_date, last_seen_location, last_seen_lat, last_seen_lng, description, photo_urls, contact_phone, contact_email, reward, reward_amount, status, closure_reason, closed_at, created_at, updated_at) VALUES
(1, 1, 1, 'lost', '2024-03-15 14:00:00+08', 'Century Park, Pudong', 31.2204, 121.5440, 'Orange tabby cat, male, 2 years old, wearing blue collar with bell', ARRAY['https://photo.example.com/lost/001.jpg', 'https://photo.example.com/lost/002.jpg'], '13812345678', 'user@example.com', true, 500.00, 'active', NULL, NULL, NOW(), NOW()),
(2, 1, 1, 'found', '2024-03-16 10:00:00+08', 'Near metro station', 31.2304, 121.4740, 'Found an orange cat matching the description', ARRAY['https://photo.example.com/found/001.jpg'], '13987654321', NULL, false, 0.00, 'resolved', 'Cat was found and reunited', '2024-03-17 15:00:00+08', NOW(), NOW()),
(3, 1, 1, 'stolen', '2024-02-20 09:00:00+08', 'Pet store parking lot', 31.2404, 121.4240, 'Small white dog taken during shopping', ARRAY['https://photo.example.com/stolen/001.jpg'], '13711112222', 'user2@example.com', true, 1000.00, 'active', NULL, NULL, NOW(), NOW());

-- pet_finder_alerts
INSERT INTO pet_finder_alerts (id, pet_id, alert_type, severity, title, message, trigger_conditions, is_active, acknowledged_at, acknowledged_by, resolved_at, resolved_by, resolution_notes, created_at, updated_at) VALUES
(1, 1, 'sighting', 'high', 'Lost Pet Alert - Orange Tabby', 'An orange tabby cat was spotted in your area', '{"location_radius": 500, "time_window": 3600}', true, '2024-03-16 10:30:00+08', 1, NULL, NULL, 'Alert sent to nearby users', NOW(), NOW()),
(2, 1, 'found', 'medium', 'Potential Match Found', 'A found pet matches your lost report description', '{"similarity_score": 85}', true, NULL, NULL, NULL, NULL, 'Waiting for owner confirmation', NOW(), NOW()),
(3, 1, 'nearby', 'low', 'Lost Pet in Your Area', 'Another user reported a lost pet nearby', '{"distance_meters": 300}', true, NULL, NULL, NULL, NULL, 'Informational alert only', NOW(), NOW());

-- pet_finder_reports
INSERT INTO pet_finder_reports (id, pet_id, reporter_user_id, report_type, sighting_time, sighting_location, sighting_lat, sighting_lng, description, photo_urls, confidence_level, verified, verifier_id, verified_at, notes, created_at, updated_at) VALUES
(1, 1, 1, 'sighting', '2024-03-15 16:00:00+08', 'Jing An Park', 31.2254, 121.4540, 'Orange cat resting under bench', ARRAY['https://photo.example.com/sight/001.jpg'], 'medium', true, 1, '2024-03-15 18:00:00+08', 'Verified by park security footage', NOW(), NOW()),
(2, 1, 1, 'sighting', '2024-03-15 18:30:00+08', 'Nanjing Road pedestrian mall', 31.2304, 121.4740, 'Orange cat chasing pigeons', ARRAY['https://photo.example.com/sight/002.jpg'], 'high', false, NULL, NULL, 'Waiting for verification', NOW(), NOW()),
(3, 1, 1, 'found', '2024-03-16 09:00:00+08', 'Metro Station Exit 3', 31.2354, 121.4840, 'Friendly orange cat, appears well-fed', ARRAY['https://photo.example.com/found/001.jpg'], 'high', true, 1, '2024-03-16 11:00:00+08', 'Reporter is fostering the cat temporarily', NOW(), NOW());

-- pet_finder_sightings
INSERT INTO pet_finder_sightings (id, pet_id, sighting_time, sighting_location, sighting_lat, sighting_lng, description, photo_urls, behavior, is_confirmed, reported_by, created_at, updated_at) VALUES
(1, 1, '2024-03-15 16:00:00+08', 'Jing An Park', 31.2254, 121.4540, 'Orange tabby sleeping under tree', ARRAY['https://photo.example.com/sight/001.jpg'], 'sleeping', true, 1, NOW(), NOW()),
(2, 1, '2024-03-15 17:30:00+08', 'West Nanjing Road', 31.2304, 121.4740, 'Orange cat walking with limp', ARRAY['https://photo.example.com/sight/002.jpg'], 'walking', false, 1, NOW(), NOW()),
(3, 1, '2024-03-16 08:00:00+08', 'Xujiahui Shopping Center', 31.1954, 121.4340, 'Orange cat near food court', ARRAY['https://photo.example.com/sight/003.jpg'], 'eating', true, 1, NOW(), NOW());

-- pet_products
INSERT INTO pet_products (id, product_code, product_name, product_type, brand, species, breed_size, age_range, description, ingredients, nutritional_info, specifications, price, cost, stock_quantity, safety_warnings, storage_method, shelf_life, image_urls, is_active, created_at, updated_at) VALUES
(1, 'FOOD001', 'Premium Adult Cat Food', 'food', 'Royal Canin', 'cat', 'all', 'adult', 'Complete nutrition for adult cats', 'Chicken, rice, beet pulp, fish oil', '{"protein": 32, "fat": 15, "fiber": 5}', '400g bag', 128.00, 65.00, 500, 'Store in cool dry place', 'Room temperature', '12 months', ARRAY['https://img.example.com/food/001.jpg'], true, NOW(), NOW()),
(2, 'FOOD002', 'Kitten Growth Formula', 'food', 'Hill''s Science', 'cat', 'small', 'kitten', 'Specially formulated for growing kittens', 'Chicken, ocean fish, rice flour', '{"protein": 35, "fat": 20, "calcium": 1.2}', '500g bag', 158.00, 80.00, 300, 'Keep sealed, avoid humidity', 'Cool dry place', '18 months', ARRAY['https://img.example.com/food/002.jpg'], true, NOW(), NOW()),
(3, 'TOY001', 'Interactive Laser Toy', 'toy', 'Catit', 'cat', 'all', 'all', 'Laser toy for indoor cats', 'Plastic, metal, LED', '{}', 'USB rechargeable', 89.00, 35.00, 150, 'Supervise during play', 'N/A', '2 years', ARRAY['https://img.example.com/toy/001.jpg'], true, NOW(), NOW());

-- pet_shop_orders
INSERT INTO pet_shop_orders (id, order_no, user_id, pet_id, product_id, quantity, unit_price, total_amount, order_status, shipping_address, shipping_phone, shipping_name, payment_method, payment_status, payment_time, shipped_at, delivered_at, created_at, updated_at) VALUES
(1, 'ORD20240320001', 1, 1, 1, 2, 128.00, 256.00, 'delivered', '123 Main St, Shanghai', '13812345678', 'Zhang San', 'wechat_pay', 'paid', '2024-03-20 10:00:00+08', '2024-03-21 09:00:00+08', '2024-03-22 14:00:00+08', NOW(), NOW()),
(2, 'ORD20240321001', 1, 1, 2, 1, 158.00, 158.00, 'shipped', '123 Main St, Shanghai', '13812345678', 'Zhang San', 'alipay', 'paid', '2024-03-21 15:30:00+08', '2024-03-22 10:00:00+08', NULL, NOW(), NOW()),
(3, 'ORD20240322001', 1, 1, 3, 1, 89.00, 89.00, 'paid', '123 Main St, Shanghai', '13812345678', 'Zhang San', 'wechat_pay', 'paid', '2024-03-22 20:00:00+08', NULL, NULL, NOW(), NOW());

-- ============================================================================
-- GROUP B: Member Related Tables
-- ============================================================================

-- member_card_groups
INSERT INTO member_card_groups (id, group_name, parent_id, sort, created_at, updated_at) VALUES
(1, 'Gold Members', NULL, 1, NOW(), NOW()),
(2, 'Silver Members', NULL, 2, NOW(), NOW()),
(3, 'Bronze Members', NULL, 3, NOW(), NOW()),
(4, 'VIP Gold', 1, 1, NOW(), NOW()),
(5, 'Regular Gold', 1, 2, NOW(), NOW());

-- member_tags
INSERT INTO member_tags (id, tag_code, tag_name, tag_type, category, color, icon, sort, status, created_at, updated_at) VALUES
(1, 'VIP', 'VIP Member', 1, 'membership', 'gold', 'crown', 1, 1, NOW(), NOW()),
(2, 'NEW', 'New Member', 1, 'membership', 'green', 'star', 2, 1, NOW(), NOW()),
(3, 'ACTIVE', 'Active User', 1, 'behavior', 'blue', 'lightning', 3, 1, NOW(), NOW()),
(4, 'PET_LOVER', 'Pet Enthusiast', 2, 'interest', 'purple', 'heart', 4, 1, NOW(), NOW()),
(5, 'PREMIUM', 'Premium Customer', 1, 'membership', 'red', 'diamond', 5, 1, NOW(), NOW());

-- member_tag_records
INSERT INTO member_tag_records (id, member_id, tag_id, tagged_by, tagged_at, source, notes, created_at) VALUES
(1, 1, 1, 1, NOW(), 'manual', 'Added by admin', NOW()),
(2, 1, 3, 1, NOW(), 'auto', 'Auto-tagged due to high activity', NOW()),
(3, 1, 4, 1, NOW(), 'manual', 'Pet owner confirmed', NOW());

-- member_operation_records
INSERT INTO member_operation_records (id, member_id, operation_type, operation_desc, operator_id, operator_type, ip_address, user_agent, related_order_id, created_at) VALUES
(1, 1, 'login', 'Member logged in', 1, 'member', '192.168.1.100', 'Mozilla/5.0', NULL, NOW()),
(2, 1, 'update_profile', 'Updated phone number', 1, 'member', '192.168.1.100', 'Mozilla/5.0', NULL, NOW()),
(3, 1, 'place_order', 'Placed new order ORD20240320001', 1, 'member', '192.168.1.100', 'Mozilla/5.0', 1, NOW());

-- member_orders
INSERT INTO member_orders (id, order_no, member_id, order_type, total_amount, discount_amount, actual_amount, points_earned, points_deducted, coupon_id, coupon_discount, shipping_fee, payment_method, payment_status, payment_no, paid_at, status, shipping_address, shipping_phone, shipping_name, invoice_status, invoice_no, remark, created_at, updated_at) VALUES
(1, 'MEM_ORD_001', 1, 'purchase', 256.00, 0.00, 256.00, 256, 0, NULL, 0.00, 0.00, 'wechat_pay', 'paid', 'WXPAY001', '2024-03-20 10:05:00+08', 'completed', '123 Main St, Shanghai', '13812345678', 'Zhang San', 'uninvoiced', NULL, 'First order bonus applied', NOW(), NOW()),
(2, 'MEM_ORD_002', 1, 'purchase', 158.00, 10.00, 148.00, 148, 0, 1, 10.00, 0.00, 'alipay', 'paid', 'ALIPAY001', '2024-03-21 15:35:00+08', 'shipped', '123 Main St, Shanghai', '13812345678', 'Zhang San', 'uninvoiced', NULL, NULL, NOW(), NOW()),
(3, 'MEM_ORD_003', 1, 'recharge', 500.00, 0.00, 500.00, 500, 0, NULL, 0.00, 0.00, 'wechat_pay', 'paid', 'WXPAY002', '2024-03-22 09:00:00+08', 'completed', NULL, NULL, NULL, 'invoiced', 'INV20240322001', 'Account recharge', NOW(), NOW());

-- order_items
INSERT INTO order_items (id, order_id, product_id, product_name, product_type, quantity, unit_price, total_price, discount_amount, final_price, sku_code, specification, created_at) VALUES
(1, 1, 1, 'Premium Adult Cat Food', 'food', 2, 128.00, 256.00, 0.00, 256.00, 'FOOD001_400G', '400g/bag', NOW()),
(2, 2, 2, 'Kitten Growth Formula', 'food', 1, 158.00, 158.00, 10.00, 148.00, 'FOOD002_500G', '500g/bag', NOW()),
(3, 3, NULL, 'Account Recharge', 'recharge', 1, 500.00, 500.00, 0.00, 500.00, 'RECHARGE_500', '500 points', NOW());

-- member_upgrade_rules
INSERT INTO member_upgrade_rules (id, rule_name, from_level, to_level, condition_type, condition_value, points_threshold, spend_threshold, days_required, is_active, priority, created_at, updated_at) VALUES
(1, 'Bronze to Silver', 1, 2, 'points', 5000, 5000, 0, 0, true, 1, NOW(), NOW()),
(2, 'Silver to Gold', 2, 3, 'spend', 10000, 0, 10000, 90, true, 2, NOW(), NOW()),
(3, 'Gold to Platinum', 3, 4, 'combined', 20000, 10000, 20000, 180, true, 3, NOW(), NOW());

-- member_upgrade_records
INSERT INTO member_upgrade_records (id, member_id, from_level, to_level, upgrade_type, trigger_type, points_balance, spend_amount, verified_by, verified_at, status, reject_reason, created_at) VALUES
(1, 1, 1, 2, 'auto', 'points', 5500, 0, NULL, NULL, 'approved', NULL, NOW()),
(2, 1, 2, 3, 'manual', 'spend', 5500, 15000, 1, NOW(), 'approved', NULL, NOW());

-- ============================================================================
-- GROUP C: Insurance/Medical
-- ============================================================================

-- insurance_products
INSERT INTO insurance_products (id, product_uuid, name, code, coverage_type, provider, coverage_amount, premium, premium_period, deductible, wait_period_days, cover_age_min, cover_age_max, breed_codes, species_allowed, description, terms, exclusions, coverage_items, max_claim_amount, annual_max_claim, is_active, sort_order, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'INS_PROD_001', 'Pet Basic Health Insurance', 'BASIC_HEALTH', 'basic', 'PingAn Insurance', 50000.00, 199.00, 'monthly', 500.00, 15, 30, 120, ARRAY['EXOTIC', 'PERSIAN', 'MAINE_COON'], ARRAY['cat', 'dog'], 'Basic health coverage for pets including accidents and common illnesses', 'Standard terms and conditions apply', 'Pre-existing conditions, cosmetic procedures', ARRAY['accident', 'illness', 'surgery'], 50000.00, 100000.00, true, 1, NULL, NOW(), NOW(), NULL),
(2, 'INS_PROD_002', 'Pet Premium Insurance', 'PREMIUM_HEALTH', 'premium', 'China Life Insurance', 150000.00, 399.00, 'monthly', 200.00, 7, 30, 144, ARRAY['ALL'], ARRAY['cat', 'dog', 'rabbit'], 'Comprehensive coverage including dental, preventive care', 'Full terms available on request', 'Breed-specific hereditary conditions', ARRAY['accident', 'illness', 'surgery', 'dental', 'preventive'], 150000.00, 300000.00, true, 2, NULL, NOW(), NOW(), NULL),
(3, 'INS_PROD_003', 'Pet Accident Only', 'ACCIDENT_ONLY', 'accident', '平安保险', 30000.00, 99.00, 'monthly', 300.00, 0, 30, 180, ARRAY['ALL'], ARRAY['cat', 'dog'], 'Accident coverage only, lower premium', 'Accident-only terms', 'Illness, preventive care', ARRAY['accident'], 30000.00, 50000.00, true, 3, NULL, NOW(), NOW(), NULL);

-- insurance_claims
INSERT INTO insurance_claims (id, claim_no, policy_id, member_id, product_id, claim_type, claim_amount, approved_amount, reimbursement_ratio, reimbursement_amount, diagnosis, diagnosis_date, treatment_details, hospital_name, veterinarian, vet_license_no, invoice_no, invoice_amount, invoice_date, status, review_comments, reviewed_by, reviewed_at, paid_at, bank_name, bank_account, account_holder, created_at, updated_at) VALUES
(1, 'CLM202403001', 1, 1, 1, 'illness', 5000.00, 4500.00, 0.90, 4050.00, 'Respiratory infection', '2024-03-10', 'Antibiotics treatment, 5 days', 'Happy Pet Hospital', 'Dr. Wang Wei', 'VET_LIC_001', 'INV001', 5000.00, '2024-03-10', 'approved', 'Claim approved, reimbursement processed', 1, '2024-03-15', '2024-03-18', 'ICBC', '6222021234567890', 'Zhang San', NOW(), NOW()),
(2, 'CLM202403002', 1, 1, 1, 'accident', 8000.00, 7200.00, 0.90, 6480.00, 'Leg fracture from fall', '2024-03-05', 'Surgery and cast', 'City Veterinary Hospital', 'Dr. Li Ming', 'VET_LIC_002', 'INV002', 8000.00, '2024-03-06', 'approved', 'Surgery claim approved', 1, '2024-03-12', '2024-03-15', 'CCB', '6222021234567891', 'Zhang San', NOW(), NOW()),
(3, 'CLM202403003', 2, 1, 2, 'dental', 3000.00, 2700.00, 0.90, 2430.00, 'Dental cleaning', '2024-03-20', 'Professional dental cleaning under anesthesia', 'Happy Pet Hospital', 'Dr. Wang Wei', 'VET_LIC_001', 'INV003', 3000.00, '2024-03-20', 'pending', 'Under review', NULL, NULL, NULL, NULL, NULL, NULL, NOW(), NOW());

-- insurance_claim_documents
INSERT INTO insurance_claim_documents (id, claim_id, document_type, file_name, file_path, file_size, mime_type, uploaded_by, verified, verified_by, verified_at, verify_notes, created_at) VALUES
(1, 1, 'invoice', 'invoice_001.pdf', '/documents/claims/CLM202403001/invoice.pdf', 1024000, 'application/pdf', 1, true, 1, NOW(), 'Invoice verified', NOW()),
(2, 1, 'diagnosis', 'diagnosis_001.pdf', '/documents/claims/CLM202403001/diagnosis.pdf', 512000, 'application/pdf', 1, true, 1, NOW(), 'Medical records confirmed', NOW()),
(3, 2, 'invoice', 'invoice_002.pdf', '/documents/claims/CLM202403002/invoice.pdf', 1024000, 'application/pdf', 1, true, 1, NOW(), 'Surgery invoice verified', NOW());

-- ============================================================================
-- GROUP D: OTA Related
-- ============================================================================

-- ota_progress
INSERT INTO ota_progress (id, deployment_id, device_id, package_id, from_version, to_version, ota_status, ota_message, progress, retry_count, started_at, completed_at, created_at, updated_at, deleted_at) VALUES
(1, 1, 'DEV001', 1, 'v1.0.0', 'v1.1.0', 'completed', 'OTA completed successfully', 100, 0, '2024-03-15 10:00:00+08', '2024-03-15 10:15:00+08', NOW(), NOW(), NULL),
(2, 2, 'DEV002', 2, 'v1.0.0', 'v1.2.0', 'in_progress', 'Downloading firmware...', 45, 1, '2024-03-20 14:00:00+08', NULL, NOW(), NOW(), NULL),
(3, 1, 'DEV003', 1, 'v1.0.0', 'v1.1.0', 'failed', 'Download timeout', 30, 3, '2024-03-18 09:00:00+08', '2024-03-18 09:30:00+08', NOW(), NOW(), NULL);

-- firmware_optimization_configs
INSERT INTO firmware_optimization_configs (id, config_name, config_key, config_value, config_type, description, min_firmware_version, max_firmware_version, device_model, priority, is_active, created_at, updated_at) VALUES
(1, 'Battery Optimization', 'battery_opt', '{"level": "aggressive", "sleep_interval": 300}', 'json', 'Optimize power consumption', 'v1.0.0', 'v1.5.0', 'M5Stack_Pet', 10, true, NOW(), NOW()),
(2, 'Network Retry', 'network_retry', '{"max_retries": 5, "timeout_ms": 30000}', 'json', 'Network retry configuration', 'v1.0.0', NULL, 'M5Stack_Pet', 5, true, NOW(), NOW()),
(3, 'Storage Compression', 'storage_comp', '{"enabled": true, "algorithm": "lz4"}', 'json', 'Enable storage compression', 'v1.1.0', NULL, 'M5Stack_Pet', 3, true, NOW(), NOW());

-- ============================================================================
-- GROUP E: AI Related
-- ============================================================================

-- ai_training
INSERT INTO ai_training (id, task_key, name, description, model_id, base_model_key, training_type, dataset_path, dataset_size, validation_path, hyper_params, resource_config, output_path, status, priority, progress, epoch, total_epochs, current_step, total_steps, loss, metrics, logs_path, error_message, started_at, completed_at, estimated_time, queued_at, org_id, create_user_id, created_at, updated_at, deleted_at) VALUES
(1, 'train_pet_emotion_v1', 'Pet Emotion Recognition v1', 'Train model to recognize pet emotions', 1, 'base_emotion_v3', 'transfer_learning', '/data/datasets/pet_emotion', 50000, '/data/val/pet_emotion', '{"lr": 0.001, "batch_size": 32}', '{"gpu": 2, "memory_gb": 32}', '/models/output/pet_emotion_v1', 'completed', 10, 100, 50, 50, 5000, 5000, 0.023, '{"accuracy": 0.95, "f1": 0.94}', '/logs/train_pet_emotion_v1', NULL, '2024-03-10 08:00:00+08', '2024-03-12 16:00:00+08', 180000, '2024-03-10 07:00:00+08', 1, 1, NOW(), NOW(), NULL),
(2, 'train_health_detection', 'Pet Health Anomaly Detection', 'Detect health anomalies from vital signs', 2, 'base_health_v2', 'fine_tuning', '/data/datasets/health_anomaly', 30000, '/data/val/health_anomaly', '{"lr": 0.0005, "batch_size": 16}', '{"gpu": 4, "memory_gb": 64}', '/models/output/health_detection', 'training', 8, 65, 30, 100, 3000, 10000, 0.045, '{"precision": 0.92, "recall": 0.89}', '/logs/train_health_detection', NULL, '2024-03-18 10:00:00+08', NULL, 360000, '2024-03-18 09:00:00+08', 1, 1, NOW(), NOW(), NULL),
(3, 'train_voice_command', 'Voice Command Recognition', 'Train pet voice command recognition', 3, 'base_asr_v1', 'transfer_learning', '/data/datasets/voice_commands', 100000, '/data/val/voice_commands', '{"lr": 0.002, "batch_size": 64}', '{"gpu": 2, "memory_gb": 32}', '/models/output/voice_command', 'queued', 5, 0, 0, 50, 0, 10000, NULL, '{}', '/logs/train_voice_command', NULL, NULL, NULL, NULL, 720000, '2024-03-22 08:00:00+08', 1, 1, NOW(), NOW(), NULL);

-- ai_inference
INSERT INTO ai_inference (id, model_id, model_version, inference_type, input_data, output_data, confidence, latency_ms, device_id, pet_id, user_id, error_message, created_at) VALUES
(1, 1, 'v1.0.5', 'emotion_recognition', '{"image": "/data/input/img_001.jpg"}', '{"emotion": "happy", "confidence": 0.95}', 0.95, 120, 'DEV001', 1, 1, NULL, NOW()),
(2, 2, 'v1.2.0', 'health_anomaly', '{"vitals": {"heart_rate": 120, "temperature": 39.5}}', '{"anomaly": false, "score": 0.12}', 0.88, 85, 'DEV001', 1, 1, NULL, NOW()),
(3, 3, 'v2.0.0', 'voice_command', '{"audio": "/data/input/audio_001.wav"}', '{"command": "sit", "confidence": 0.92}', 0.92, 200, 'DEV001', 1, 1, NULL, NOW());

-- ai_audit_logs
INSERT INTO ai_audit_logs (id, audit_type, model_id, model_version, action, operator_id, operator_type, ip_address, input_summary, output_summary, risk_level, risk_score, flagged, flag_reason, review_status, reviewed_by, reviewed_at, created_at) VALUES
(1, 'bias_check', 1, 'v1.0.5', 'inference', 1, 'system', '127.0.0.1', 'Image of cat', 'Emotion: happy', 'low', 0.1, false, NULL, 'approved', NULL, NULL, NOW()),
(2, 'fairness', 2, 'v1.2.0', 'training', 1, 'user', '192.168.1.100', 'Dataset: 50k samples', 'Fairness metrics within threshold', 'low', 0.15, false, NULL, 'approved', 1, NOW(), NOW()),
(3, 'output_review', 3, 'v2.0.0', 'inference', 1, 'system', '127.0.0.1', 'Voice command audio', 'Command: sit', 'medium', 0.35, true, 'Low confidence on ambiguous audio', 'pending', NULL, NULL, NOW());

-- ai_audit_reports
INSERT INTO ai_audit_reports (id, report_key, report_type, model_id, model_version, period_start, period_end, total_inferences, flagged_inferences, risk_distribution, bias_metrics, fairness_metrics, recommendations, created_by, status, approved_by, approved_at, created_at) VALUES
(1, 'AUDIT_2024_W11', 'weekly', 1, 'v1.0.5', '2024-03-11', '2024-03-17', 15000, 45, '{"low": 14000, "medium": 800, "high": 200}', '{"gender_bias": 0.02, "breed_bias": 0.05}', '{"fairness_delta": 0.03}', 'Consider collecting more diverse training data for Persian cats', 1, 'approved', 1, NOW(), NOW()),
(2, 'AUDIT_2024_W12', 'weekly', 2, 'v1.2.0', '2024-03-18', '2024-03-24', 8000, 12, '{"low": 7500, "medium": 400, "high": 100}', '{"age_bias": 0.03, "size_bias": 0.04}', '{"fairness_delta": 0.02}', 'Model performs slightly worse on senior pets, recommend age-specific tuning', 1, 'pending', NULL, NULL, NOW()),
(3, 'AUDIT_HEALTH_001', 'monthly', 2, 'v1.2.0', '2024-03-01', '2024-03-31', 32000, 89, '{"low": 29000, "medium": 2200, "high": 800}', '{"gender_bias": 0.01, "breed_bias": 0.06}', '{"fairness_delta": 0.04}', 'Health detection accuracy improved by 5% this month', 1, 'approved', 1, NOW(), NOW());

-- ai_fairness_tests
INSERT INTO ai_fairness_tests (id, test_key, model_id, model_version, test_type, test_groups, protected_attributes, fairness_metrics, threshold, sample_size, pass_count, fail_count, status, test_results, error_message, executed_at, created_at) VALUES
(1, 'FAIR_TEST_001', 1, 'v1.0.5', 'demographic_parity', '["cat", "dog"]', '["species", "breed"]', '{"demographic_parity_diff": 0.02}', 0.05, 1000, 980, 20, 'passed', '{"species_parity": 0.98, "breed_parity": 0.95}', NULL, NOW(), NOW()),
(2, 'FAIR_TEST_002', 2, 'v1.2.0', 'equalized_odds', '["young", "adult", "senior"]', '["age_group"]', '{"equalized_odds_diff": 0.03}', 0.05, 2000, 1950, 50, 'passed', '{"young_tpr": 0.97, "adult_tpr": 0.95, "senior_tpr": 0.94}', NULL, NOW(), NOW()),
(3, 'FAIR_TEST_003', 3, 'v2.0.0', 'individual_fairness', '["indoor", "outdoor"]', '["lifestyle"]', '{"consistency_score": 0.91}', 0.10, 500, 450, 50, 'failed', '{"individual_fairness_violations": 50}', 'Sample size too small for outdoor cats', NOW(), NOW());

-- ai_fairness_metrics
INSERT INTO ai_fairness_metrics (id, test_id, metric_name, metric_value, threshold, is_within_threshold, group_name, sample_count, created_at) VALUES
(1, 1, 'demographic_parity', 0.02, 0.05, true, 'cat', 500, NOW()),
(2, 1, 'demographic_parity', 0.03, 0.05, true, 'dog', 500, NOW()),
(3, 2, 'equalized_odds_tpr', 0.03, 0.05, true, 'young', 800, NOW());

-- ai_deploy_sharded
INSERT INTO ai_deploy_sharded (id, deploy_id, shard_id, model_id, model_version, shard_index, total_shards, shard_path, shard_hash, shard_size, device_id, device_model, deployed_at, status, error_message, created_at, updated_at) VALUES
(1, 1, 'S001', 1, 'v1.0.5', 0, 4, '/models/shards/emotion_v1/shard_0.bin', 'sha256:abc123', 52428800, 'DEV001', 'M5Stack_Pet', NOW(), 'active', NULL, NOW(), NOW()),
(2, 1, 'S002', 1, 'v1.0.5', 1, 4, '/models/shards/emotion_v1/shard_1.bin', 'sha256:def456', 52428800, 'DEV002', 'M5Stack_Pet', NOW(), 'active', NULL, NOW(), NOW()),
(3, 2, 'S003', 2, 'v1.2.0', 0, 8, '/models/shards/health_v2/shard_0.bin', 'sha256:ghi789', 67108864, 'DEV001', 'M5Stack_Pet', NOW(), 'deploying', NULL, NOW(), NOW());

-- ai_model_deploy_history
INSERT INTO ai_model_deploy_history (id, deploy_key, model_id, model_version, deploy_type, target_devices, success_count, fail_count, deploy_status, started_at, completed_at, rollback_from, created_at, updated_at) VALUES
(1, 'DEPLOY_001', 1, 'v1.0.5', 'rolling', 100, 98, 2, 'completed', '2024-03-15 10:00:00+08', '2024-03-15 10:30:00+08', NULL, NOW(), NOW()),
(2, 'DEPLOY_002', 2, 'v1.2.0', 'canary', 50, 48, 0, 'in_progress', '2024-03-20 14:00:00+08', NULL, NULL, NOW(), NOW()),
(3, 'DEPLOY_003', 1, 'v1.0.4', 'rolling', 100, 100, 0, 'rolled_back', '2024-03-10 09:00:00+08', '2024-03-10 09:20:00+08', 'v1.0.5', NOW(), NOW());

-- ai_bias_detections
INSERT INTO ai_bias_detections (id, detection_key, model_id, model_version, bias_type, protected_attribute, group_a, group_b, metric_name, metric_value_a, metric_value_b, bias_magnitude, is_significant, p_value, sample_size, detected_at, status, reviewed_by, reviewed_at, notes, created_at) VALUES
(1, 'BIAS_DET_001', 1, 'v1.0.5', 'species', 'species', 'cat', 'dog', 'accuracy', 0.95, 0.92, 0.03, false, 0.12, 1000, NOW(), 'confirmed', NULL, NULL, 'Minor difference, within acceptable range', NOW()),
(2, 'BIAS_DET_002', 2, 'v1.2.0', 'age', 'age_group', 'young', 'senior', 'recall', 0.94, 0.87, 0.07, true, 0.03, 800, NOW(), 'under_review', NULL, NULL, 'Significant recall difference for senior pets', NOW()),
(3, 'BIAS_DET_003', 3, 'v2.0.0', 'lifestyle', 'indoor_outdoor', 'indoor', 'outdoor', 'precision', 0.91, 0.78, 0.13, true, 0.01, 500, NOW(), 'flagged', 1, NOW(), 'High precision difference, needs attention', NOW());

-- model_shards
INSERT INTO model_shards (id, model_id, model_version, shard_index, total_shards, shard_file_path, shard_hash, shard_size_bytes, checksum_algorithm, created_at) VALUES
(1, 1, 'v1.0.5', 0, 4, '/models/emotion/shard_0_v105.bin', 'sha256:a1b2c3d4', 52428800, 'SHA256', NOW()),
(2, 1, 'v1.0.5', 1, 4, '/models/emotion/shard_1_v105.bin', 'sha256:e5f6g7h8', 52428800, 'SHA256', NOW()),
(3, 2, 'v1.2.0', 0, 8, '/models/health/shard_0_v120.bin', 'sha256:i9j0k1l2', 67108864, 'SHA256', NOW());

-- ============================================================================
-- GROUP F: Digital Twin (Vital Signs & Health)
-- ============================================================================

-- vital_trends
INSERT INTO vital_trends (pet_uuid, vital_type, current_value, avg_value, min_value, max_value, trend, trend_rate, is_abnormal, abnormal_level, last_updated) VALUES
('PET001', 'heart_rate', 85.5, 82.3, 65.0, 120.0, 'stable', 0.02, false, NULL, NOW()),
('PET001', 'temperature', 38.8, 38.5, 37.5, 39.5, 'rising', 0.05, false, NULL, NOW()),
('PET001', 'activity', 4500.0, 4200.0, 1000.0, 8000.0, 'increasing', 0.08, false, NULL, NOW());

-- health_alert_rules
INSERT INTO health_alert_rules (id, rule_uuid, pet_uuid, rule_name, alert_type, condition, alert_level, title_template, suggestion, cooldown_period, is_enabled, priority, notify_channels, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'RULE001', 'PET001', 'High Heart Rate Alert', 'heart_rate', '{"operator": ">", "value": 100, "duration": 300}', 'warning', 'Heart Rate Alert', 'Please check your pet immediately', 3600, true, 10, ARRAY['app', 'sms'], NULL, NOW(), NOW(), NULL),
(2, 'RULE002', 'PET001', 'Fever Alert', 'temperature', '{"operator": ">", "value": 39.5, "duration": 600}', 'critical', 'Fever Detected', 'Seek veterinary care', 1800, true, 5, ARRAY['app', 'sms', 'email'], NULL, NOW(), NOW(), NULL),
(3, 'RULE003', 'PET001', 'Low Activity Alert', 'activity', '{"operator": "<", "value": 1000, "duration": 7200}', 'info', 'Low Activity Notice', 'Monitor your pet closely', 7200, true, 15, ARRAY['app'], NULL, NOW(), NOW(), NULL);

-- health_monitor_settings
INSERT INTO health_monitor_settings (id, profile_id, setting_id, heart_rate_monitor, heart_rate_min, heart_rate_max, bp_monitor, bp_systolic_min, bp_systolic_max, bp_diastolic_min, bp_diastolic_max, sleep_monitor, activity_monitor, step_goal, fall_detection, fall_alert_enabled, emergency_alert_enabled, alert_threshold, check_interval, report_frequency, enabled, created_at, updated_at, deleted_at) VALUES
(1, 'PROF001', 'SET001', true, 50, 120, true, 90, 140, 60, 90, true, true, 6000, true, true, true, 3, 60, 'daily', true, NOW(), NOW(), NULL),
(2, 'PROF002', 'SET002', true, 60, 100, false, 0, 0, 0, 0, true, true, 8000, true, true, false, 5, 120, 'weekly', true, NOW(), NOW(), NULL);

-- exercise_goals
INSERT INTO exercise_goals (id, goal_uuid, pet_uuid, goal_type, target_value, unit, start_date, end_date, current_value, progress, status, priority, notes, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'GOAL001', 'PET001', 'steps', 6000.00, 'steps', '2024-03-01', '2024-03-31', 4500.00, 75.00, 'active', 10, 'Daily step goal', NULL, NOW(), NOW(), NULL),
(2, 'GOAL002', 'PET001', 'distance', 5.00, 'km', '2024-03-01', '2024-03-31', 3.50, 70.00, 'active', 8, 'Monthly distance target', NULL, NOW(), NOW(), NULL),
(3, 'GOAL003', 'PET001', 'calories', 500.00, 'kcal', '2024-03-01', '2024-03-31', 380.00, 76.00, 'active', 6, 'Calorie burn goal', NULL, NOW(), NOW(), NULL);

-- exercise_summaries
INSERT INTO exercise_summaries (id, pet_uuid, summary_date, total_duration, total_steps, total_distance, total_calories, avg_heart_rate, exercise_count, walk_count, run_count, swim_count, play_count, training_count, other_count, active_minutes, goal_achieved_count, goal_total_count, goal_achievement_rate, intensity_distribution, tenant_id, created_at, updated_at) VALUES
(1, 'PET001', '2024-03-20', 3600, 5500, 4.50, 380.00, 95.50, 4, 2, 1, 0, 1, 0, 0, 45, 2, 3, 66.67, '{"low": 30, "medium": 50, "high": 20}', NULL, NOW(), NOW()),
(2, 'PET001', '2024-03-19', 4200, 6200, 5.20, 420.00, 98.00, 5, 2, 2, 0, 1, 0, 0, 55, 3, 3, 100.00, '{"low": 20, "medium": 40, "high": 40}', NULL, NOW(), NOW()),
(3, 'PET001', '2024-03-18', 3000, 4800, 3.80, 320.00, 92.00, 3, 1, 1, 0, 1, 0, 0, 40, 1, 3, 33.33, '{"low": 40, "medium": 40, "high": 20}', NULL, NOW(), NOW());

-- exercise_trends
INSERT INTO exercise_trends (date, total_duration, total_steps, total_distance, total_calories) VALUES
('2024-03-20 00:00:00+08', 3600, 5500, 4.50, 380.00),
('2024-03-19 00:00:00+08', 4200, 6200, 5.20, 420.00),
('2024-03-18 00:00:00+08', 3000, 4800, 3.80, 320.00);

-- ============================================================================
-- GROUP G: Embodied Intelligence/Simulation
-- ============================================================================

-- simulation_environments
INSERT INTO simulation_environments (id, env_id, name, description, scene_type, scene_config, parameters, status, tags, create_user_id, org_id, created_at, updated_at, deleted_at) VALUES
(1, 'ENV001', 'Living Room Simulation', 'Virtual living room environment for pet training', 'indoor', '{"room_size": "20x15", "furniture": ["sofa", "table", "rug"]}', '{"temperature": 25, "humidity": 60}', 'active', 'indoor,training', 1, 1, NOW(), NOW(), NULL),
(2, 'ENV002', 'Garden Exploration', 'Outdoor garden with various zones', 'outdoor', '{"area": "50x50", "zones": ["grass", "path", "flowers"]}', '{"temperature": 22, "humidity": 65}', 'idle', 'outdoor,exploration', 1, 1, NOW(), NOW(), NULL),
(3, 'ENV003', 'Obstacle Course', 'Training obstacle course', 'training', '{"obstacles": ["tunnel", "jump", "weave"]}', '{"difficulty": "medium"}', 'active', 'training,obstacle', 1, 1, NOW(), NOW(), NULL);

-- simulation_metrics
INSERT INTO simulation_metrics (id, metric_id, run_id, pet_id, env_id, metric_type, metric_name, metric_value, unit, tags, snapshots, org_id, created_at, updated_at, deleted_at) VALUES
(1, 'MET001', 'RUN001', 'PET001', 'ENV001', 'performance', 'success_rate', 0.95, '%', 'navigation', '{"attempts": 100, "successes": 95}', 1, NOW(), NOW(), NULL),
(2, 'MET002', 'RUN001', 'PET001', 'ENV001', 'performance', 'avg_completion_time', 12.5, 'seconds', 'navigation', '{"attempts": 100}', 1, NOW(), NOW(), NULL),
(3, 'MET003', 'RUN002', 'PET001', 'ENV003', 'training', 'skill_improvement', 0.15, '%', 'obstacle', '{"baseline": 0.7, "current": 0.85}', 1, NOW(), NOW(), NULL);

-- exploration_sessions
INSERT INTO exploration_sessions (id, session_key, entity_id, entity_type, strategy, exploration_goal, max_duration, max_distance, start_x, start_y, boundary_min_x, boundary_max_x, boundary_min_y, boundary_max_y, waypoints, visited_areas, discovered_objects, coverage_rate, path_length, new_discovery_count, status, progress, started_at, ended_at, pause_duration, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'SESS001', 'PET001', 'pet', 'random_walk', 'Explore living room', 3600, 100.00, 0.00, 0.00, -10.00, 10.00, -7.50, 7.50, ARRAY['[0,0]', '[5,3]', '[-3,5]'], ARRAY['area_1', 'area_2'], ARRAY['toy_ball', 'rug'], 75.50, 85.30, 5, 'completed', 100.00, '2024-03-20 10:00:00+08', '2024-03-20 11:00:00+08', 120, NULL, NOW(), NOW(), NULL),
(2, 'SESS002', 'PET001', 'pet', 'grid_search', 'Map garden area', 7200, 200.00, 0.00, 0.00, -25.00, 25.00, -25.00, 25.00, ARRAY['[0,0]', '[10,0]', '[10,10]'], ARRAY['zone_a', 'zone_b'], ARRAY['flower_bed', 'pond'], 45.00, 120.50, 12, 'active', 45.00, '2024-03-20 14:00:00+08', NULL, 0, NULL, NOW(), NOW(), NULL);

-- ============================================================================
-- GROUP H: Content Distribution (App Store)
-- ============================================================================

-- app_distributions
INSERT INTO app_distributions (id, name, app_id, version_id, distribution_type, target_ids, target_count, pending_count, success_count, failed_count, status, cancelled_by, cancelled_at, completed_at, created_by, created_at, updated_at, deleted_at) VALUES
(1, 'Production Release v2.0', 1, 1, 'production', '[1,2,3]', 100, 25, 70, 5, 'completed', NULL, NULL, NOW(), 'admin', NOW(), NOW(), NULL),
(2, 'Beta Test Release', 1, 2, 'beta', '[4,5]', 50, 10, 35, 5, 'in_progress', NULL, NULL, NULL, 'admin', NOW(), NOW(), NULL),
(3, 'Internal Test', 2, 3, 'internal', '[1]', 10, 0, 10, 0, 'completed', NULL, NULL, NOW(), 'admin', NOW(), NOW(), NULL);

-- app_install_records
INSERT INTO app_install_records (id, distribution_id, device_id, app_id, version_id, status, installed_at, created_at, updated_at, deleted_at) VALUES
(1, 1, 'DEV001', 1, 1, 'installed', NOW(), NOW(), NOW(), NULL),
(2, 1, 'DEV002', 1, 1, 'installed', NOW(), NOW(), NOW(), NULL),
(3, 2, 'DEV003', 1, 2, 'pending', NULL, NOW(), NOW(), NULL);

-- app_licenses
INSERT INTO app_licenses (id, user_id, app_id, license_key, license_type, purchase_at, expires_at, status, created_at, updated_at, deleted_at) VALUES
(1, 'USER001', 1, 'LIC-2024-001-PRO', 'professional', '2024-01-01 00:00:00+08', '2025-01-01 00:00:00+08', 'active', NOW(), NOW(), NULL),
(2, 'USER002', 1, 'LIC-2024-002-TRIAL', 'trial', '2024-03-01 00:00:00+08', '2024-03-31 00:00:00+08', 'expired', NOW(), NOW(), NULL);

-- store_apps
INSERT INTO store_apps (id, name, bundle_id, description, icon_url, screenshots, category, developer, developer_id, platform, price, currency, rating, install_count, status, review_status, review_note, reviewer_id, reviewed_at, published_at, is_published, version, min_os_version, created_at, updated_at, deleted_at) VALUES
(1, 'PetCare Pro', 'com.petcare.pro', 'Professional pet care management app', 'https://img.example.com/icon/petcare.png', 'https://img.example.com/screen/petcare1.jpg', 'lifestyle', 'PetTech Inc', 1, 'ios', 29.99, 'CNY', 4.80, 50000, 1, 1, 'Approved for publishing', 1, NOW(), NOW(), true, '2.0.0', '14.0', NOW(), NOW(), NULL),
(2, 'PetHealth Tracker', 'com.petcare.health', 'Track your pet health vitals', 'https://img.example.com/icon/health.png', 'https://img.example.com/screen/health1.jpg', 'health', 'PetTech Inc', 1, 'android', 19.99, 'CNY', 4.60, 35000, 1, 1, 'Approved', 1, NOW(), NOW(), true, '1.5.0', '10.0', NOW(), NOW(), NULL),
(3, 'PetFinder', 'com.petcare.finder', 'Find lost pets nearby', 'https://img.example.com/icon/finder.png', 'https://img.example.com/screen/finder1.jpg', 'social', 'PetTech Inc', 1, 'ios', 0.00, 'CNY', 4.90, 80000, 1, 1, 'Approved', 1, NOW(), NOW(), true, '3.0.0', '13.0', NOW(), NOW(), NULL);

-- store_app_versions
INSERT INTO store_app_versions (id, app_id, version, build_number, file_size, file_url, file_md5, min_os_version, release_notes, is_mandatory, is_active, is_latest, download_count, status, created_at, updated_at, deleted_at) VALUES
(1, 1, '2.0.0', '200', 52428800, 'https://download.example.com/petcare_v2.0.0.apk', 'md5:abc123def456', '14.0', 'Major update with new features', true, true, true, 15000, 1, NOW(), NOW(), NULL),
(2, 1, '2.0.1', '201', 52428800, 'https://download.example.com/petcare_v2.0.1.apk', 'md5:def456ghi789', '14.0', 'Bug fixes', false, true, false, 5000, 1, NOW(), NOW(), NULL),
(3, 2, '1.5.0', '150', 45000000, 'https://download.example.com/health_v1.5.0.apk', 'md5:ghi789jkl012', '10.0', 'Health tracking improvements', true, true, true, 8000, 1, NOW(), NOW(), NULL);

-- store_installations
INSERT INTO store_installations (id, app_id, app_version_id, device_id, device_uuid, user_id, tenant_id, status, progress, error_msg, installed_at, uninstalled_at, created_at, updated_at, deleted_at) VALUES
(1, 1, 1, 1, 'DEV001', 1, 1, 1, 100, NULL, NOW(), NULL, NOW(), NOW(), NULL),
(2, 1, 1, 2, 'DEV002', 1, 1, 1, 100, NULL, NOW(), NULL, NOW(), NOW(), NULL),
(3, 2, 3, 1, 'DEV001', 1, 1, 1, 100, NULL, NOW(), NULL, NOW(), NOW(), NULL);

-- store_reviews
INSERT INTO store_reviews (id, app_id, version_id, reviewer_id, status, action, reason, reviewed_at, created_at, updated_at, deleted_at) VALUES
(1, 1, 1, 1, 1, 'approved', NULL, NOW(), NOW(), NOW(), NULL),
(2, 1, 1, 2, 1, 'approved', NULL, NOW(), NOW(), NOW(), NULL),
(3, 2, 3, 3, 1, 'approved', NULL, NOW(), NOW(), NOW(), NULL);

-- ============================================================================
-- GROUP I: Data Analytics
-- ============================================================================

-- analytics_records
INSERT INTO analytics_records (id, tenant_id, analysis_type, period_start, period_end, dimensions, metrics, summary, created_at, updated_at, deleted_at) VALUES
(1, NULL, 'user_activity', '2024-03-01 00:00:00+08', '2024-03-31 23:59:59+08', '{"region": "Shanghai", "platform": "iOS"}', '{"dau": 5000, "mau": 15000, "sessions": 45000}', 'Monthly active users increased by 15%', NOW(), NOW(), NULL),
(2, NULL, 'device_usage', '2024-03-01 00:00:00+08', '2024-03-31 23:59:59+08', '{"device_model": "M5Stack_Pet"}', '{"total_devices": 1000, "active_devices": 850, "avg_online_hours": 18.5}', 'Device engagement stable', NOW(), NOW(), NULL),
(3, NULL, 'revenue', '2024-03-01 00:00:00+08', '2024-03-31 23:59:59+08', '{"subscription_type": "premium"}', '{"mrp": 150000, "arpu": 150, "conversion_rate": 0.05}', 'Revenue growth of 12% MoM', NOW(), NOW(), NULL);

-- custom_reports
INSERT INTO custom_reports (id, tenant_id, name, description, report_config, chart_type, is_scheduled, cron_expr, last_run_at, next_run_at, is_public, created_by, updated_by, created_at, updated_at, deleted_at) VALUES
(1, NULL, 'Weekly Sales Report', 'Weekly breakdown of sales by category', '{"data_source": "orders", "dimensions": ["category", "region"], "metrics": ["revenue", "orders", "avg_order_value"]}', 'bar', true, '0 2 * * 1', NOW(), '2024-03-25 02:00:00+08', true, 1, 1, NOW(), NOW(), NULL),
(2, NULL, 'User Retention Analysis', 'Monthly user retention cohort analysis', '{"data_source": "users", "dimensions": ["cohort_month"], "metrics": ["retention_d1", "retention_d7", "retention_d30"]}', 'line', true, '0 3 1 * *', NOW(), '2024-04-01 03:00:00+08', false, 1, 1, NOW(), NOW(), NULL);

-- export_jobs
INSERT INTO export_jobs (id, tenant_id, export_type, data_source, filters, status, file_path, file_size, record_count, error_msg, started_at, completed_at, expires_at, created_by, created_at, updated_at, deleted_at) VALUES
(1, NULL, 'full_export', 'members', '{"created_after": "2024-01-01"}', 'completed', '/exports/members_20240320.csv', 1048576, 5000, NULL, '2024-03-20 10:00:00+08', '2024-03-20 10:15:00+08', '2024-04-19 10:15:00+08', 1, NOW(), NOW(), NULL),
(2, NULL, 'incremental_export', 'orders', '{"date_range": "2024-03-01 to 2024-03-31"}', 'processing', NULL, 0, 0, NULL, '2024-03-21 14:00:00+08', NULL, '2024-04-20 14:00:00+08', 1, NOW(), NOW(), NULL);

-- ============================================================================
-- GROUP J: Security/Encryption
-- ============================================================================

-- encryption_keys
INSERT INTO encryption_keys (id, key_id, key_version, encrypted_key, is_primary, status, algorithm, rotated_at, expires_at, rotated_by, created_at, updated_at) VALUES
(1, 'KEY001', 1, 'encrypted_content_placeholder_1', true, 1, 'AES-256-GCM', NOW(), '2025-03-20 00:00:00+08', 1, NOW(), NOW()),
(2, 'KEY001', 2, 'encrypted_content_placeholder_2', false, 1, 'AES-256-GCM', NULL, '2026-03-20 00:00:00+08', NULL, NOW(), NOW()),
(3, 'KEY002', 1, 'encrypted_content_placeholder_3', true, 1, 'AES-256-GCM', NOW(), '2025-06-01 00:00:00+08', 1, NOW(), NOW());

-- data_anonymization_records
INSERT INTO data_anonymization_records (id, record_id, original_data, anonymized_data, anonymize_type, fields, user_id, username, purpose, export_format, status, created_at, completed_at) VALUES
(1, 'ANON001', '{"phone": "13812345678", "email": "user@example.com"}', '{"phone": "138****5678", "email": "u***@example.com"}', 'partial_mask', 'phone,email', 1, 'admin', 'GDPR data export', 'json', 1, NOW(), NOW()),
(2, 'ANON002', '{"id_card": "310101199001011234"}', '{"id_card": "****************1234"}', 'full_mask', 'id_card', 1, 'admin', 'Analytics processing', 'csv', 1, NOW(), NOW());

-- data_scopes
INSERT INTO data_scopes (id, role_id, scope_type, dept_ids, store_ids, created_at, updated_at) VALUES
(1, 1, 1, '1,2,3', NULL, NOW(), NOW()),
(2, 2, 2, '1,2', '1,2,3', NOW(), NOW());

-- data_permission_rules
INSERT INTO data_permission_rules (id, name, rule_name, rule_type, resource_type, resource_ids, permission_expr, description, priority, is_active, tenant_id, created_by, created_at, updated_at) VALUES
(1, 'Department Data Access', 'dept_data', 'department', 'orders', NULL, '{"dept_ids": [1, 2]}', 'Allow access to department orders', 50, true, NULL, 1, NOW(), NOW()),
(2, 'Own Records Only', 'own_data', 'owner', 'pets', NULL, '{"owner_id": "current_user"}', 'Users can only access their own pet records', 100, true, NULL, 1, NOW(), NOW());

-- user_data_permissions
INSERT INTO user_data_permissions (id, user_id, role_id, resource_type, rule_type, column_fields, data_scope, filter_expr, priority, is_active, tenant_id, created_by, created_at, updated_at) VALUES
(1, 1, 1, 'orders', 'department', NULL, '{"dept_ids": [1]}', NULL, 50, true, NULL, 1, NOW(), NOW()),
(2, 1, 1, 'members', 'owner', 'phone,email', NULL, '{"owner_id": 1}', 100, true, NULL, 1, NOW(), NOW());

-- ============================================================================
-- GROUP K: Other Configuration Tables
-- ============================================================================

-- translations
INSERT INTO translations (id, locale, key, namespace, value, context, tags, is_active, created_at, updated_at) VALUES
(1, 'en-US', 'common.save', 'common', 'Save', 'Button label', 'button', true, NOW(), NOW()),
(2, 'en-US', 'common.cancel', 'common', 'Cancel', 'Button label', 'button', true, NOW(), NOW()),
(3, 'zh-CN', 'common.save', 'common', '保存', '按钮标签', 'button', true, NOW(), NOW()),
(4, 'zh-CN', 'common.cancel', 'common', '取消', '按钮标签', 'button', true, NOW(), NOW()),
(5, 'en-US', 'pet.profile.title', 'pet', 'Pet Profile', 'Page title', 'page', true, NOW(), NOW());

-- sys_user_exts
INSERT INTO sys_user_exts (id, user_id, employee_id, dept_id, company_id, role_ids, data_scope, created_at, updated_at) VALUES
(1, 1, 10001, 1, 1, '1,2', 1, NOW(), NOW()),
(2, 1, 10002, 2, 1, '2', 2, NOW(), NOW());

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
(1, 'PROF001', 'LIM001', 120, 480, 30, '08:00', '22:00', '[1,2,3,4,5]', 10, 5, true, 30, true, true, NOW(), NOW(), NULL),
(2, 'PROF002', 'LIM002', 60, 240, 15, '09:00', '20:00', '[1,2,3,4,5,6,7]', 15, 10, true, 20, false, true, NOW(), NOW(), NULL);

-- subscription_changes
INSERT INTO subscription_changes (id, change_id, user_id, sub_id, change_type, from_plan_id, to_plan_id, amount, change_reason, effective_at, created_at, updated_at, deleted_at) VALUES
(1, 'CHANGE001', 1, 'SUB001', 'upgrade', 'PLAN_BASIC', 'PLAN_PREMIUM', 100.00, 'Want more features', '2024-03-15 00:00:00+08', NOW(), NOW(), NULL),
(2, 'CHANGE002', 1, 'SUB002', 'downgrade', 'PLAN_PREMIUM', 'PLAN_BASIC', -50.00, 'Cost reduction', '2024-03-20 00:00:00+08', NOW(), NOW(), NULL);

-- wipe_history
INSERT INTO wipe_history (id, device_id, operator_id, operator_name, wipe_type, status, confirm_token, confirmed_at, executed_at, completed_at, result, reason, tenant_id, created_at, updated_at) VALUES
(1, 'DEV001', 1, 'Admin', 'factory_reset', 'completed', 'token123', '2024-03-10 10:00:00+08', '2024-03-10 10:01:00+08', '2024-03-10 10:05:00+08', 'Device wiped successfully', 'Device reported stolen', NULL, NOW(), NOW()),
(2, 'DEV002', 1, 'Admin', 'data_wipe', 'pending', 'token456', NULL, NULL, NULL, NULL, 'User requested data wipe', NULL, NOW(), NOW());

-- finder_alerts
INSERT INTO finder_alerts (id, alert_uuid, user_id, species, latitude, longitude, radius_km, notify_email, notify_sms, notify_app, is_active, tenant_id, created_at, updated_at, deleted_at) VALUES
(1, 'ALERT001', 1, 'cat', 31.2304, 121.4740, 10.00, true, false, true, true, NULL, NOW(), NOW(), NULL),
(2, 'ALERT002', 1, 'dog', 31.2204, 121.5440, 5.00, true, true, true, true, NULL, NOW(), NOW(), NULL);

-- sighting_reports
INSERT INTO sighting_reports (id, sighting_uuid, report_uuid, location, sighting_time, description, photo_url, reporter_name, contact_phone, is_credible, reporter_id, tenant_id, created_at) VALUES
(1, 'SIGHT001', 'RPT001', '{"lat": 31.2304, "lng": 121.4740, "address": "Nanjing Road"}', '2024-03-15 16:00:00+08', 'Orange tabby cat resting under bench', 'https://photo.example.com/sight/001.jpg', 'John Doe', '13900001111', true, 1, NULL, NOW()),
(2, 'SIGHT002', 'RPT001', '{"lat": 31.2254, "lng": 121.4540, "address": "Jing An Park"}', '2024-03-15 18:00:00+08', 'Small white dog, appears lost', 'https://photo.example.com/sight/002.jpg', 'Jane Smith', '13900002222', true, 1, NULL, NOW());

-- vaccination_reminders
INSERT INTO vaccination_reminders (id, vaccination_id, pet_id, user_id, remind_at, remind_type, is_sent, is_completed, memo, created_at) VALUES
(1, 1, 1, 1, '2025-01-10 10:00:00+08', 'email', false, false, 'Annual rabies booster reminder', NOW()),
(2, 2, 1, 1, '2024-08-15 14:00:00+08', 'sms', false, false, 'Distemper booster reminder', NOW());

-- ============================================================================
-- GROUP L: GDPR/Compliance
-- ============================================================================

-- gdpr_requests
INSERT INTO gdpr_requests (id, request_id, request_type, requester_email, requester_name, user_id, status, request_reason, processed_by, processed_at, completed_at, rejected_reason, export_path, response_data, tenant_id, created_at, updated_at) VALUES
(1, 'GDPR001', 'data_export', 'user@example.com', 'Zhang San', 1, 2, 'Want to download my data', 1, NOW(), NOW(), NULL, '/exports/gdpr/GDPR001.zip', '{"profile": {}, "orders": []}', 1, NOW(), NOW()),
(2, 'GDPR002', 'data_deletion', 'user2@example.com', 'Li Si', NULL, 1, 'Want to delete my account', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NOW(), NOW()),
(3, 'GDPR003', 'data_portability', 'user3@example.com', 'Wang Wu', 1, 3, 'Request data portability', 1, NOW(), NULL, 'Insufficient verification', NULL, NULL, 1, NOW(), NOW());

-- content_filter_rules
INSERT INTO content_filter_rules (id, profile_id, rule_id, rule_name, filter_level, block_adult, block_violence, block_gambling, block_ads, block_games, allowed_categories, blocked_keywords, allowed_apps, blocked_apps, whitelist_mode, enabled, created_at, updated_at, deleted_at) VALUES
(1, 'PROF001', 'RULE_CF001', 'Child Safe Filter', 2, true, true, true, true, false, NULL, NULL, NULL, NULL, false, true, NOW(), NOW(), NULL),
(2, 'PROF002', 'RULE_CF002', 'Teen Filter', 1, true, true, false, true, true, NULL, NULL, NULL, NULL, false, true, NOW(), NOW(), NULL);

-- compliance_violations
INSERT INTO compliance_violations (id, policy_id, device_id, policy_type, expected_value, actual_value, severity, action_taken, status, resolved_at, resolved_by, created_at) VALUES
(1, 1, 'DEV001', 'firmware_version', 'v2.0.0', 'v1.5.0', 2, 'notified', 1, NULL, NULL, NOW()),
(2, 2, 'DEV002', 'security_patch', '2024-03', '2023-12', 3, 'device_locked', 1, NULL, NULL, NOW());