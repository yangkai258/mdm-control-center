#!/usr/bin/env python3
"""
修复编码问题的社交API测试脚本
使用ASCII字符替代Unicode符号
"""

import sqlite3
import json
from social_api_final import SocialAPI

def print_test_result(test_name, result):
    """打印测试结果（使用ASCII字符）"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")
    
    if result.get("success"):
        print(f"[PASS] 成功: {result.get('message', '操作成功')}")
        
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
        print(f"[FAIL] 失败: {result.get('error', '未知错误')}")
    
    return result.get("success", False)

def test_database_structure():
    """测试数据库结构"""
    print("测试数据库结构...")
    
    try:
        conn = sqlite3.connect("mbti_test.db")
        cursor = conn.cursor()
        
        # 检查表
        tables = ['shares', 'friendships', 'posts', 'comments', 'likes']
        
        print("检查社交相关表:")
        
        all_tables_exist = True
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"  [OK] {table} 表存在")
            else:
                print(f"  [MISSING] {table} 表不存在")
                all_tables_exist = False
        
        conn.close()
        return all_tables_exist
    except Exception as e:
        print(f"数据库测试失败: {e}")
        return False

def test_basic_functions():
    """测试基本功能"""
    print("\n测试基本API功能...")
    
    api = SocialAPI()
    
    try:
        # 测试用户ID
        test_user_id = 1
        
        print(f"使用测试用户ID: {test_user_id}")
        
        # 1. 测试获取用户资料
        print("\n1. 测试用户资料功能:")
        result = api.get_user_profile(test_user_id)
        success1 = print_test_result("获取用户资料", result)
        
        # 2. 测试创建帖子
        print("\n2. 测试社区功能:")
        result = api.create_post(test_user_id, "测试帖子标题", "测试帖子内容", "INTJ")
        success2 = print_test_result("创建帖子", result)
        
        if success2:
            post_id = result.get("post_id")
            
            # 获取帖子列表
            result = api.get_posts(limit=3)
            success3 = print_test_result("获取帖子列表", result)
        
        # 3. 测试分享功能
        print("\n3. 测试分享功能:")
        result = api.create_share(test_user_id, 1, "wechat", "分享测试")
        success4 = print_test_result("创建分享", result)
        
        # 4. 测试统计功能
        print("\n4. 测试统计功能:")
        result = api.get_social_stats(test_user_id)
        success5 = print_test_result("获取社交统计", result)
        
        # 汇总结果
        successes = [s for s in [success1, success2, success3, success4, success5] if s is not None]
        passed = sum(1 for s in successes if s)
        total = len(successes)
        
        print(f"\n{'='*60}")
        print(f"测试结果: {passed}/{total} 个测试通过")
        
        if passed == total:
            print("[ALL PASS] 所有测试通过！")
            return True
        else:
            print(f"[PARTIAL] {total - passed} 个测试失败")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        api.close()

def main():
    """主测试函数"""
    print("MBTI社交API测试 (修复编码版)")
    print("="*60)
    
    # 先检查数据库结构
    if not test_database_structure():
        print("\n[WARNING] 数据库结构不完整，部分测试可能失败")
        print("请先运行数据库升级脚本: python upgrade_database_for_social.py")
    
    print("\n" + "="*60)
    print("开始功能测试")
    print("="*60)
    
    # 运行功能测试
    test_passed = test_basic_functions()
    
    if test_passed:
        print("\n" + "="*60)
        print("[SUCCESS] 所有测试通过！")
        print("社交API功能完整，可以集成到主服务器。")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("[WARNING] 测试未完全通过")
        print("请检查失败的功能模块。")
        print("="*60)
    
    return test_passed

if __name__ == "__main__":
    main()