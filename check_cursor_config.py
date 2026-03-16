#!/usr/bin/env python3
"""
检查Cursor配置
"""

import os
import json

print("检查Cursor配置...")

# 检查Local State文件
local_state_path = r"C:\Users\YKing\AppData\Roaming\Cursor\Local State"
if os.path.exists(local_state_path):
    print(f"\n检查: {local_state_path}")
    try:
        with open(local_state_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找可能的API配置
            import re
            patterns = [
                r'api[_-]?key["\']?\s*:\s*["\'][^"\']+["\']',
                r'openai["\']?\s*:\s*{[^}]+}',
                r'gpt["\']?\s*:\s*{[^}]+}',
                r'token["\']?\s*:\s*["\'][^"\']+["\']'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"找到匹配 ({pattern}):")
                    for match in matches[:3]:  # 只显示前3个
                        print(f"  {match[:100]}...")
    except Exception as e:
        print(f"读取错误: {e}")

# 检查其他可能的位置
config_paths = [
    r"C:\Users\YKing\.cursor\config.json",
    r"C:\Users\YKing\AppData\Roaming\Cursor\User\globalStorage\storage.json",
    r"C:\Users\YKing\AppData\Roaming\Cursor\User\settings.json"
]

for path in config_paths:
    if os.path.exists(path):
        print(f"\n检查: {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 打印AI相关配置
                ai_keys = ['ai', 'openai', 'gpt', 'api', 'model', 'provider']
                for key in ai_keys:
                    if key in str(data):
                        print(f"  包含 '{key}' 配置")
        except:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if any(key in content.lower() for key in ai_keys):
                        print(f"  包含AI相关配置")
            except:
                print(f"  无法读取")

print("\n=== 建议 ===")
print("1. Cursor通常不提供本地API供外部调用")
print("2. Cursor可能使用:")
print("   - OpenAI API (需要你自己的API密钥)")
print("   - Cursor自己的云服务")
print("   - 其他AI提供商")
print("\n3. 你可以:")
print("   a) 在Cursor设置中查看AI配置")
print("   b) 使用相同的API密钥配置OpenClaw")
print("   c) 考虑其他AI提供商")

print("\n=== 立即行动 ===")
print("打开Cursor，然后:")
print("1. 点击左下角设置图标")
print("2. 查看AI/Model设置")
print("3. 看看使用的是什么AI服务")
print("4. 如果有API密钥，可以在OpenClaw中使用同样的密钥")