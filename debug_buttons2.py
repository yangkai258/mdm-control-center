import re
f = open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue', 'r', encoding='utf-8-sig')
content = f.read()
f.close()

# Find all button patterns with their context
buttons = re.findall(r'<a-button[^>]*>.*?</a-button>', content, re.DOTALL)
for b in buttons:
    print(repr(b[:100]))
    print()
