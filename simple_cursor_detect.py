#!/usr/bin/env python3
"""
简单探测Cursor API
"""

import requests
import json

print("简单探测Cursor API...")

# 常见端口
ports = [3000, 3001, 8080, 8000]

for port in ports:
    print(f"\n=== 测试端口 {port} ===")
    
    # 测试根路径
    try:
        r = requests.get(f"http://localhost:{port}", timeout=2)
        print(f"GET /: {r.status_code}")
    except:
        print(f"GET /: 无法连接")
        continue
    
    # 测试常见API路径
    paths = [
        "/api/chat",
        "/v1/chat/completions",
        "/api/ai/chat"
    ]
    
    test_data = {"messages": [{"role": "user", "content": "hi"}]}
    
    for path in paths:
        try:
            r = requests.post(f"http://localhost:{port}{path}", 
                            json=test_data, timeout=3)
            print(f"POST {path}: {r.status_code}")
            if r.status_code == 200:
                print(f"  成功! 尝试解析响应...")
                try:
                    data = r.json()
                    print(f"  响应: {json.dumps(data)[:100]}...")
                except:
                    print(f"  响应不是JSON")
        except Exception as e:
            print(f"POST {path}: 错误 - {e}")

print("\n=== 检查进程 ===")
import subprocess
result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Cursor.exe"], 
                       capture_output=True, text=True)
print(result.stdout[:500])

print("\n建议:")
print("1. 打开Cursor，按Ctrl+Shift+I看Network请求")
print("2. 检查Cursor设置里的AI配置")
print("3. 查看 ~/.cursor/ 或 AppData/Roaming/Cursor/ 下的配置文件")