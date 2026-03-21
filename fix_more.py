import re
import os

files = [
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\knowledge\KnowledgeList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\miniclaw\FirmwareList.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\owner\OwnerProfile.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\pet\PetConsole.vue",
    r"C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\pet\PetConversations.vue",
]

for filepath in files:
    if not os.path.exists(filepath):
        print(f"NOT FOUND: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove a-layout-sider block
    content = re.sub(r'<a-layout-sider[^>]*>[\s\S]*?</a-layout-sider>', '', content)
    
    # Replace outer a-layout with div
    content = re.sub(r'<a-layout\s+class="[^"]*">\s*', '<div class="page-container">\n', content)
    
    # Remove a-layout header
    content = re.sub(r'<a-layout-header[^>]*>[\s\S]*?</a-layout-header>', '', content)
    
    # Replace <a-layout> <a-layout-content with <div>
    content = re.sub(r'<a-layout>\s*<a-layout-content\s+class="content">\s*', '<div class="page-container">\n', content)
    
    # Replace </a-layout-content></a-layout> with </div>
    content = re.sub(r'\s*</a-layout-content>\s*</a-layout>', '\n</div>', content)
    
    # Remove any remaining </a-layout>
    content = re.sub(r'</a-layout>', '', content)
    content = re.sub(r'<a-layout[^>]*>', '', content)
    
    # Remove router import and related
    if 'handleMenuClick' in content:
        content = re.sub(r"import\s+\{[^}]*\}\s+from\s+'vue-router'\s*", '', content)
        content = re.sub(r'const\s+router\s*=\s*useRouter\(\)\s*', '', content)
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
