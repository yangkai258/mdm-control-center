#!/usr/bin/env python3
"""
数据库升级脚本 - 为MBTI测试系统添加社交功能支持
"""

import sqlite3
import sys
import os
import time
import shutil

DB_FILE = "mbti_test.db"

def upgrade_database():
    """升级数据库以支持社交功能"""
    print("开始升级数据库以支持社交功能...")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 1. 创建分享记录表
        print("创建分享记录表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                test_result_id INTEGER NOT NULL,
                share_type VARCHAR(20) NOT NULL,
                share_content TEXT,
                share_image_url VARCHAR(500),
                view_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (test_result_id) REFERENCES test_records(id)
            )
        ''')
        
        # 2. 创建好友关系表
        print("创建好友关系表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS friendships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                friend_id INTEGER NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, friend_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (friend_id) REFERENCES users(id)
            )
        ''')
        
        # 3. 创建社区帖子表
        print("创建社区帖子表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mbti_type VARCHAR(4),
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                like_count INTEGER DEFAULT 0,
                comment_count INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                is_pinned BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # 4. 创建评论表
        print("创建评论表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                like_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # 5. 创建点赞表
        print("创建点赞表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                comment_id INTEGER,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(post_id, comment_id, user_id),
                FOREIGN KEY (post_id) REFERENCES posts(id),
                FOREIGN KEY (comment_id) REFERENCES comments(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                CHECK ((post_id IS NOT NULL) OR (comment_id IS NOT NULL))
            )
        ''')
        
        # 6. 为用户表添加社交相关字段
        print("为用户表添加社交相关字段...")
        
        # 检查是否已存在这些字段
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # 添加头像URL字段
        if 'avatar_url' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500)")
            print("  添加 avatar_url 字段")
        
        # 添加个人简介字段
        if 'bio' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT")
            print("  添加 bio 字段")
        
        # 添加MBTI类型字段（缓存用户的最新测试结果）
        if 'mbti_type' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN mbti_type VARCHAR(4)")
            print("  添加 mbti_type 字段")
        
        # 添加好友数量字段
        if 'friend_count' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN friend_count INTEGER DEFAULT 0")
            print("  添加 friend_count 字段")
        
        # 添加帖子数量字段
        if 'post_count' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN post_count INTEGER DEFAULT 0")
            print("  添加 post_count 字段")
        
        # 7. 为测试记录表添加分享相关字段
        print("为测试记录表添加分享相关字段...")
        cursor.execute("PRAGMA table_info(test_records)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # 添加分享次数字段
        if 'share_count' not in columns:
            cursor.execute("ALTER TABLE test_records ADD COLUMN share_count INTEGER DEFAULT 0")
            print("  添加 share_count 字段")
        
        # 添加查看次数字段
        if 'view_count' not in columns:
            cursor.execute("ALTER TABLE test_records ADD COLUMN view_count INTEGER DEFAULT 0")
            print("  添加 view_count 字段")
        
        # 8. 创建索引以提高查询性能
        print("创建索引...")
        
        # 分享记录索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_shares_user_id ON shares(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_shares_test_result_id ON shares(test_result_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_shares_created_at ON shares(created_at)")
        
        # 好友关系索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_friendships_user_id ON friendships(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_friendships_friend_id ON friendships(friend_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_friendships_status ON friendships(status)")
        
        # 帖子索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_mbti_type ON posts(mbti_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_like_count ON posts(like_count)")
        
        # 评论索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id)")
        
        # 点赞索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_likes_post_id ON likes(post_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_likes_comment_id ON likes(comment_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_likes_user_id ON likes(user_id)")
        
        # 提交更改
        conn.commit()
        
        print("\n数据库升级完成！")
        print("已创建以下表：")
        print("  1. shares - 分享记录表")
        print("  2. friendships - 好友关系表")
        print("  3. posts - 社区帖子表")
        print("  4. comments - 评论表")
        print("  5. likes - 点赞表")
        print("\n已添加以下字段：")
        print("  1. users表: avatar_url, bio, mbti_type, friend_count, post_count")
        print("  2. test_records表: share_count, view_count")
        
        # 显示表结构
        print("\n当前数据库表结构：")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n{table_name}:")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"数据库升级失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_database():
    """验证数据库升级结果"""
    print("\n验证数据库升级结果...")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 检查所有表是否存在
        required_tables = ['shares', 'friendships', 'posts', 'comments', 'likes']
        
        for table in required_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"  ✓ {table} 表存在")
            else:
                print(f"  ✗ {table} 表不存在")
        
        # 检查用户表的新字段
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [column[1] for column in cursor.fetchall()]
        required_user_columns = ['avatar_url', 'bio', 'mbti_type', 'friend_count', 'post_count']
        
        for column in required_user_columns:
            if column in user_columns:
                print(f"  ✓ users.{column} 字段存在")
            else:
                print(f"  ✗ users.{column} 字段不存在")
        
        # 检查测试记录表的新字段
        cursor.execute("PRAGMA table_info(test_records)")
        test_columns = [column[1] for column in cursor.fetchall()]
        required_test_columns = ['share_count', 'view_count']
        
        for column in required_test_columns:
            if column in test_columns:
                print(f"  ✓ test_records.{column} 字段存在")
            else:
                print(f"  ✗ test_records.{column} 字段不存在")
        
        conn.close()
        print("\n验证完成！")
        return True
        
    except Exception as e:
        print(f"验证失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("MBTI测试系统 - 数据库升级工具")
    print("=" * 60)
    
    # 检查数据库文件是否存在
    if not os.path.exists(DB_FILE):
        print(f"错误：数据库文件 {DB_FILE} 不存在！")
        print("请先运行MBTI测试服务器以创建数据库。")
        return False
    
    # 备份原始数据库
    backup_file = f"{DB_FILE}.backup.{int(time.time())}"
    print(f"创建数据库备份: {backup_file}")
    try:
        shutil.copy2(DB_FILE, backup_file)
        print("备份创建成功！")
    except Exception as e:
        print(f"备份失败: {e}")
        print("继续升级...")
    
    # 执行升级
    if upgrade_database():
        print("\n" + "=" * 60)
        print("升级成功！")
        print("=" * 60)
        
        # 验证升级结果
        verify_database()
        
        print("\n下一步：")
        print("1. 重启MBTI测试服务器以应用更改")
        print("2. 开始开发社交功能API")
        print("3. 更新前端界面以支持社交功能")
        
        return True
    else:
        print("\n" + "=" * 60)
        print("升级失败！")
        print("=" * 60)
        print("请检查错误信息并手动修复。")
        return False

if __name__ == "__main__":
    import time
    main()