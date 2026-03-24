-- ota_packages (固件包) - 3条 (fixed md5 length)
INSERT INTO ota_packages (name, version, hardware_model, file_size, file_url, file_md5, upload_source, is_active, is_mandatory, allow_downgrade, release_notes, created_by, created_at, updated_at) VALUES
('PetBot v1.2.4', 'v1.2.4', 'M5Stack-PetBot-v2', 4194304, 'https://cdn.example.com/firmware/petbot_v124.bin', 'md5:a1b2c3d4e5f6a1b2c3d4e5f6a1', 'official', true, true, false, 'Bug fixes', 'admin', NOW(), NOW());

INSERT INTO ota_packages (name, version, hardware_model, file_size, file_url, file_md5, upload_source, is_active, is_mandatory, allow_downgrade, release_notes, created_by, created_at, updated_at) VALUES
('PetBot v1.2.3', 'v1.2.3', 'M5Stack-PetBot-v2', 4194304, 'https://cdn.example.com/firmware/petbot_v123.bin', 'md5:b2c3d4e5f6a1b2c3d4e5f6a1b2', 'official', true, false, false, 'Speed fix', 'admin', NOW(), NOW());

INSERT INTO ota_packages (name, version, hardware_model, file_size, file_url, file_md5, upload_source, is_active, is_mandatory, allow_downgrade, release_notes, created_by, created_at, updated_at) VALUES
('PetBot v1.1.1', 'v1.1.1', 'M5Stack-PetBot-v1', 3145728, 'https://cdn.example.com/firmware/petbot_v111.bin', 'md5:c3d4e5f6a1b2c3d4e5f6a1b2c3', 'official', true, false, true, 'Minor fix', 'admin', NOW(), NOW());
