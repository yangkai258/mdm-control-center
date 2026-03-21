import re
import os

files = [
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertRules.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertSettings.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppDistributions.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppVersions.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\members\MemberCoupons.vue",
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
    
    # Replace orphaned </a-layout> with </div>
    content = re.sub(r'\s*</a-layout>\s*</template>', '\n  </div>\n</template>', content)
    
    # Also fix any remaining </a-layout> before </template>
    content = re.sub(r'</a-layout>\s*</template>', '</div>\n</template>', content)
    
    # Remove any <a-layout> or </a-layout> tags that might be left
    content = re.sub(r'</a-layout>', '', content)
    content = re.sub(r'<a-layout[^>]*>', '', content)
    
    # Clean up multiple empty lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED: {os.path.basename(filepath)}")
    else:
        print(f"NO CHANGE: {os.path.basename(filepath)}")

print("\nDone!")
