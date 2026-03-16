                order_clause = "ORDER BY (p.like_count * 2 + p.comment_count) / (1 + (strftime('%s', 'now') - strftime('%s', p.created_at)) / 3600) DESC"
            
            query = f'''
                SELECT p.*, u.username, u.nickname, u.avatar_url, u.mbti_type as user_mbti
                FROM posts p
                JOIN users u ON p.user_id = u.id
                {where_clause}
                {order_clause}
                LIMIT ? OFFSET ?
            '''
            
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            posts = []
            for row in cursor.fetchall():
                post = dict(row)
                posts.append(post)
            
            # 获取总数
            count_query = f'''
                SELECT COUNT(*) as total FROM posts p {where_clause}
            '''
            count_params = params[:-2]  # 移除limit和offset参数
            cursor.execute(count_query, count_params)
            total = cursor.fetchone()['total']
            
            return {
                "success": True,
                "posts": posts,
                "total": total,
                "limit": limit,
                "offset": offset
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"获取帖子列表失败: {str(e)}"
            }
    
    def get_post_detail(self, post_id):
        """获取帖子详情"""
        try:
            cursor = self.conn.cursor()
            
            # 获取帖子详情
            cursor.execute('''
                SELECT p.*, u.username, u.nickname, u.avatar_url, u.mbti_type as user_mbti
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = ?
            ''', (post_id,))
            
            post = cursor.fetchone()
            if not post:
                return {
                    "success": False,
                    "error": "帖子不存在"
                }
            
            post_dict = dict(post)
            
            # 增加查看次数
            cursor.execute('''
                UPDATE posts SET view_count = view_count + 1 WHERE id = ?
            ''', (post_id,))
            
            # 获取评论
            cursor.execute('''
                SELECT c.*, u.username, u.nickname, u.avatar_url
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = ?
                ORDER BY c.created_at ASC
            ''', (post_id,))
            
            comments = []
            for row in cursor.fetchall():
                comment = dict(row)
                comments.append(comment)
            
            self.conn.commit()
            
            return {
                "success": True,
                "post": post_dict,
                "comments": comments,
                "comment_count": len(comments)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"获取帖子详情失败: {str(e)}"
            }
    
    def create_comment(self, user_id, post_id, content):
        """创建评论"""
        try:
            cursor = self.conn.cursor()
            
            # 插入评论
            cursor.execute('''
                INSERT INTO comments (post_id, user_id, content)
                VALUES (?, ?, ?)
            ''', (post_id, user_id, content))
            
            comment_id = cursor.lastrowid
            
            # 更新帖子的评论计数
            cursor.execute('''
                UPDATE posts SET comment_count = comment_count + 1 WHERE id = ?
            ''', (post_id,))
            
            self.conn.commit()
            
            # 获取完整的评论信息
            cursor.execute('''
                SELECT c.*, u.username, u.nickname, u.avatar_url
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = ?
            ''', (comment_id,))
            
            comment_info = dict(cursor.fetchone())
            
            return {
                "success": True,
                "comment_id": comment_id,
                "message": "评论创建成功",
                "comment": comment_info
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"创建评论失败: {str(e)}"
            }
    
    def like_post(self, user_id, post_id):
        """点赞帖子"""
        try:
            cursor = self.conn.cursor()
            
            # 检查是否已经点赞
            cursor.execute('''
                SELECT * FROM likes 
                WHERE post_id = ? AND user_id = ? AND comment_id IS NULL
            ''', (post_id, user_id))
            
            existing = cursor.fetchone()
            if existing:
                return {
                    "success": False,
                    "error": "已经点赞过该帖子"
                }
            
            # 插入点赞记录
            cursor.execute('''
                INSERT INTO likes (post_id, user_id)
                VALUES (?, ?)
            ''', (post_id, user_id))
            
            # 更新帖子的点赞计数
            cursor.execute('''
                UPDATE posts SET like_count = like_count + 1 WHERE id = ?
            ''', (post_id,))
            
            self.conn.commit()
            
            # 获取更新后的点赞数
            cursor.execute('SELECT like_count FROM posts WHERE id = ?', (post_id,))
            like_count = cursor.fetchone()['like_count']
            
            return {
                "success": True,
                "message": "点赞成功",
                "like_count": like_count
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"点赞失败: {str(e)}"
            }
    
    def unlike_post(self, user_id, post_id):
        """取消点赞帖子"""
        try:
            cursor = self.conn.cursor()
            
            # 检查是否已经点赞
            cursor.execute('''
                SELECT * FROM likes 
                WHERE post_id = ? AND user_id = ? AND comment_id IS NULL
            ''', (post_id, user_id))
            
            existing = cursor.fetchone()
            if not existing:
                return {
                    "success": False,
                    "error": "尚未点赞该帖子"
                }
            
            # 删除点赞记录
            cursor.execute('''
                DELETE FROM likes 
                WHERE post_id = ? AND user_id = ? AND comment_id IS NULL
            ''', (post_id, user_id))
            
            # 更新帖子的点赞计数
            cursor.execute('''
                UPDATE posts SET like_count = like_count - 1 WHERE id = ?
            ''', (post_id,))
            
            self.conn.commit()
            
            # 获取更新后的点赞数
            cursor.execute('SELECT like_count FROM posts WHERE id = ?', (post_id,))
            like_count = cursor.fetchone()['like_count']
            
            return {
                "success": True,
                "message": "取消点赞成功",
                "like_count": like_count
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"取消点赞失败: {str(e)}"
            }
    
    def like_comment(self, user_id, comment_id):
        """点赞评论"""
        try:
            cursor = self.conn.cursor()
            
            # 检查是否已经点赞
            cursor.execute('''
                SELECT * FROM likes 
                WHERE comment_id = ? AND user_id = ?
            ''', (comment_id, user_id))
            
            existing = cursor.fetchone()
            if existing:
                return {
                    "success": False,
                    "error": "已经点赞过该评论"
                }
            
            # 插入点赞记录
            cursor.execute('''
                INSERT INTO likes (comment_id, user_id)
                VALUES (?, ?)
            ''', (comment_id, user_id))
            
            # 更新评论的点赞计数
            cursor.execute('''
                UPDATE comments SET like_count = like_count + 1 WHERE id = ?
            ''', (comment_id,))
            
            self.conn.commit()
            
            # 获取更新后的点赞数
            cursor.execute('SELECT like_count FROM comments WHERE id = ?', (comment_id,))
            like_count = cursor.fetchone()['like_count']
            
            return {
                "success": True,
                "message": "评论点赞成功",
                "like_count": like_count
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"评论点赞失败: {str(e)}"
            }
    
    # ==================== 用户资料API ====================
    
    def update_user_profile(self, user_id, nickname=None, avatar_url=None, bio=None):
        """更新用户资料"""
        try:
            cursor = self.conn.cursor()
            
            update_fields = []
            params = []
            
            if nickname is not None:
                update_fields.append("nickname = ?")
                params.append(nickname)
            
            if avatar_url is not None:
                update_fields.append("avatar_url = ?")
                params.append(avatar_url)
            
            if bio is not None:
                update_fields.append("bio = ?")
                params.append(bio)
            
            if not update_fields:
                return {
                    "success": False,
                    "error": "没有需要更新的字段"
                }
            
            params.append(user_id)
            
            query = f'''
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE id = ?
            '''
            
            cursor.execute(query, params)
            self.conn.commit()
            
            # 获取更新后的用户信息
            cursor.execute('''
                SELECT id, username, nickname, avatar_url, bio, mbti_type, friend_count, post_count
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user_info = dict(cursor.fetchone())
            
            return {
                "success": True,
                "message": "资料更新成功",
                "user": user_info
            }
            
        except Exception as e:
            self.conn.rollback()
            return {
                "success": False,
                "error": f"更新资料失败: {str(e)}"
            }
    
    def get_user_profile(self, user_id):
        """获取用户资料"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT id, username, nickname, avatar_url, bio, mbti_type, 
                       friend_count, post_count, created_at
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            if not user:
                return {
                    "success": False,
                    "error": "用户不存在"
                }
            
            user_dict = dict(user)
            
            # 获取用户的测试记录
            cursor.execute('''
                SELECT id, mbti_type, status, start_time, end_time, share_count, view_count
                FROM test_records 
                WHERE user_id = ? 
                ORDER BY end_time DESC 
                LIMIT 5
            ''', (user_id,))
            
            test_records = []
            for row in cursor.fetchall():
                record = dict(row)
                test_records.append(record)
            
            user_dict['recent_tests'] = test_records
            
            return {
                "success": True,
                "user": user_dict
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"获取用户资料失败: {str(e)}"
            }
    
    def search_users(self, keyword, limit=20, offset=0):
        """搜索用户"""
        try:
            cursor = self.conn.cursor()
            
            search_pattern = f"%{keyword}%"
            
            cursor.execute('''
                SELECT id, username, nickname, avatar_url, bio, mbti_type, friend_count
                FROM users
                WHERE username LIKE ? OR nickname LIKE ?
                ORDER BY friend_count DESC, username ASC
                LIMIT ? OFFSET ?
            ''', (search_pattern, search_pattern, limit, offset))
            
            users = []
            for row in cursor.fetchall():
                user = dict(row)
                users.append(user)
            
            # 获取总数
            cursor.execute('''
                SELECT COUNT(*) as total 
                FROM users
                WHERE username LIKE ? OR nickname LIKE ?
            ''', (search_pattern, search_pattern))
            
            total = cursor.fetchone()['total']
            
            return {
                "success": True,
                "users": users,
                "total": total,
                "limit": limit,
                "offset": offset
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"搜索用户失败: {str(e)}"
            }
    
    # ==================== 统计功能API ====================
    
    def get_social_stats(self, user_id):
        """获取社交统计信息"""
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # 分享统计
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_shares,
                    SUM(view_count) as total_views,
                    share_type,
                    COUNT(*) as type_count
                FROM shares 
                WHERE user_id = ?
                GROUP BY share_type
            ''', (user_id,))
            
            share_stats = []
            for row in cursor.fetchall():
                share_stats.append(dict(row))
            
            stats['shares'] = {
                "total": sum(item['total_shares'] for item in share_stats) if share_stats else 0,
                "by_type": share_stats
            }
            
            # 好友统计
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_friends,
                    SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) as accepted_friends,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_requests
                FROM friendships 
                WHERE user_id = ? OR friend_id = ?
            ''', (user_id, user_id))
            
            friend_stats = dict(cursor.fetchone())
            stats['friends'] = friend_stats
            
            # 社区统计
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_posts,
                    SUM(like_count) as total_likes,
                    SUM(comment_count) as total_comments,
                    SUM(view_count) as total_views
                FROM posts 
                WHERE user_id = ?
            ''', (user_id,))
            
            post_stats = dict(cursor.fetchone())
            stats['posts'] = post_stats
            
            # 评论统计
            cursor.execute('''
                SELECT COUNT(*) as total_comments_made
                FROM comments 
                WHERE user_id = ?
            ''', (user_id,))
            
            comment_stats = dict(cursor.fetchone())
            stats['comments'] = comment_stats
            
            # 点赞统计
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_likes_given,
                    SUM(CASE WHEN post_id IS NOT NULL THEN 1 ELSE 0 END) as post_likes,
                    SUM(CASE WHEN comment_id IS NOT NULL THEN 1 ELSE 0 END) as comment_likes
                FROM likes 
                WHERE user_id = ?
            ''', (user_id,))
            
            like_stats = dict(cursor.fetchone())
            stats['likes'] = like_stats
            
            return {
                "success": True,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"获取统计信息失败: {str(e)}"
            }


# ==================== API处理器 ====================

class SocialAPIHandler:
    """社交API HTTP处理器"""
    
    def __init__(self):
        self.api = SocialAPI()
    
    def handle_request(self, path, method, headers, body):
        """处理HTTP请求"""
        # 解析路径
        path_parts = path.strip('/').split('/')
        
        if len(path_parts) < 2 or path_parts[0] != 'api':
            return self._error_response(404, "API路径不存在")
        
        api_type = path_parts[1]
        
        # 验证令牌（除了公开API）
        token = headers.get('Authorization', '').replace('Bearer ', '')
        
        if api_type not in ['public', 'stats'] and len(path_parts) > 2:
            user_id = self.api.verify_token(token)
            if not user_id:
                return self._error_response(401, "未授权访问")
        else:
            user_id = None
        
        try:
            # 路由到对应的API处理函数
            if api_type == 'share':
                return self._handle_share_api(path_parts[2:], method, user_id, body)
            elif api_type == 'friend':
                return self._handle_friend_api(path_parts[2:], method, user_id, body)
            elif api_type == 'community':
                return self._handle_community_api(path_parts[2:], method, user_id, body)
            elif api_type == 'user':
                return self._handle_user_api(path_parts[2:], method, user_id, body)
            elif api_type == 'stats':
                return self._handle_stats_api(path_parts[2:], method, user_id, body)
            else:
                return self._error_response(404, "API类型不存在")
                
        except Exception as e:
            return self._error_response(500, f"服务器内部错误: {str(e)}")
    
    def _handle_share_api(self, path_parts, method, user_id, body):
        """处理分享相关API"""
        if method == 'POST' and not path_parts:
            # 创建分享
            data = json.loads(body)
            result = self.api.create_share(
                user_id,
                data.get('test_result_id'),
                data.get('share_type'),
                data.get('share_content'),
                data.get('share_image_url')
            )
            return self._json_response(result)
        
        elif method == 'GET' and not path_parts:
            # 获取用户的分享记录
            params = parse_qs(body) if '=' in body else {}
            limit = int(params.get('limit', [20])[0])
            offset = int(params.get('offset', [0])[0])
            
            result = self.api.get_user_shares(user_id, limit, offset)
            return self._json_response(result)
        
        elif method == 'POST' and len(path_parts) == 1 and path_parts[0] == 'view