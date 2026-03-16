#!/usr/bin/env python3
"""
社交API集成到主服务器的方案
"""

def generate_social_integration_code():
    """生成社交API集成代码"""
    
    code = '''
# ==================== 社交功能集成 ====================

def _handle_social_share(self, data):
    """处理分享相关请求"""
    from social_api_final import SocialAPI
    
    # 验证令牌
    token = self.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        self._send_error(401, "需要认证")
        return
    
    api = SocialAPI()
    user_id = api.verify_token(token)
    if not user_id:
        self._send_error(401, "无效令牌")
        api.close()
        return
    
    action = data.get('action', '')
    
    if action == 'create':
        # 创建分享
        test_result_id = data.get('test_result_id')
        share_type = data.get('share_type', 'wechat')
        share_content = data.get('share_content')
        
        if not test_result_id:
            self._send_error(400, "缺少test_result_id")
            api.close()
            return
        
        result = api.create_share(user_id, test_result_id, share_type, share_content)
        api.close()
        self._send_json_response(result)
    
    elif action == 'list':
        # 获取分享列表
        limit = data.get('limit', 20)
        offset = data.get('offset', 0)
        
        result = api.get_user_shares(user_id, limit, offset)
        api.close()
        self._send_json_response(result)
    
    else:
        api.close()
        self._send_error(400, "无效的分享操作")

def _handle_social_friend(self, data):
    """处理好友相关请求"""
    from social_api_final import SocialAPI
    
    # 验证令牌
    token = self.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        self._send_error(401, "需要认证")
        return
    
    api = SocialAPI()
    user_id = api.verify_token(token)
    if not user_id:
        self._send_error(401, "无效令牌")
        api.close()
        return
    
    action = data.get('action', '')
    
    if action == 'send_request':
        # 发送好友请求
        friend_username = data.get('friend_username')
        if not friend_username:
            self._send_error(400, "缺少friend_username")
            api.close()
            return
        
        result = api.send_friend_request(user_id, friend_username)
        api.close()
        self._send_json_response(result)
    
    elif action == 'get_requests':
        # 获取好友请求列表
        result = api.get_friend_requests(user_id)
        api.close()
        self._send_json_response(result)
    
    elif action == 'accept_request':
        # 接受好友请求
        request_id = data.get('request_id')
        if not request_id:
            self._send_error(400, "缺少request_id")
            api.close()
            return
        
        result = api.accept_friend_request(user_id, request_id)
        api.close()
        self._send_json_response(result)
    
    elif action == 'get_friends':
        # 获取好友列表
        result = api.get_friends(user_id)
        api.close()
        self._send_json_response(result)
    
    elif action == 'compare':
        # MBTI对比
        friend_id = data.get('friend_id')
        if not friend_id:
            self._send_error(400, "缺少friend_id")
            api.close()
            return
        
        result = api.compare_with_friend(user_id, friend_id)
        api.close()
        self._send_json_response(result)
    
    else:
        api.close()
        self._send_error(400, "无效的好友操作")

def _handle_social_community(self, data):
    """处理社区相关请求"""
    from social_api_final import SocialAPI
    
    # 验证令牌（某些操作不需要认证）
    token = self.headers.get('Authorization', '').replace('Bearer ', '')
    api = SocialAPI()
    
    action = data.get('action', '')
    
    if action == 'create_post':
        # 创建帖子（需要认证）
        if not token:
            self._send_error(401, "需要认证")
            api.close()
            return
        
        user_id = api.verify_token(token)
        if not user_id:
            self._send_error(401, "无效令牌")
            api.close()
            return
        
        title = data.get('title')
        content = data.get('content')
        mbti_type = data.get('mbti_type')
        
        if not title or not content:
            self._send_error(400, "缺少标题或内容")
            api.close()
            return
        
        result = api.create_post(user_id, title, content, mbti_type)
        api.close()
        self._send_json_response(result)
    
    elif action == 'get_posts':
        # 获取帖子列表（公开，不需要认证）
        mbti_type = data.get('mbti_type')
        limit = data.get('limit', 20)
        offset = data.get('offset', 0)
        order_by = data.get('order_by', 'newest')
        
        result = api.get_posts(mbti_type, limit, offset, order_by)
        api.close()
        self._send_json_response(result)
    
    elif action == 'create_comment':
        # 创建评论（需要认证）
        if not token:
            self._send_error(401, "需要认证")
            api.close()
            return
        
        user_id = api.verify_token(token)
        if not user_id:
            self._send_error(401, "无效令牌")
            api.close()
            return
        
        post_id = data.get('post_id')
        content = data.get('content')
        
        if not post_id or not content:
            self._send_error(400, "缺少帖子ID或评论内容")
            api.close()
            return
        
        result = api.create_comment(user_id, post_id, content)
        api.close()
        self._send_json_response(result)
    
    elif action == 'like_post':
        # 点赞帖子（需要认证）
        if not token:
            self._send_error(401, "需要认证")
            api.close()
            return
        
        user_id = api.verify_token(token)
        if not user_id:
            self._send_error(401, "无效令牌")
            api.close()
            return
        
        post_id = data.get('post_id')
        if not post_id:
            self._send_error(400, "缺少帖子ID")
            api.close()
            return
        
        result = api.like_post(user_id, post_id)
        api.close()
        self._send_json_response(result)
    
    else:
        api.close()
        self._send_error(400, "无效的社区操作")

def _handle_social_profile(self, data):
    """处理用户资料相关请求"""
    from social_api_final import SocialAPI
    
    # 验证令牌
    token = self.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        self._send_error(401, "需要认证")
        return
    
    api = SocialAPI()
    user_id = api.verify_token(token)
    if not user_id:
        self._send_error(401, "无效令牌")
        api.close()
        return
    
    action = data.get('action', '')
    
    if action == 'update':
        # 更新用户资料
        nickname = data.get('nickname')
        avatar_url = data.get('avatar_url')
        bio = data.get('bio')
        
        result = api.update_user_profile(user_id, nickname, avatar_url, bio)
        api.close()
        self._send_json_response(result)
    
    elif action == 'get':
        # 获取用户资料
        target_user_id = data.get('user_id', user_id)
        
        result = api.get_user_profile(target_user_id)
        api.close()
        self._send_json_response(result)
    
    elif action == 'search':
        # 搜索用户
        keyword = data.get('keyword')
        if not keyword:
            self._send_error(400, "缺少搜索关键词")
            api.close()
            return
        
        limit = data.get('limit', 20)
        offset = data.get('offset', 0)
        
        result = api.search_users(keyword, limit, offset)
        api.close()
        self._send_json_response(result)
    
    else:
        api.close()
        self._send_error(400, "无效的资料操作")

def _handle_social_stats(self, data):
    """处理社交统计请求"""
    from social_api_final import SocialAPI
    
    action = data.get('action', '')
    api = SocialAPI()
    
    if action == 'user_stats':
        # 获取用户社交统计（需要认证）
        token = self.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            self._send_error(401, "需要认证")
            api.close()
            return
        
        user_id = api.verify_token(token)
        if not user_id:
            self._send_error(401, "无效令牌")
            api.close()
            return
        
        result = api.get_social_stats(user_id)
        api.close()
        self._send_json_response(result)
    
    elif action == 'community_stats':
        # 获取社区整体统计（公开）
        result = api.get_community_stats()
        api.close()
        self._send_json_response(result)
    
    else:
        api.close()
        self._send_error(400, "无效的统计操作")
'''
    
    return code

def generate_server_modifications():
    """生成服务器修改代码"""
    
    modifications = '''
# 在do_GET方法中添加社交API路由（GET请求）
elif path == '/api/social/posts':
    # 获取帖子列表
    query_params = parse_qs(parsed_path.query)
    data = {
        'action': 'get_posts',
        'mbti_type': query_params.get('mbti_type', [None])[0],
        'limit': int(query_params.get('limit', [20])[0]),
        'offset': int(query_params.get('offset', [0])[0]),
        'order_by': query_params.get('order_by', ['newest'])[0]
    }
    self._handle_social_community(data)

elif path == '/api/social/profile':
    # 获取用户资料
    query_params = parse_qs(parsed_path.query)
    data = {
        'action': 'get',
        'user_id': int(query_params.get('user_id', [0])[0])
    }
    self._handle_social_profile(data)

elif path == '/api/social/stats/community':
    # 获取社区统计
    data = {'action': 'community_stats'}
    self._handle_social_stats(data)

# 在do_POST方法中添加社交API路由（POST请求）
elif path == '/api/social/share':
    self._handle_social_share(data)

elif path == '/api/social/friend':
    self._handle_social_friend(data)

elif path == '/api/social/community':
    self._handle_social_community(data)

elif path == '/api/social/profile':
    self._handle_social_profile(data)

elif path == '/api/social/stats':
    self._handle_social_stats(data)
'''
    
    return modifications

def main():
    """主函数"""
    print("社交API集成方案")
    print("="*60)
    
    print("\n1. 需要添加到MBTIServer类的方法:")
    print("-"*40)
    print(generate_social_integration_code())
    
    print("\n2. 需要修改的路由处理:")
    print("-"*40)
    print(generate_server_modifications())
    
    print("\n3. 集成步骤:")
    print("="*60)
    print("""
步骤1: 将social_api_final.py复制到服务器目录
步骤2: 在complete_server.py中添加社交API处理方法
步骤3: 在do_GET和do_POST中添加路由
步骤4: 测试集成功能
步骤5: 创建前端界面调用这些API
    """)
    
    print("\n4. 新API端点:")
    print("="*60)
    print("""
GET端点:
  /api/social/posts          - 获取帖子列表
  /api/social/profile        - 获取用户资料
  /api/social/stats/community - 获取社区统计

POST端点:
  /api/social/share          - 分享相关操作
  /api/social/friend         - 好友相关操作  
  /api/social/community      - 社区相关操作
  /api/social/profile        - 资料相关操作
  /api/social/stats          - 统计相关操作
    """)
    
    print("\n5. 请求参数示例:")
    print("="*60)
    print("""
创建分享:
  POST /api/social/share
  {
    "action": "create",
    "test_result_id": 1,
    "share_type": "wechat",
    "share_content": "我的MBTI测试结果"
  }

获取好友列表:
  POST /api/social/friend
  {
    "action": "get_friends"
  }

创建帖子:
  POST /api/social/community
  {
    "action": "create_post",
    "title": "MBTI讨论",
    "content": "大家觉得INTJ和ENFP配吗？",
    "mbti_type": "INTJ"
  }
    """)

if __name__ == "__main__":
    main()