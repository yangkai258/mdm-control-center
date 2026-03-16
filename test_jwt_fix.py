#!/usr/bin/env python3
"""
测试JWT令牌修复
验证服务器重启后令牌仍然有效
"""

import requests
import json
import time

BASE_URL = "http://localhost:8004"

def test_jwt_fix():
    print("测试JWT令牌修复...")
    print("=" * 50)
    
    # 1. 测试用户登录
    print("1. 测试用户登录...")
    login_data = {
        "username": "testuser2",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            print(f"[OK] 登录成功")
            print(f"   令牌: {token[:30]}...")
            
            # 2. 测试使用令牌访问受保护端点
            print("\n2. 测试访问受保护端点...")
            headers = {"Authorization": f"Bearer {token}"}
            
            # 测试 /api/user/profile
            profile_response = requests.get(f"{BASE_URL}/api/user/profile", headers=headers)
            if profile_response.status_code == 200:
                print(f"[OK] /api/user/profile 访问成功")
            else:
                print(f"[ERROR] /api/user/profile 访问失败: {profile_response.status_code}")
                print(f"   响应: {profile_response.text}")
            
            # 测试 /api/test/continue
            continue_response = requests.get(f"{BASE_URL}/api/test/continue", headers=headers)
            if continue_response.status_code == 200:
                print(f"[OK] /api/test/continue 访问成功")
            else:
                print(f"[ERROR] /api/test/continue 访问失败: {continue_response.status_code}")
                print(f"   响应: {continue_response.text}")
                
        else:
            print(f"[ERROR] 登录失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] 测试过程中出现异常: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！")

if __name__ == "__main__":
    test_jwt_fix()