import os, re

base = r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views'

# Get button texts from actual file content
fpath = os.path.join(base, 'DeviceDashboard.vue')
with open(fpath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Find all button texts
buttons = re.findall(r'<a-button[^>]*>([^<]+)</a-button>', content)
print('Current button texts:')
for b in set(buttons):
    # Get the hex of each char
    hex_str = ' '.join(f'{ord(c):04x}' for c in b)
    print(f'  {repr(b)} -> {hex_str}')
