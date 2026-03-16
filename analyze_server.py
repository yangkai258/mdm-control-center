#!/usr/bin/env python3
"""
分析服务器结构，为集成社交API做准备
"""

import re

def analyze_server_structure():
    """分析服务器代码结构"""
    with open('complete_server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("分析MBTI测试服务器结构...")
    print("="*60)
    
    # 查找类定义
    class_pattern = r'class (\w+)'
    classes = re.findall(class_pattern, content)
    print(f"找到 {len(classes)} 个类: {classes}")
    
    # 查找函数定义
    function_pattern = r'def (\w+)\('
    functions = re.findall(function_pattern, content)
    print(f"\n找到 {len(functions)} 个函数")
    
    # 按类别分组
    api_functions = [f for f in functions if f.startswith('handle_')]
    helper_functions = [f for f in functions if not f.startswith('handle_') and f not in ['__init__', 'do_GET', 'do_POST']]
    
    print(f"\nAPI处理函数 ({len(api_functions)}个):")
    for func in sorted(api_functions):
        print(f"  - {func}")
    
    print(f"\n辅助函数 ({len(helper_functions)}个):")
    for func in sorted(helper_functions)[:10]:  # 只显示前10个
        print(f"  - {func}")
    if len(helper_functions) > 10:
        print(f"  ... 还有 {len(helper_functions) - 10} 个")
    
    # 查找API路由
    route_pattern = r'if path == "([^"]+)"'
    routes = re.findall(route_pattern, content)
    
    print(f"\nAPI路由端点 ({len(routes)}个):")
    for route in sorted(routes):
        print(f"  - /{route}")
    
    # 查找数据库相关代码
    db_pattern = r'(?:sqlite3|cursor|execute|fetch)'
    db_lines = [line.strip() for line in content.split('\n') if re.search(db_pattern, line, re.IGNORECASE)]
    
    print(f"\n数据库操作示例 (前5个):")
    for line in db_lines[:5]:
        print(f"  {line[:100]}...")
    
    # 分析JWT和认证相关代码
    jwt_pattern = r'(?:jwt|token|auth|login|register)'
    jwt_lines = [line.strip() for line in content.split('\n') if re.search(jwt_pattern, line, re.IGNORECASE)]
    
    print(f"\n认证相关代码示例 (前5个):")
    for line in jwt_lines[:5]:
        print(f"  {line[:100]}...")
    
    print("\n" + "="*60)
    print("集成建议:")
    print("1. 社交API需要添加新的路由端点")
    print("2. 需要集成JWT认证机制")
    print("3. 数据库连接可以复用现有连接")
    print("4. 错误处理需要保持一致性")
    
    return {
        'classes': classes,
        'api_functions': api_functions,
        'routes': routes,
        'db_operations': len(db_lines),
        'auth_operations': len(jwt_lines)
    }

if __name__ == "__main__":
    analyze_server_structure()