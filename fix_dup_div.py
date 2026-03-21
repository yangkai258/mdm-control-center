import re
import os

files = [
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertRules.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertSettings.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppDistributions.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppVersions.vue",
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

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix duplicate divs: <div class="page-container">\n<div class="page-container">
    content = re.sub(
        r'<div class="page-container">\s*<div class="page-container">',
        '<div class="page-container">',
        content
    )
    
    # Also fix with different whitespace
    content = re.sub(
        r'<div class="page-container">\n\s*<div class="page-container">',
        '<div class="page-container">',
        content
    )
    
    # Remove empty page-container divs
    content = re.sub(r'<div class="page-container">\s*</div>', '', content)
    
    # Clean up multiple empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {os.path.basename(filepath)}")
    else:
        print(f"NO CHANGE: {os.path.basename(filepath)}")

print("\nDone!")
