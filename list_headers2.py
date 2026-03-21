with open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md', 'rb') as f:
    content = f.read()
import re
headers = re.findall(b'#{1,2} [^\\n]+', content)
for i, h in enumerate(headers):
    if i >= 340:
        try:
            print(str(i) + ': ' + h.decode('utf-8'))
        except:
            print(str(i) + ': BIN')
