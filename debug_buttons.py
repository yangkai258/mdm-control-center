import re
f = open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue', 'r', encoding='utf-8-sig')
content = f.read()
f.close()

# Find actual button patterns
buttons = re.findall(r'<a-button[^>]*>([^<]+)</a-button>', content)
for b in buttons:
    print(f'Found button text: {repr(b)}')
    # Check if the pattern exists
    pattern = f'">{b}</a-button>'
    print(f'  Pattern {repr(pattern)}: {pattern in content}')
