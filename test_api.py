#!/usr/bin/env python3
"""
MBTI测试服务器API测试脚本
用于验证服务器功能是否正常
"""

import requests
import json
import time

BASE_URL = "http://localhost:8004"

def test_api(endpoint, method="GET", data=None, token=None):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if data:
        headers["Content-Type"] = "application/json"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        else:
            print(f"❌ 不支持的HTTP方法: {method}")
            return None
        
        print(f"🔍 {method} {endpoint}")
        print(f"   状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   错误: {response.text}")
        
        try:
            return response.json()
        except:
            return response.text
        
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务器 {BASE_URL}")
        print("   请确保服务器正在运行 (python complete_server.py)")
        return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def test_server_status():
    """测试服务器状态"""
    print("\n" + "="*50)
    print("测试服务器状态")
    print("="*50)
    
    # 测试首页
    result = test_api("/")
    if result and "html" in str(result).lower():
        print("✅ 服务器首页正常")
    else:
        print("❌ 服务器首页异常")
    
    # 测试登录页面
    result = test_api("/login.html")
    if result and "html" in str(result).lower():
        print("✅ 登录页面正常")
    else:
        print("❌ 登录页面异常")

def test_user_registration():
    """测试用户注册"""
    print("\n" + "="*50)
    print("测试用户注册")
    print("="*50)
    
    # 生成唯一的用户名
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    
    register_data = {
        "username": username,
        "password": "test123",
        "nickname": f"测试用户{timestamp}",
        "gender": "男",
        "age": 25
    }
    
    result = test_api("/api/register", "POST", register_data)
    
    if result and "token" in result:
        print(f"✅ 用户注册成功: {username}")
        return result["token"], username
    else:
        print("❌ 用户注册失败")
        return None, None

def test_user_login():
    """测试用户登录"""
    print("\n" + "="*50)
    print("测试用户登录")
    print("="*50)
    
    login_data = {
        "username": "testuser",
        "password": "test123"
    }
    
    result = test_api("/api/login", "POST", login_data)
    
    if result and "token" in result:
        print("✅ 用户登录成功")
        return result["token"]
    else:
        print("❌ 用户登录失败")
        return None

def test_protected_apis(token):
    """测试需要认证的API"""
    print("\n" + "="*50)
    print("测试需要认证的API")
    print("="*50)
    
    if not token:
        print("❌ 没有有效的token，跳过认证API测试")
        return
    
    # 测试获取用户资料
    result = test_api("/api/user/profile", "GET", token=token)
    if result and "username" in result:
        print("✅ 获取用户资料成功")
    else:
        print("❌ 获取用户资料失败")
    
    # 测试获取测试说明
    result = test_api("/api/test/instructions", "GET", token=token)
    if result and "title" in result:
        print("✅ 获取测试说明成功")
    else:
        print("❌ 获取测试说明失败")
    
    # 测试获取题目
    result = test_api("/api/test/questions", "GET", token=token)
    if result and "questions" in result:
        print(f"✅ 获取题目成功，共 {result['total']} 题")
        return result["questions"]
    else:
        print("❌ 获取题目失败")
        return None

def test_test_flow(token, questions):
    """测试完整的测试流程"""
    print("\n" + "="*50)
    print("测试完整的测试流程")
    print("="*50)
    
    if not token or not questions:
        print("❌ 缺少token或题目，跳过测试流程")
        return
    
    # 开始测试
    result = test_api("/api/test/start", "POST", {}, token)
    if result and "test_id" in result:
        print("✅ 开始测试成功")
        record_id = result["record_id"]
    else:
        print("❌ 开始测试失败")
        return
    
    # 模拟回答所有题目
    answers = {}
    for i, question in enumerate(questions[:3]):  # 只测试前3题
        question_id = question["id"]
        # 选择第一个选项
        answer = question["options"][0]["text"]
        answers[question_id] = answer
        print(f"   已回答第{i+1}题: {answer[:20]}...")
    
    # 提交测试
    submit_data = {
        "record_id": record_id,
        "answers": answers
    }
    
    result = test_api("/api/test/submit", "POST", submit_data, token)
    if result and "mbti_type" in result:
        print(f"✅ 提交测试成功，MBTI类型: {result['mbti_type']}")
        print(f"   分析: {result['analysis']['description'][:50]}...")
    else:
        print("❌ 提交测试失败")

def test_history_and_analysis(token):
    """测试历史记录和分析"""
    print("\n" + "="*50)
    print("测试历史记录和分析")
    print("="*50)
    
    if not token:
        print("❌ 没有有效的token，跳过历史记录测试")
        return
    
    # 测试获取历史记录
    result = test_api("/api/test/history", "GET", token=token)
    if result and "records" in result:
        records = result["records"]
        print(f"✅ 获取历史记录成功，共 {len(records)} 条记录")
        
        # 如果有完成的测试，测试分析报告
        completed_records = [r for r in records if r["status"] == "completed"]
        if completed_records:
            record_id = completed_records[0]["id"]
            result = test_api(f"/api/test/analysis?record_id={record_id}", "GET", token=token)
            if result and "mbti_type" in result:
                print(f"✅ 获取分析报告成功，类型: {result['mbti_type']}")
            else:
                print("❌ 获取分析报告失败")
    else:
        print("❌ 获取历史记录失败")

def main():
    """主测试函数"""
    print("🚀 MBTI测试服务器API测试")
    print(f"目标服务器: {BASE_URL}")
    print()
    
    # 测试服务器状态
    test_server_status()
    
    # 测试用户注册
    token, username = test_user_registration()
    
    # 如果注册失败，尝试登录测试用户
    if not token:
        print("\n⚠️  尝试使用测试用户登录...")
        token = test_user_login()
    
    if token:
        # 测试需要认证的API
        questions = test_protected_apis(token)
        
        # 测试完整的测试流程
        test_test_flow(token, questions)
        
        # 测试历史记录和分析
        test_history_and_analysis(token)
        
        print("\n" + "="*50)
        print("测试总结")
        print("="*50)
        print(f"✅ 测试用户: {username or 'testuser'}")
        print(f"✅ Token: {token[:20]}...")
        print("✅ 所有测试完成！")
    else:
        print("\n" + "="*50)
        print("测试总结")
        print("="*50)
        print("❌ 认证失败，部分测试未完成")
        print("💡 建议:")
        print("   1. 确保服务器正在运行")
        print("   2. 检查服务器端口 (8004)")
        print("   3. 尝试手动注册用户")

if __name__ == "__main__":
    main()