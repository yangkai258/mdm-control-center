import os, re

fpath = r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue'

with open(fpath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Find all button text and wrap with 「」
def replace_button_text(m):
    text = m.group(1)
    full_tag = m.group(0)
    # Skip if already has 「」
    if '「' in text:
        return full_tag
    return full_tag.replace(text, f'「{text}」')

# Pattern: <a-button...>text</a-button>
new_content = re.sub(r'(<a-button[^>]*>)([^<]+)(</a-button>)', replace_button_text, content)

if new_content != content:
    with open(fpath, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(new_content)
    print(f'Fixed: {fpath}')
else:
    print('No changes needed')
