import re
import os
from pathlib import Path

files_to_fix = [
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertRules.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertSettings.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppDistributions.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppVersions.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\members\MemberCoupons.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\members\MemberPoints.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\members\MemberPromotions.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\policies\ComplianceRules.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\policies\PolicyConfigs.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\policies\PolicyList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\DeviceDashboard.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\DeviceDetail.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\DeviceStatus.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\OtaFirmware.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\PetConfig.vue",
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"NOT FOUND: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Skip if no a-layout-sider
    if 'a-layout-sider' not in content:
        print(f"SKIP (no sider): {os.path.basename(filepath)}")
        continue
    
    # Remove a-layout-sider block completely (from <a-layout-sider to </a-layout-sider>)
    content = re.sub(r'<a-layout-sider[^>]*>[\s\S]*?</a-layout-sider>', '', content)
    
    # Replace outer a-layout with a div wrapper
    # Match: <a-layout class="xxx"> content </a-layout>
    content = re.sub(
        r'<a-layout\s+class="[^"]*">\s*',
        '<div class="page-container">\n',
        content
    )
    
    # Remove a-layout header if exists (between layout and content)
    content = re.sub(r'<a-layout-header[^>]*>[\s\S]*?</a-layout-header>', '', content)
    
    # Replace <a-layout> <a-layout-content class="content"> with <div>
    content = re.sub(
        r'<a-layout>\s*<a-layout-content\s+class="content">\s*',
        '<div class="page-container">\n',
        content
    )
    
    # Replace </a-layout-content></a-layout> with </div>
    content = re.sub(
        r'\s*</a-layout-content>\s*</a-layout>',
        '\n</div>',
        content
    )
    
    # Remove empty a-layout tags
    content = re.sub(r'<a-layout>\s*</a-layout>', '', content)
    content = re.sub(r'<a-layout\s+class="[^"]*">\s*</a-layout>', '', content)
    
    # Remove router import and related if present
    if 'handleMenuClick' in content and 'router' in content:
        content = re.sub(r"import\s+\{[^}]*\}\s+from\s+'vue-router'\s*", '', content)
        content = re.sub(r'const\s+router\s*=\s*useRouter\(\)\s*', '', content)
    
    # Remove selectedKeys and collapsed refs (used by menu)
    content = re.sub(r"const\s+selectedKeys\s*=\s*ref\([^)]*\)\s*", '', content)
    content = re.sub(r"const\s+collapsed\s*=\s*ref\([^)]*\)\s*", '', content)
    content = re.sub(r"const\s+handleMenuClick\s*=\s*\([^)]*\)\s*=>\s*\{[\s\S]*?\}\s*", '', content)
    
    # Clean up multiple empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {os.path.basename(filepath)}")
    else:
        print(f"NO CHANGE: {os.path.basename(filepath)}")

print("\nDone!")
