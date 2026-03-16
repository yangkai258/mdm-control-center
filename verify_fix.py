#!/usr/bin/env python3
"""
验证题目数量显示修复
"""

import re

def verify_fix():
    print("验证题目数量显示修复...")
    print("=" * 50)
    
    with open('test.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查修复点
    checks = [
        ("测试说明中的题目数量", r"题目数量.*?(\d+)道"),
        ("测试说明中的描述", r"通过(\d+)道精心设计的题目"),
        ("进度显示", r"第1题 / 共(\d+)题"),
        ("预计时间", r"预计时间.*?(\d+-\d+)分钟"),
    ]
    
    all_passed = True
    for check_name, pattern in checks:
        match = re.search(pattern, content)
        if match:
            value = match.group(1)
            if '100' in value or '25' in value or '15-25' in value:
                print(f"[OK] {check_name}: {value}")
            else:
                print(f"[ERROR] {check_name}: 找到 '{value}'，但期望包含100或15-25")
                all_passed = False
        else:
            print(f"[ERROR] {check_name}: 未找到匹配")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[OK] 所有修复验证通过！")
    else:
        print("[ERROR] 部分修复未通过验证")
    
    return all_passed

if __name__ == "__main__":
    verify_fix()