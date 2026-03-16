#!/usr/bin/env python3
"""
MBTI测试系统 - 社交功能API模块
提供分享、好友、社区等社交功能API
"""

import sqlite3
import json
import time
from datetime import datetime
from urllib.parse import parse_qs
import jwt

DB_FILE = "mbti_test.db"
SECRET_KEY = "mbti_test_fixed_secret_key_2026_03_13_1234567890abcdef"

class SocialAPI:
    """社交功能API处理类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
    
    def verify_token(self, token):
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    # ==================== 分享功能API ====================
    
    def create_share(self, user_id, test_result_id, share_type, share_content=None, share_image_url=None):
        """创建分享记录"""
        try:
            cursor = self.conn.cursor()
            
            # 插入分享记录
            cursor.execute('''
                INSERT INTO shares (user_id, test_result_id, share_type, share_content, share_image_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, test_result_id, share_type, share_content, share_image_url))
            
            share_id = cursor.lastrowid
            
            # 更新测试记录的分享计数
            cursor.execute('''
                UPDATE test_records 
                SET share_count = share_count + 1 
                WHERE id = ?
            ''', (test_result_id,))
            
            self.conn.commit()
            
            return {
                "success": True,
                "share_id": share_id,
                "message": "分享创建成功"
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"创建分享失败: {str(e)}"
            }
    
    def get_user_shares(self, user_id, limit=20, offset=0):
        """获取用户的分享记录"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT s.*, t.mbti_type, u.nickname, u.avatar_url
                FROM shares s
                JOIN test_records t ON s.test_result_id = t.id
                JOIN users u ON s.user_id = u.id
                WHERE s.user_id = ?
                ORDER BY s.created_at DESC
                LIMIT ? OFFSET ?
            ''', (user_id, limit, offset))
            
            shares = []
            for row in cursor.fetchall():
                share = dict(row)
                # 转换时间格式
                if share['created_at']:
                    share['created_at'] = share['created_at']
                shares.append(share)
            
            # 获取总数
            cursor.execute('''
                SELECT COUNT(*) as total FROM shares WHERE user_id = ?
            ''', (user_id,))
            total = cursor.fetchone()['total']
            
            return {
                "success": True,
                "shares": shares,
                "total": total,
                "limit": limit,
                "offset": offset
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"获取分享记录失败: {str(e)}"
            }
    
    def record_share_view(self, share_id):
        """记录分享查看次数"""
        try:
            cursor = self.conn.cursor()
            
            # 更新分享查看次数
            cursor.execute('''
                UPDATE shares 
                SET view_count = view_count + 1 
                WHERE id = ?
            ''', (share_id,))
            
            # 获取对应的测试记录ID
            cursor.execute('''
                SELECT test_result_id FROM shares WHERE id = ?
            ''', (share_id,))
            result = cursor.fetchone()
            
            if result:
                test_result_id = result['test_result_id']
                # 更新测试记录查看次数
                cursor.execute('''
                    UPDATE test_records 
                    SET view_count = view_count + 1 
                    WHERE id = ?
                ''', (test_result_id,))
            
            self.conn.commit()
            
            return {
                "success": True,
                "message": "查看记录成功"
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"记录查看失败: {str(e)}"
            }
    
    # ==================== 好友功能API ====================
    
    def send_friend_request(self, user_id, friend_username):
        """发送好友请求"""
        try:
            cursor = self.conn.cursor()
            
            # 查找好友用户ID
            cursor.execute('SELECT id FROM users WHERE username = ?', (friend_username,))
            friend_result = cursor.fetchone()
            
            if not friend_result:
                return {
                    "success": False,
                    "error": "用户不存在"
                }
            
            friend_id = friend_result['id']
            
            # 检查是否已经是好友
            cursor.execute('''
                SELECT * FROM friendships 
                WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
            ''', (user_id, friend_id, friend_id, user_id))
            
            existing = cursor.fetchone()
            if existing:
                status = existing['status']
                if status == 'accepted':
                    return {
                        "success": False,
                        "error": "已经是好友"
                    }
                elif status == 'pending':
                    return {
                        "success": False,
                        "error": "好友请求已发送，等待对方接受"
                    }
            
            # 发送好友请求
            cursor.execute('''
                INSERT INTO friendships (user_id, friend_id, status)
                VALUES (?, ?, 'pending')
            ''', (user_id, friend_id))
            
            self.conn.commit()
            
            # 获取好友信息
            cursor.execute('''
                SELECT id, username, nickname, avatar_url, mbti_type, bio 
                FROM users WHERE id = ?
            ''', (friend_id,))
            friend_info = dict(cursor.fetchone())
            
            return {
                "success": True,
                "message": "好友请求已发送",
                "friend": friend_info
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"发送好友请求失败: {str(e)}"
            }
    
    def get_friend_requests(self, user_id):
        """获取好友请求列表"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT f.*, u.username, u.nickname, u.avatar_url, u.mbti_type, u.bio
                FROM friendships f
                JOIN users u ON f.user_id = u.id
                WHERE f.friend_id = ? AND f.status = 'pending'
                ORDER BY f.created_at DESC
            ''', (user_id,))
            
            requests = []
            for row in cursor.fetchall():
                request = dict(row)
                requests.append(request)
            
            return {
                "success": True,
                "requests": requests,
                "count": len(requests)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"获取好友请求失败: {str(e)}"
            }
    
    def accept_friend_request(self, user_id, request_id):
        """接受好友请求"""
        try:
            cursor = self.conn.cursor()
            
            # 验证请求存在且属于当前用户
            cursor.execute('''
                SELECT * FROM friendships 
                WHERE id = ? AND friend_id = ? AND status = 'pending'
            ''', (request_id, user_id))
            
            request = cursor.fetchone()
            if not request:
                return {
                    "success": False,
                    "error": "好友请求不存在或已处理"
                }
            
            # 更新好友关系状态
            cursor.execute('''
                UPDATE friendships 
                SET status = 'accepted', updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (request_id,))
            
            # 更新双方的好友计数
            requester_id = request['user_id']
            
            cursor.execute('''
                UPDATE users SET friend_count = friend_count + 1 WHERE id = ?
            ''', (requester_id,))
            
            cursor.execute('''
                UPDATE users SET friend_count = friend_count + 1 WHERE id = ?
            ''', (user_id,))
            
            self.conn.commit()
            
            # 获取好友信息
            cursor.execute('''
                SELECT id, username, nickname, avatar_url, mbti_type, bio 
                FROM users WHERE id = ?
            ''', (requester_id,))
            friend_info = dict(cursor.fetchone())
            
            return {
                "success": True,
                "message": "好友请求已接受",
                "friend": friend_info
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"接受好友请求失败: {str(e)}"
            }
    
    def get_friends(self, user_id):
        """获取好友列表"""
        try:
            cursor = self.conn.cursor()
            
            # 获取用户的好友（双向关系）
            cursor.execute('''
                SELECT u.id, u.username, u.nickname, u.avatar_url, u.mbti_type, u.bio, u.friend_count,
                       f.created_at as friendship_date
                FROM friendships f
                JOIN users u ON (
                    (f.user_id = ? AND f.friend_id = u.id) OR 
                    (f.friend_id = ? AND f.user_id = u.id)
                )
                WHERE f.status = 'accepted'
                ORDER BY f.updated_at DESC
            ''', (user_id, user_id))
            
            friends = []
            for row in cursor.fetchall():
                friend = dict(row)
                friends.append(friend)
            
            return {
                "success": True,
                "friends": friends,
                "count": len(friends)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"获取好友列表失败: {str(e)}"
            }
    
    def compare_with_friend(self, user_id, friend_id):
        """与好友进行MBTI对比分析"""
        try:
            cursor = self.conn.cursor()
            
            # 获取用户的MBTI类型
            cursor.execute('''
                SELECT mbti_type FROM users WHERE id = ?
            ''', (user_id,))
            user_result = cursor.fetchone()
            
            # 获取好友的MBTI类型
            cursor.execute('''
                SELECT mbti_type FROM users WHERE id = ?
            ''', (friend_id,))
            friend_result = cursor.fetchone()
            
            if not user_result or not user_result['mbti_type']:
                return {
                    "success": False,
                    "error": "用户未完成MBTI测试"
                }
            
            if not friend_result or not friend_result['mbti_type']:
                return {
                    "success": False,
                    "error": "好友未完成MBTI测试"
                }
            
            user_mbti = user_result['mbti_type']
            friend_mbti = friend_result['mbti_type']
            
            # MBTI兼容性分析
            compatibility = self.analyze_mbti_compatibility(user_mbti, friend_mbti)
            
            # 获取好友信息
            cursor.execute('''
                SELECT id, username, nickname, avatar_url, mbti_type, bio 
                FROM users WHERE id = ?
            ''', (friend_id,))
            friend_info = dict(cursor.fetchone())
            
            return {
                "success": True,
                "user_mbti": user_mbti,
                "friend_mbti": friend_mbti,
                "friend_info": friend_info,
                "compatibility": compatibility
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"对比分析失败: {str(e)}"
            }
    
    def analyze_mbti_compatibility(self, mbti1, mbti2):
        """分析两个MBTI类型的兼容性"""
        # 简化的兼容性分析算法
        # 实际应用中可以使用更复杂的算法
        
        if len(mbti1) != 4 or len(mbti2) != 4:
            return {
                "score": 50,
                "level": "中等",
                "description": "MBTI类型不完整，无法进行详细分析"
            }
        
        score = 0
        
        # 分析每个维度的相似性
        dimensions = [
            ("外向(E)", "内向(I)", mbti1[0], mbti2[0]),
            ("实感(S)", "直觉(N)", mbti1[1], mbti2[1]),
            ("思考(T)", "情感(F)", mbti1[2], mbti2[2]),
            ("判断(J)", "感知(P)", mbti1[3], mbti2[3])
        ]
        
        same_count = 0
        analysis = []
        
        for dim_name1, dim_name2, char1, char2 in dimensions:
            if char1 == char2:
                same_count += 1
                analysis.append({
                    "dimension": f"{dim_name1}/{dim_name2}",
                    "status": "相同",
                    "description": f"你们都倾向于{char1}，在这方面有很好的理解"
                })
                score += 25
            else:
                analysis.append({
                    "dimension": f"{dim_name1}/{dim_name2}",
                    "status": "不同",
                    "description": f"你倾向于{char1}，而好友倾向于{char2}，可以互补"
                })
                score += 15
        
        # 根据相同维度数量确定兼容性等级
        if same_count >= 3:
            level = "非常高"
            overall_desc = "你们的MBTI类型非常相似，在很多方面都有共同点"
        elif same_count == 2:
            level = "高"
            overall_desc = "你们的MBTI类型有相似之处，也有互补之处"
        elif same_count == 1:
            level = "中等"
            overall_desc = "你们的MBTI类型有一定差异，但可以互相学习和成长"
        else:
            level = "低"
            overall_desc = "你们的MBTI类型差异较大，需要更多理解和沟通"
        
        return {
            "score": score,
            "level": level,
            "same_dimensions": same_count,
            "overall_description": overall_desc,
            "dimension_analysis": analysis,
            "suggestions": self.get_compatibility_suggestions(mbti1, mbti2)
        }
    
    def get_compatibility_suggestions(self, mbti1, mbti2):
        """获取兼容性建议"""
        suggestions = []
        
        # 沟通建议
        suggestions.append({
            "category": "沟通",
            "suggestion": "定期分享彼此的想法和感受，建立开放的沟通渠道"
        })
        
        # 合作建议
        suggestions.append({
            "category": "合作",
            "suggestion": "在项目中发挥各自的优势，互相补充不足"
        })
        
        # 冲突解决建议
        suggestions.append({
            "category": "冲突解决",
            "suggestion": "当意见不合时，尝试从对方的角度理解问题"
        })
        
        # 成长建议
        suggestions.append({
            "category": "共同成长",
            "suggestion": "互相学习对方的优点，共同提升个人能力"
        })
        
        return suggestions
    
    # ==================== 社区功能API ====================
    
    def create_post(self, user_id, title, content, mbti_type=None):
        """创建社区帖子"""
        try:
            cursor = self.conn.cursor()
            
            # 插入帖子
            cursor.execute('''
                INSERT INTO posts (user_id, mbti_type, title, content)
                VALUES (?, ?, ?, ?)
            ''', (user_id, mbti_type, title, content))
            
            post_id = cursor.lastrowid
            
            # 更新用户的帖子计数
            cursor.execute('''
                UPDATE users SET post_count = post_count + 1 WHERE id = ?
            ''', (user_id,))
            
            self.conn.commit()
            
            # 获取完整的帖子信息
            cursor.execute('''
                SELECT p.*, u.username, u.nickname, u.avatar_url
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = ?
            ''', (post_id,))
            
            post_info = dict(cursor.fetchone())
            
            return {
                "success": True,
                "post_id": post_id,
                "message": "帖子创建成功",
                "post": post_info
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"创建帖子失败: {str(e)}"
            }
    
    def get_posts(self, mbti_type=None, limit=20, offset=0, order_by="newest"):
        """获取帖子列表"""
        try:
            cursor = self.conn.cursor()
            
            # 构建查询条件
            where_clause = "WHERE 1=1"
            params = []
            
            if mbti_type:
                where_clause += " AND p.mbti_type = ?"
                params.append(mbti_type)
            
            # 构建排序条件
            order_clause = "ORDER BY p.created_at DESC"  # 默认按最新排序
            if order_by == "popular":
                order_clause = "ORDER BY p.like_count DESC, p.comment_count DESC"
            elif order_by == "hot":
                # 热门帖子：综合考虑点赞、评论和时间
                order_clause = "ORDER BY (p.like_count * 2 + p.comment_count) / (1 + (strftime('%s', 'now') - strftime('%s', p.created_at)) / 3600)