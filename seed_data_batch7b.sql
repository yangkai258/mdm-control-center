-- app_versions (应用版本) - fix the 3rd insert
INSERT INTO app_versions (app_id, version, build_number, file_size, file_url, file_md5, min_os_version, release_notes, is_mandatory, is_active, created_at, updated_at) VALUES
(2, '1.8.0', '2026032001', 41943040, 'https://cdn.example.com/apps/petpal_staff_v180.apk', 'md5:c3d4e5f6a1b2c3d4e5f6a1b2c3', 'iOS 13.0', '1. 新增设备批量管理\n2. 优化门店列表加载', true, true, NOW(), NOW());
