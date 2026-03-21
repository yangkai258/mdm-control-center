import re
f = open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue', 'r', encoding='utf-8-sig')
content = f.read()
f.close()
# Find button elements
buttons = re.findall(r'<a-button[^>]*>[^<]+</a-button>', content)
for b in buttons[:5]:
    print(repr(b[:80]))
print()
# Check patterns
old = '>新建</a-button>'
new = '>「新建」</a-button>'
print(f'Old pattern in content: {old in content}')
print(f'New pattern in content: {new in content}')
