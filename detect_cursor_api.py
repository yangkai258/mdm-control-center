#!/usr/bin/env python3
"""
探测Cursor的AI API端点
"""

import requests
import json
import time
from typing import Optional, Dict, Any

def test_endpoint(url: str, method: str = "POST", data: Optional[Dict] = None, headers: Optional[Dict] = None) -> bool:
    """测试API端点"""
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        else:
            response = requests.get(url, headers=headers, timeout=5)
        
        print(f"  {url}: {response.status_code}")
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"    Success! Response keys: {list(result.keys())[:5]}")
                return True
            except:
                print(f"    Success! (Non-JSON response)")
                return True
        elif response.status_code in [401, 403]:
            print(f"    Authentication required")
            return True  # 端点存在，只是需要认证
        return False
    except requests.exceptions.RequestException as e:
        print(f"  {url}: Error - {type(e).__name__}")
        return False

def main():
    print("开始探测Cursor AI API端点...")
    print("="*60)
    
    # Cursor可能使用的端口
    ports = [3000, 3001, 8080, 8081, 8000, 8001, 9000, 9001]
    
    # 可能的API路径
    api_paths = [
        "/api/ai/chat",
        "/api/chat",
        "/v1/chat/completions",
        "/api/completions",
        "/api/generate",
        "/chat",
        "/api/v1/chat/completions",
        "/api/ai/completions"
    ]
    
    # 测试数据
    test_data = {
        "messages": [{"role": "user", "content": "Hello"}],
        "model": "gpt-4",
        "stream": False
    }
    
    found_endpoints = []
    
    for port in ports:
        base_url = f"http://localhost:{port}"
        
        print(f"\n测试端口 {port}:")
        
        # 先测试根路径
        try:
            response = requests.get(base_url, timeout=3)
            if response.status_code < 500:  # 不是服务器错误
                print(f"  {base_url}/: {response.status_code}")
        except:
            pass
        
        # 测试各个API路径
        for path in api_paths:
            url = base_url + path
            if test_endpoint(url, data=test_data):
                found_endpoints.append(url)
    
    print("\n" + "="*60)
    print("探测结果:")
    
    if found_endpoints:
        print(f"✅ 找到 {len(found_endpoints)} 个可能的API端点:")
        for endpoint in found_endpoints:
            print(f"  - {endpoint}")
        
        # 测试OpenAI兼容性
        print("\n测试OpenAI兼容性:")
        for endpoint in found_endpoints[:2]:  # 只测试前两个
            print(f"\n测试 {endpoint}:")
            
            # 测试/models端点
            models_url = endpoint.replace("/chat/completions", "/models").replace("/chat", "/models").replace("/completions", "/models")
            if test_endpoint(models_url, method="GET"):
                print(f"  ✅ 支持OpenAI兼容的/models端点")
            
            # 测试完整请求
            response = requests.post(endpoint, json=test_data, timeout=5)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "choices" in result:
                        print(f"  ✅ OpenAI兼容格式: 有choices字段")
                        print(f"     回复: {result['choices'][0]['message']['content'][:100]}...")
                except:
                    pass
    else:
        print("❌ 未找到可用的API端点")
        
        # 建议手动检查
        print("\n建议手动检查:")
        print("1. 打开Cursor")
        print("2. 按 Ctrl+Shift+I 打开开发者工具")
        print("3. 切换到Network标签")
        print("4. 在Cursor中问一个问题")
        print("5. 查看请求的URL")
    
    print("\n" + "="*60)
    
    # 检查Cursor的配置文件位置
    print("\n检查Cursor配置文件:")
    import os
    
    config_paths = [
        os.path.expanduser("~/.cursor/config.json"),
        os.path.expanduser("~/AppData/Roaming/Cursor/config.json"),
        os.path.expanduser("~/AppData/Local/Cursor/config.json"),
        os.path.expanduser("~/Library/Application Support/Cursor/config.json")
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            print(f"✅ 找到配置文件: {path}")
            try:
                with open(path, 'r') as f:
                    config = json.load(f)
                    print(f"   配置内容: {json.dumps(config, indent=2)[:200]}...")
            except:
                print(f"   无法读取配置文件")
        else:
            print(f"  {path}: 不存在")

if __name__ == "__main__":
    main()