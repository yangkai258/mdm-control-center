#!/usr/bin/env python3
"""
社交API功能测试脚本
测试所有社交功能的API接口
"""

import json
from social_api_complete import SocialAPI

def print_test_result(test_name, result):
    """打印测试结果"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")
    
    if result.get("success"):
        print(f"✅ 成功: {result.get('message', '操作成功')}")
        
        # 打印重要数据
        data_keys = [k for k in result.keys() if k not in ['success', 'message', 'error']]
        for key in data_keys:
            if isinstance(result[key], (list, dict)) and result[key]:
                print(f"\n{key}:")
                if isinstance(result[key], list):
                    for i, item in enumerate(result[key][:3]):  # 只显示前3个
                        print(f"  {i+1}. {item}")
                    if len(result[key]) > 3:
                        print(f"  ... 还有 {len(result[key]) - 3} 个")
                else:
                    for k, v in result[key].items():
                        if isinstance(v, (list, dict)) and v:
                            print(f"  {k}: {type(v).__name__} ({len(v) if isinstance(v, list) else len(v.keys())}项)")
                        else:
                            print(f"  {k}: {v}")
    else:
        print(f"❌ 失败: {result.get('error', '未知错误')}")
    
    return result.get("success", False)

def test_share_functions(api, user_id):
    """测试分享功能"""
    print("\n" + "="*60)
    print("测试分享功能")
    print("="*60)
    
    # 假设有一个测试记录ID
    test_result_id = 1
    
    # 1. 创建分享
    result = api.create_share(
        user_id=user_id,
        test_result_id=test_result_id,
        share_type="wechat",
        share_content="我的MBTI测试结果",
        share_image_url="https://example.com/share.jpg"
    )
    success1 = print_test_result("创建分享", result)
    
    if success1:
        share_id = result.get("share_id")
        
        # 2. 获取用户分享记录
        result = api.get_user_shares(user_id, limit=5)
        success2 = print_test_result("获取分享记录", result)
        
        # 3. 记录分享查看
        if share_id:
            result = api.record_share_view(share_id)
            success3 = print_test_result("记录分享查看", result)
    
    return success1

def test_friend_functions(api, user_id):
    """测试好友功能"""
    print("\n" + "="*60)
    print("测试好友功能")
    print("="*60)
    
    # 注意：这里需要实际存在的用户名
    test_friend_username = "test_user"  # 需要修改为实际存在的用户名
    
    # 1. 发送好友请求
    result = api.send_friend_request(user_id, test_friend_username)
    success1 = print_test_result("发送好友请求", result)
    
    # 2. 获取好友请求列表
    result = api.get_friend_requests(user_id)
    success2 = print_test_result("获取好友请求列表", result)
    
    # 3. 获取好友列表
    result = api.get_friends(user_id)
    success3 = print_test_result("获取好友列表", result)
    
    # 4. 如果有好友，测试对比功能
    if success3 and result.get("friends"):
        friend_id = result["friends"][0]["id"]
        result = api.compare_with_friend(user_id, friend_id)
        success4 = print_test_result("MBTI对比分析", result)
    
    return success1 or success2 or success3

def test_community_functions(api, user_id):
    """测试社区功能"""
    print("\n" + "="*60)
    print("测试社区功能")
    print("="*60)
    
    # 1. 创建帖子
    result = api.create_post(
        user_id=user_id,
        title="测试帖子 - MBTI讨论",
        content="这是一个测试帖子，用于测试社区功能。欢迎大家讨论MBTI相关话题！",
        mbti_type="INTJ"
    )
    success1 = print_test_result("创建帖子", result)
    
    if success1:
        post_id = result.get("post_id")
        
        # 2. 获取帖子列表
        result = api.get_posts(limit=5)
        success2 = print_test_result("获取帖子列表", result)
        
        # 3. 获取帖子详情
        if post_id:
            result = api.get_post_detail(post_id)
            success3 = print_test_result("获取帖子详情", result)
            
            # 4. 创建评论
            if success3:
                result = api.create_comment(
                    user_id=user_id,
                    post_id=post_id,
                    content="这是一个测试评论，支持楼主的观点！"
                )
                success4 = print_test_result("创建评论", result)
                
                # 5. 点赞帖子
                result = api.like_post(user_id, post_id)
                success5 = print_test_result("点赞帖子", result)
    
    return success1

def test_user_profile_functions(api, user_id):
    """测试用户资料功能"""
    print("\n" + "="*60)
    print("测试用户资料功能")
    print("="*60)
    
    # 1. 更新用户资料
    result = api.update_user_profile(
        user_id=user_id,
        nickname="测试用户",
        avatar_url="https://example.com/avatar.jpg",
        bio="这是一个测试用户的个人简介"
    )
    success1 = print_test_result("更新用户资料", result)
    
    # 2. 获取用户资料
    result = api.get_user_profile(user_id)
    success2 = print_test_result("获取用户资料", result)
    
    # 3. 搜索用户
    result = api.search_users("测试", limit=5)
    success3 = print_test_result("搜索用户", result)
    
    return success1 or success2 or success3

def test_statistics_functions(api, user_id):
    """测试统计功能"""
    print("\n" + "="*60)
    print("测试统计功能")
    print("="*60)
    
    # 1. 获取用户社交统计
    result = api.get_social_stats(user_id)
    success1 = print_test_result("获取用户社交统计", result)
    
    # 2. 获取社区整体统计
    result = api.get_community_stats()
    success2 = print_test_result("获取社区整体统计", result)
    
    return success1 or success2

def test_all_functions():
    """测试所有功能"""
    print("开始全面测试社交API功能")
    print("="*60)
    
    api = SocialAPI()
    
    try:
        # 使用测试用户ID（需要根据实际情况调整）
        test_user_id = 1
        
        # 测试各功能模块
        test_results = {
            "分享功能": test_share_functions(api, test_user_id),
            "好友功能": test_friend_functions(api, test_user_id),
            "社区功能": test_community_functions(api, test_user_id),
            "用户资料": test_user_profile_functions(api, test_user_id),
            "统计功能": test_statistics_functions(api, test_user_id)
        }
        
        # 打印总结
        print("\n" + "="*60)
        print("测试总结")
        print("="*60)
        
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result)
        
        for module, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{module}: {status}")
        
        print(f"\n总计: {passed_tests}/{total_tests} 个模块测试通过")
        
        if passed_tests == total_tests:
            print("\n🎉 所有测试通过！社交API功能正常。")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} 个模块测试失败，需要检查。")
        
        return passed_tests == total_tests
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        api.close()

def test_database_structure():
    """测试数据库结构"""
    print("\n" + "="*60)
    print("测试数据库结构")
    print("="*60)
    
    try:
        import sqlite3
        
        conn = sqlite3.connect("mbti_test.db")
        cursor = conn.cursor()
        
        # 检查所有社交相关表
        social_tables = ['shares', 'friendships', 'posts', 'comments', 'likes']
        
        print("检查社交相关表结构:")
        
        for table in social_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"  ✅ {table} 表存在")
                
                # 显示表结构
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"    包含 {len(columns)} 个字段:")
                for col in columns[:5]:  # 只显示前5个字段
                    print(f"      - {col[1]} ({col[2]})")
                if len(columns) > 5:
                    print(f"      ... 还有 {len(columns) - 5} 个字段")
            else:
                print(f"  ❌ {table} 表不存在")
        
        # 检查用户表的新字段
        print("\n检查用户表的新字段:")
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [column[1] for column in cursor.fetchall()]
        
        new_fields = ['avatar_url', 'bio', 'mbti_type', 'friend_count', 'post_count']
        for field in new_fields:
            if field in user_columns:
                print(f"  ✅ users.{field} 字段存在")
            else:
                print(f"  ❌ users.{field} 字段不存在")
        
        # 检查测试记录表的新字段
        print("\n检查测试记录表的新字段:")
        cursor.execute("PRAGMA table_info(test_records)")
        test_columns = [column[1] for column in cursor.fetchall()]
        
        new_fields = ['share_count', 'view_count']
        for field in new_fields:
            if field in test_columns:
                print(f"  ✅ test_records.{field} 字段存在")
            else:
                print(f"  ❌ test_records.{field} 字段不存在")
        
        conn.close()
        print("\n✅ 数据库结构检查完成")
        return True
        
    except Exception as e:
        print(f"\n❌ 数据库结构检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("MBTI测试系统 - 社交API功能测试")
    print("="*60)
    
    # 先检查数据库结构
    if not test_database_structure():
        print("\n⚠️ 数据库结构不完整，请先运行数据库升级脚本")
        return False
    
    print("\n" + "="*60)
    print("开始功能测试")
    print("="*60)
    
    # 运行功能测试
    test_passed = test_all_functions()
    
    if test_passed:
        print("\n" + "="*60)
        print("🎉 所有测试通过！")
        print("社交API功能完整，可以集成到主服务器。")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("⚠️ 测试未完全通过")
        print("请检查失败的功能模块。")
        print("="*60)
    
    return test_passed

if __name__ == "__main__":
    main()