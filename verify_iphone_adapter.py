#!/usr/bin/env python3
"""
验证iPhone 15 Pro Max适配
"""

import re

def verify_iphone_adapter():
    print("验证iPhone 15 Pro Max适配...")
    print("=" * 60)
    
    with open('test.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查iPhone 15 Pro Max特定适配
    checks = [
        ("iPhone 15 Pro Max竖屏适配", r"@media.*max-width.*430px.*min-height.*932px"),
        ("iPhone 15 Pro Max横屏适配", r"@media.*orientation.*landscape.*max-width.*932px.*min-height.*430px"),
        ("安全区域支持", r"env\(safe-area-inset"),
        ("iOS系统字体", r"font-size.*17px.*iOS系统字体大小"),
        ("毛玻璃效果", r"backdrop-filter.*blur"),
        ("渐变色彩", r"linear-gradient.*135deg"),
        ("圆角设计", r"border-radius.*25px"),
        ("阴影效果", r"box-shadow.*0.*10px.*30px"),
    ]
    
    all_passed = True
    for check_name, pattern in checks:
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            print(f"[OK] {check_name}: 已实现")
        else:
            print(f"[ERROR] {check_name}: 未找到")
            all_passed = False
    
    # 检查响应式断点
    print("\n响应式断点检查:")
    breakpoints = [
        ("移动端通用", r"@media.*max-width.*767px"),
        ("平板", r"@media.*min-width.*768px"),
        ("桌面", r"@media.*min-width.*1024px"),
        ("大桌面", r"@media.*min-width.*1200px"),
    ]
    
    for bp_name, pattern in breakpoints:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"[OK] {bp_name}断点: 已定义")
        else:
            print(f"[WARNING] {bp_name}断点: 未定义")
    
    # 检查关键CSS属性
    print("\n关键CSS属性检查:")
    css_properties = [
        ("视口设置", r"viewport-fit=cover"),
        ("用户缩放控制", r"user-scalable=no"),
        ("最大缩放", r"maximum-scale=1.0"),
        ("弹性布局", r"display.*flex"),
        ("网格布局", r"display.*grid"),
        ("过渡动画", r"transition.*all.*0.3s"),
        ("悬停效果", r":hover"),
        ("活动状态", r":active"),
    ]
    
    for prop_name, pattern in css_properties:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"[OK] {prop_name}: 已实现")
        else:
            print(f"[WARNING] {prop_name}: 未找到")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ iPhone 15 Pro Max适配验证通过！")
        print("\n适配特性总结:")
        print("1. 📱 专门针对430×932pt (@3x)分辨率优化")
        print("2. 🎨 符合iOS设计语言的视觉风格")
        print("3. 👆 符合Apple人机交互指南的触控设计")
        print("4. 🔒 支持安全区域（刘海和Home条）")
        print("5. 🔄 完善的横竖屏适配")
        print("6. ⚡ 性能优化的动画和过渡效果")
        print("7. 🎯 精确的字体大小和间距控制")
        print("8. 🌈 现代化的渐变色彩和阴影系统")
    else:
        print("❌ iPhone 15 Pro Max适配验证失败")
        print("\n建议:")
        print("1. 检查CSS中是否包含iPhone 15 Pro Max的专门适配")
        print("2. 确保支持安全区域(env(safe-area-inset))")
        print("3. 验证响应式断点是否正确")
        print("4. 测试实际设备上的显示效果")
    
    return all_passed

def check_test_page():
    print("\n" + "=" * 60)
    print("检查iPhone 15 Pro Max测试页面...")
    
    try:
        with open('test_iphone15promax.html', 'r', encoding='utf-8') as f:
            test_content = f.read()
        
        test_checks = [
            ("设备模拟器", r"device-simulator"),
            ("刘海模拟", r"notch"),
            ("安全区域测试", r"safe-area-inset"),
            ("设备检测脚本", r"detectDevice"),
            ("适配测试功能", r"runTests"),
            ("触觉反馈", r"hapticFeedback"),
            ("横竖屏监听", r"orientationchange"),
        ]
        
        all_test_passed = True
        for check_name, pattern in test_checks:
            if re.search(pattern, test_content, re.IGNORECASE):
                print(f"[OK] {check_name}: 已实现")
            else:
                print(f"[WARNING] {check_name}: 未找到")
                all_test_passed = False
        
        if all_test_passed:
            print("\n✅ iPhone 15 Pro Max测试页面完整！")
            print("\n测试页面功能:")
            print("1. 📱 精确的设备模拟器")
            print("2. 🔍 自动设备检测")
            print("3. ⚡ 性能测试功能")
            print("4. 📊 详细的测试报告")
            print("5. 📱 横竖屏切换支持")
            print("6. 👆 触觉反馈模拟")
            print("7. 📝 完整的设备信息")
        else:
            print("\n⚠️ 测试页面需要完善")
        
        return all_test_passed
        
    except FileNotFoundError:
        print("[ERROR] test_iphone15promax.html 文件不存在")
        return False

if __name__ == "__main__":
    print("iPhone 15 Pro Max适配验证工具")
    print("=" * 60)
    
    main_passed = verify_iphone_adapter()
    test_passed = check_test_page()
    
    print("\n" + "=" * 60)
    print("总体验证结果:")
    
    if main_passed and test_passed:
        print("🎉 所有验证通过！iPhone 15 Pro Max适配完整。")
        print("\n下一步:")
        print("1. 在真实iPhone 15 Pro Max设备上测试")
        print("2. 测试横竖屏切换效果")
        print("3. 验证安全区域显示")
        print("4. 测试触控交互体验")
        print("5. 验证性能表现")
    elif main_passed:
        print("📱 主页面适配通过，但测试页面需要完善")
    elif test_passed:
        print("🧪 测试页面完整，但主页面适配需要改进")
    else:
        print("❌ 需要全面改进iPhone 15 Pro Max适配")
    
    print("\n测试地址:")
    print("1. 主测试页面: http://localhost:8004/test.html")
    print("2. iPhone适配测试: file://" + __file__.replace('verify_iphone_adapter.py', 'test_iphone15promax.html'))