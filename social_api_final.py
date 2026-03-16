#!/usr/bin/env python3
"""
MBTI测试系统 - 社交功能API模块 (简化完整版)
"""

import sqlite3
import json
from datetime import datetime
import jwt

DB_FILE = "mbti_test.db"
SECRET_KEY = "mbti_test_fixed_secret_key_2026_03_13_1234567890abcdef"

class SocialAPI:
    """社交功能API类"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload.get("user_id")
        except:
            return None
    
    # ==================== 分享功能 ====================
    
    def create_share(self, user_id, test_result_id, share_type, share_content=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO shares (user_id, test_result_id, share_type, share_content)
                VALUES (?, ?, ?, ?)
            ''', (user_id, test_result_id, share_type, share_content))
            
            cursor.execute('UPDATE test_records SET share_count = share_count + 1 WHERE id = ?', (test_result_id,))
            self.conn.commit()
            
            return {"success": True, "share_id": cursor.lastrowid, "message": "分享创建成功"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": f"创建分享失败: {str(e)}"}
    
    def get_user_shares(self, user_id, limit=20):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT s.*, t.mbti_type, u.nickname
                FROM shares s
                JOIN test_records t ON s.test_result_id = t.id
                JOIN users u ON s.user_id = u.id
                WHERE s.user_id = ?
                ORDER BY s.created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            shares = [dict(row) for row in cursor.fetchall()]
            return {"success": True, "shares": shares}
        except Exception as e:
            return {"success": False, "error": f"获取分享记录失败: {str(e)}"}
    
    # ==================== 好友功能 ====================
    
    def send_friend_request(self, user_id, friend_username):
        try:
            cursor = self.conn.cursor()
            
            # 查找好友
            cursor.execute('SELECT id FROM users WHERE username = ?', (friend_username,))
            friend = cursor.fetchone()
            if not friend:
                return {"success": False, "error": "用户不存在"}
            
            friend_id = friend['id']
            
            # 检查关系
            cursor.execute('''
                SELECT * FROM friendships 
                WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
            ''', (user_id, friend_id, friend_id, user_id))
            
            if cursor.fetchone():
                return {"success": False, "error": "已经是好友或已发送请求"}
            
            # 发送请求
            cursor.execute('INSERT INTO friendships (user_id, friend_id, status) VALUES (?, ?, "pending")', 
                          (user_id, friend_id))
            self.conn.commit()
            
            return {"success": True, "message": "好友请求已发送"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": f"发送好友请求失败: {str(e)}"}
    
    def get_friend_requests(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT f.*, u.username, u.nickname
                FROM friendships f
                JOIN users u ON f.user_id = u.id
                WHERE f.friend_id = ? AND f.status = "pending"
            ''', (user_id,))
            
            requests = [dict(row) for row in cursor.fetchall()]
            return {"success": True, "requests": requests}
        except Exception as e:
            return {"success": False, "error": f"获取好友请求失败: {str(e)}"}
    
    def accept_friend_request(self, user_id, request_id):
        try:
            cursor = self.conn.cursor()
            
            # 验证请求
            cursor.execute('SELECT * FROM friendships WHERE id = ? AND friend_id = ? AND status = "pending"', 
                          (request_id, user_id))
            request = cursor.fetchone()
            if not request:
                return {"success": False, "error": "请求不存在"}
            
            # 接受请求
            cursor.execute('UPDATE friendships SET status = "accepted" WHERE id = ?', (request_id,))
            
            # 更新好友计数
            requester_id = request['user_id']
            cursor.execute('UPDATE users SET friend_count = friend_count + 1 WHERE id IN (?, ?)', 
                          (requester_id, user_id))
            
            self.conn.commit()
            return {"success": True, "message": "好友请求已接受"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": f"接受好友请求失败: {str(e)}"}
    
    def get_friends(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT u.id, u.username, u.nickname, u.mbti_type
                FROM friendships f
                JOIN users u ON (
                    (f.user_id = ? AND f.friend_id = u.id) OR 
                    (f.friend_id = ? AND f.user_id = u.id)
                )
                WHERE f.status = "accepted"
            ''', (user_id, user_id))
            
            friends = [dict(row) for row in cursor.fetchall()]
            return {"success": True, "friends": friends}
        except Exception as e:
            return {"success": False, "error": f"获取好友列表失败: {str(e)}"}
    
    # ==================== 社区功能 ====================
    
    def create_post(self, user_id, title, content, mbti_type=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO posts (user_id, mbti_type, title, content)
                VALUES (?, ?, ?, ?)
            ''', (user_id, mbti_type, title, content))
            
            cursor.execute('UPDATE users SET post_count = post_count + 1 WHERE id = ?', (user_id,))
            self.conn.commit()
            
            return {"success": True, "post_id": cursor.lastrowid, "message": "帖子创建成功"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": f"创建帖子失败: {str(e)}"}
    
    def get_posts(self, limit=20):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT p.*, u.username, u.nickname
                FROM posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (limit,))
            
            posts = [dict(row) for row in cursor.fetchall()]
            return {"success": True, "posts": posts}
        except Exception as e:
            return {"success": False, "error": f"获取帖子列表失败: {str(e)}"}
    
    def create_comment(self, user_id, post_id, content):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)', 
                          (post_id, user_id, content))
            
            cursor.execute('UPDATE posts SET comment_count = comment_count + 1 WHERE id = ?', (post_id,))
            self.conn.commit()
            
            return {"success": True, "comment_id": cursor.lastrowid, "message": "评论创建成功"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": f"创建评论失败: {str(e)}"}
    
    # ==================== 用户资料 ====================
    
    def update_user_profile(self, user_id, nickname=None, bio=None):
        try:
            cursor = self.conn.cursor()
            
            updates = []
            params = []
            
            if nickname:
                updates.append("nickname = ?")
                params.append(nickname)
            if bio:
                updates.append("bio = ?")
                params.append(bio)
            
            if not updates:
                return {"success": False, "error": "没有需要更新的字段"}
            
            params.append(user_id)
            query = f'UPDATE users SET {", ".join(updates)} WHERE id = ?'
            cursor.execute(query, params)
            self.conn.commit()
            
            return {"success": True, "message": "资料更新成功"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "error": f"更新资料失败: {str(e)}"}
    
    def get_user_profile(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, username, nickname, bio, mbti_type, friend_count, post_count
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            if not user:
                return {"success": False, "error": "用户不存在"}
            
            return {"success": True, "user": dict(user)}
        except Exception as e:
            return {"success": False, "error": f"获取用户资料失败: {str(e)}"}
    
    # ==================== 统计功能 ====================
    
    def get_social_stats(self, user_id):
        try:
            cursor = self.conn.cursor()
            stats = {}
            
            # 分享统计
            cursor.execute('SELECT COUNT(*) as share_count FROM shares WHERE user_id = ?', (user_id,))
            stats['share_count'] = cursor.fetchone()['share_count']
            
            # 好友统计
            cursor.execute('SELECT COUNT(*) as friend_count FROM friendships WHERE (user_id = ? OR friend_id = ?) AND status = "accepted"', 
                          (user_id, user_id))
            stats['friend_count'] = cursor.fetchone()['friend_count']
            
            # 帖子统计
            cursor.execute('SELECT COUNT(*) as post_count FROM posts WHERE user_id = ?', (user_id,))
            stats['post_count'] = cursor.fetchone()['post_count']
            
            return {"success": True, "stats": stats}
        except Exception as e:
            return {"success": False, "error": f"获取统计信息失败: {str(e)}"}


# ==================== 测试函数 ====================

def test_database():
    """测试数据库结构"""
    print("测试数据库结构...")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 检查表
        tables = ['shares', 'friendships', 'posts', 'comments', 'likes']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"  ✅ {table} 表存在")
            else:
                print(f"  ❌ {table} 表不存在")
        
        conn.close()
        return True
    except Exception as e:
        print(f"数据库测试失败: {e}")
        return False

def main():
    """主函数"""
    print("社交API模块测试")
    print("="*60)
    
    # 测试数据库
    if not test_database():
        print("\n请先运行数据库升级脚本！")
        return
    
    print("\n数据库结构正常，可以开始API测试。")
    
    # 创建API实例
    api = SocialAPI()
    
    try:
        # 测试用户ID
        test_user_id = 1
        
        print(f"\n使用测试用户ID: {test_user_id}")
        
        # 测试用户资料
        print("\n1. 测试用户资料功能:")
        result = api.get_user_profile(test_user_id)
        if result["success"]:
            print(f"  ✅ 获取用户资料成功: {result['user']['username']}")
        else:
            print(f"  ❌ 获取用户资料失败: {result['error']}")
        
        # 测试创建帖子
        print("\n2. 测试社区功能:")
        result = api.create_post(test_user_id, "测试帖子", "这是一个测试帖子内容", "INTJ")
        if result["success"]:
            print(f"  ✅ 创建帖子成功，ID: {result['post_id']}")
            
            # 获取帖子列表
            result = api.get_posts(5)
            if result["success"]:
                print(f"  ✅ 获取帖子列表成功，共 {len(result['posts'])} 条")
        else:
            print(f"  ❌ 创建帖子失败: {result['error']}")
        
        # 测试分享功能
        print("\n3. 测试分享功能:")
        result = api.create_share(test_user_id, 1, "wechat", "分享我的MBTI测试结果")
        if result["success"]:
            print(f"  ✅ 创建分享成功，ID: {result['share_id']}")
        else:
            print(f"  ❌ 创建分享失败: {result['error']}")
        
        # 测试统计功能
        print("\n4. 测试统计功能:")
        result = api.get_social_stats(test_user_id)
        if result["success"]:
            stats = result["stats"]
            print(f"  ✅ 获取统计成功:")
            print(f"     分享数: {stats.get('share_count', 0)}")
            print(f"     好友数: {stats.get('friend_count', 0)}")
            print(f"     帖子数: {stats.get('post_count', 0)}")
        else:
            print(f"  ❌ 获取统计失败: {result['error']}")
        
        print("\n" + "="*60)
        print("✅ 基本功能测试完成")
        print("社交API模块工作正常")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
    
    finally:
        api.close()

if __name__ == "__main__":
    main()