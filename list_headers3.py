with open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md', 'rb') as f:
    content = f.read()
import re
headers = re.findall(b'#{1,2} [^\\n]+', content)
print('Total headers:', len(headers))
# Print last 10
for i, h in enumerate(headers[-10:]):
    idx = len(headers) - 10 + i
    try:
        print(str(idx) + ': ' + h.decode('utf-8'))
    except:
        print(str(idx) + ': BIN')
# Check for appendix
for i, h in enumerate(headers):
    try:
        if '附录' in h.decode('utf-8') or 'API' in h.decode('utf-8') or '非功能性' in h.decode('utf-8') or '数据库' in h.decode('utf-8'):
            print('Found at', i, ':', h.decode('utf-8'))
    except:
        pass
# Check last 200 bytes of file
print('Last 200 bytes:', repr(content[-200:]))
