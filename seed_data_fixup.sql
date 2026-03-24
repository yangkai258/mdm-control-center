-- ota_packages (固件包) - 3条
INSERT INTO ota_packages (name, version, hardware_model, file_size, file_url, file_md5, upload_source, is_active, is_mandatory, allow_downgrade, release_notes, created_by, created_at, updated_at) VALUES
('PetBot v1.2.4 Stable', 'v1.2.4', 'M5Stack-PetBot-v2', 4194304, 'https://cdn.example.com/firmware/petbot_v124.bin', 'md5:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d', 'official', true, true, false, 'Bug fixes and heartbeat optimization', 'admin', NOW(), NOW());

INSERT INTO ota_packages (name, version, hardware_model, file_size, file_url, file_md5, upload_source, is_active, is_mandatory, allow_downgrade, release_notes, created_by, created_at, updated_at) VALUES
('PetBot v1.2.3 Stable', 'v1.2.3', 'M5Stack-PetBot-v2', 4194304, 'https://cdn.example.com/firmware/petbot_v123.bin', 'md5:b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e', 'official', true, false, false, 'Response speed optimization', 'admin', NOW(), NOW());

INSERT INTO ota_packages (name, version, hardware_model, file_size, file_url, file_md5, upload_source, is_active, is_mandatory, allow_downgrade, release_notes, created_by, created_at, updated_at) VALUES
('PetBot v1.1.1 Upgrade', 'v1.1.1', 'M5Stack-PetBot-v1', 3145728, 'https://cdn.example.com/firmware/petbot_v111.bin', 'md5:c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f', 'official', true, false, true, 'Known issue fixes', 'admin', NOW(), NOW());

-- app_versions for app_id=1 (PetPal owner)
INSERT INTO app_versions (app_id, version, build_number, file_size, file_url, file_md5, min_os_version, release_notes, is_mandatory, is_active, created_at, updated_at) VALUES
(1, '2.5.0', '2026032401', 52428800, 'https://cdn.example.com/apps/petpal_owner_v250.apk', 'md5:a1b2c3d4e5f6a1b2c3d4e5f6a1b2', 'iOS 14.0', 'New features and bug fixes', true, true, NOW(), NOW());

INSERT INTO app_versions (app_id, version, build_number, file_size, file_url, file_md5, min_os_version, release_notes, is_mandatory, is_active, created_at, updated_at) VALUES
(1, '2.4.5', '2026031001', 52428800, 'https://cdn.example.com/apps/petpal_owner_v245.apk', 'md5:b2c3d4e5f6a1b2c3d4e5f6a1b2c3', 'iOS 13.0', 'Push notification fix and startup speed', false, true, NOW(), NOW());
