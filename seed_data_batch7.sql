-- =====================
-- 第7批：内容/社交
-- =====================

-- knowledge (知识库) - 3条
INSERT INTO knowledge (category, question, answer, status, created_at, updated_at) VALUES
('pet_care', '如何给宠物科学减肥？', '宠物减肥需要控制饮食热量摄入，增加运动量。建议：1）减少高热量零食；2）选择低脂宠粮；3）每天固定时间散步；4）避免过度投喂；5）定期称重监控。', 1, NOW(), NOW()),
('health', '宠物疫苗接种时间表', '幼犬/猫：6-8周龄首次疫苗，之后每3-4周加强一次，至16周龄。成年后每年加强一次。核心疫苗包括：狂犬病疫苗、犬瘟热疫苗、猫瘟疫苗等。具体请遵医嘱。', 1, NOW(), NOW()),
('behavior', '狗狗乱叫怎么处理？', '狗狗乱叫的原因包括：分离焦虑、无聊、警告、兴奋等。处理方法：1）正向训练，建立安静指令；2）消耗精力，每天充分运动；3）避免强化乱叫行为；4）提供磨牙玩具分散注意力；5）严重情况咨询行为专家。', 1, NOW(), NOW());

-- pet_social_posts (宠物动态) - 3条
INSERT INTO pet_social_posts (pet_id, content, images, like_count, comment_count, view_count, is_public, created_at, updated_at) VALUES
('DEV001', '今天和小旺一起去了公园，玩得好开心！', 'https://cdn.example.com/photos/post001.jpg', 156, 23, 890, true, NOW(), NOW()),
('DEV002', '咪咪今天特别乖，主动去喝水了~', 'https://cdn.example.com/photos/post002.jpg', 89, 12, 456, true, NOW(), NOW()),
('DEV003', '晒晒我家豆豆的新窝，萌萌哒！', 'https://cdn.example.com/photos/post003.jpg', 234, 45, 1200, true, NOW(), NOW());

-- family_albums (家庭相册) - 3条
INSERT INTO family_albums (uuid, household_id, pet_id, uploader_id, title, description, image_url, thumbnail_url, category, tags, metadata, file_size, width, height, tenant_id, created_at, updated_at) VALUES
('ALBUM001', 1, 1, 1, '小旺的快乐时光', '记录小旺成长的点点滴滴', 'https://cdn.example.com/albums/album001.jpg', 'https://cdn.example.com/albums/album001_thumb.jpg', 'daily', '萌宠,成长记录', '{"camera": "Canon EOS R5"}'::jsonb, 3145728, 4032, 3024, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('ALBUM002', 1, 2, 2, '咪咪的日常', '咪咪的可爱瞬间', 'https://cdn.example.com/albums/album002.jpg', 'https://cdn.example.com/albums/album002_thumb.jpg', 'daily', '萌猫,日常', '{"camera": "iPhone 14 Pro"}'::jsonb, 2097152, 3024, 4032, (SELECT id FROM tenants LIMIT 1), NOW(), NOW()),
('ALBUM003', 2, 3, 3, '豆豆的户外探险', '豆豆在公园玩耍的照片', 'https://cdn.example.com/albums/album003.jpg', 'https://cdn.example.com/albums/album003_thumb.jpg', 'outdoor', '户外,探险,狗狗', '{"camera": "Sony A7IV"}'::jsonb, 4194304, 3840, 2160, (SELECT id FROM tenants LIMIT 1), NOW(), NOW());

-- apps (应用) - 3条
INSERT INTO apps (name, bundle_id, description, icon_url, category, developer, status, platform, created_at, updated_at) VALUES
('PetPal 主人端', 'com.smartepet.owner', '宠物主人管理宠物的手机应用', 'https://cdn.example.com/icons/app_owner.png', 'lifestyle', 'SmartEpet Inc.', 1, 'ios,android', NOW(), NOW()),
('PetPal 店员端', 'com.smartepet.staff', '门店店员使用的管理应用', 'https://cdn.example.com/icons/app_staff.png', 'business', 'SmartEpet Inc.', 1, 'ios,android', NOW(), NOW()),
('PetPal 管理员端', 'com.smartepet.admin', '管理员后台管理应用', 'https://cdn.example.com/icons/app_admin.png', 'business', 'SmartEpet Inc.', 1, 'ios,android', NOW(), NOW());

-- app_versions (应用版本) - 3条
INSERT INTO app_versions (app_id, version, build_number, file_size, file_url, file_md5, min_os_version, release_notes, is_mandatory, is_active, created_at, updated_at) VALUES
(1, '2.5.0', '2026032401', 52428800, 'https://cdn.example.com/apps/petpal_owner_v250.apk', 'md5:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e', 'iOS 14.0', '1. 新增宠物情绪识别功能\n2. 优化设备连接稳定性\n3. 修复已知问题', true, true, NOW(), NOW()),
(1, '2.4.5', '2026031001', 52428800, 'https://cdn.example.com/apps/petpal_owner_v245.apk', 'md5:b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f', 'iOS 13.0', '1. 修复推送问题\n2. 优化启动速度', false, true, NOW(), NOW()),
(2, '1.8.0', '2026032001', 41943040, 'https://cdn.example.com/apps/petpal_staff_v180.apk', 'md5:c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a', 'iOS 13.0', '1. 新增设备批量管理\n2. 优化门店列表加载', true, true, NOW(), NOW());
