-- Remaining AI tables to seed

-- ai_fairness_metrics (uses model_id as primary key)
INSERT INTO ai_fairness_metrics (model_id, model_key, demographic_parity, equal_opportunity, disparate_impact, statistical_parity, precision_gap, recall_gap, false_positive_gap, overall_score, total_tests_run, total_bias_detections, critical_bias_count, high_bias_count, last_updated) VALUES
(1, 'emotion_v1', 0.0230, 0.0150, 0.9500, 0.0200, 0.0180, 0.0120, 0.0150, 0.92, 50, 5, 0, 2, NOW()),
(2, 'health_v2', 0.0310, 0.0280, 0.9200, 0.0280, 0.0250, 0.0300, 0.0220, 0.88, 30, 8, 1, 3, NOW());

-- ai_deploy_sharded
INSERT INTO ai_deploy_sharded (id, model_id, version_id, version, target_env, replica_count, resource_config, status, error_message, started_at, completed_at, deployed_by, org_id, created_at, updated_at) VALUES
(1, 1, 1, 'v1.0.5', 'production', 3, '{"gpu": 1, "memory": "2gb"}', 'completed', NULL, NOW(), NOW(), 1, 1, NOW(), NOW()),
(2, 2, 2, 'v1.2.0', 'staging', 2, '{"gpu": 2, "memory": "4gb"}', 'in_progress', NULL, NOW(), NULL, 1, 1, NOW(), NOW()),
(3, 1, 1, 'v1.0.5', 'edge', 1, '{"gpu": 0.5, "memory": "1gb"}', 'completed', NULL, NOW(), NOW(), 1, 1, NOW(), NOW());

-- ai_model_deploy_history
INSERT INTO ai_model_deploy_history (id, model_id, target_env, replica_count, resource_config, status, started_at, completed_at, error_message, deployed_by, rollback_from, created_at) VALUES
(1, 1, 'production', 3, '{"gpu": 1, "memory": "2gb"}', 'completed', '2024-03-15 10:00:00+08', '2024-03-15 10:30:00+08', NULL, 1, NULL, NOW()),
(2, 2, 'staging', 2, '{"gpu": 2, "memory": "4gb"}', 'in_progress', '2024-03-20 14:00:00+08', NULL, NULL, 1, NULL, NOW()),
(3, 1, 'production', 3, '{"gpu": 1, "memory": "2gb"}', 'rolled_back', '2024-03-10 09:00:00+08', '2024-03-10 09:20:00+08', NULL, 1, NULL, NOW());

-- ai_bias_detections
INSERT INTO ai_bias_detections (id, detection_key, model_id, model_key, input_data, output_data, bias_type, severity, confidence, bias_score, evidence, context, recommendation, detected_at, org_id, create_user_id, created_at, updated_at, deleted_at) VALUES
(1, 'BIAS_DET_001', 1, 'emotion_v1', '{"image": "cat_photo.jpg"}', '{"emotion": "happy"}', 'species', 'low', 0.9500, 0.0200, 'Minor difference in accuracy between cat breeds', 'Comparison of Persian vs Maine Coon', 'Collect more diverse training data', NOW(), 1, 1, NOW(), NOW(), NULL),
(2, 'BIAS_DET_002', 2, 'health_v2', '{"vitals": {"age": 12}}', '{"anomaly": false}', 'age', 'medium', 0.8800, 0.0700, 'Recall 7% lower for senior pets', 'Senior pet health detection', 'Consider age-specific model tuning', NOW(), 1, 1, NOW(), NOW(), NULL);

-- model_shards
INSERT INTO model_shards (id, model_id, version, shard_index, shard_name, file_size, file_path, file_md5, file_sha256, checksum, status, verify_message, verified_at, verified_by, created_by, org_id, created_at, updated_at, deleted_at) VALUES
(1, 1, 'v1.0.5', 0, 'emotion_v1_shard_0.bin', 52428800, '/models/emotion/shard_0_v105.bin', 'abc123def456', 'sha256:a1b2c3d4e5f6', 'SHA256', 'verified', NULL, NOW(), 1, 1, 1, NOW(), NOW(), NULL),
(2, 1, 'v1.0.5', 1, 'emotion_v1_shard_1.bin', 52428800, '/models/emotion/shard_1_v105.bin', 'def456ghi789', 'sha256:f6e5d4c3b2a1', 'SHA256', 'verified', NULL, NOW(), 1, 1, 1, NOW(), NOW(), NULL),
(3, 2, 'v1.2.0', 0, 'health_v2_shard_0.bin', 67108864, '/models/health/shard_0_v120.bin', 'ghi789jkl012', 'sha256:0123456789ab', 'SHA256', 'pending', NULL, NULL, NULL, 1, 1, NOW(), NOW(), NULL);
