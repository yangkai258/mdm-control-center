import re
f = open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue', 'rb')
raw = f.read()
f.close()
# Find buttons
buttons = re.findall(b'<a-button[^>]*>([^<]+)</a-button>', raw)
print('Button contents:')
for btn in buttons:
    print(f'  Bytes: {btn}')
    try:
        print(f'  UTF-8: {btn.decode("utf-8")}')
    except:
        print(f'  UTF-8: <decode error>')
    try:
        print(f'  GBK: {btn.decode("gbk")}')
    except:
        print(f'  GBK: <decode error>')
    print()
