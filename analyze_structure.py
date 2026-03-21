# -*- coding: utf-8 -*-
fp = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(fp, 'rb') as f:
    raw = f.read()
print('File size:', len(raw))

# Find all ## headings (UTF-8)
import re
content = raw.decode('utf-8', errors='replace')

# Find all top-level chapter headings (## followed by Chinese numeral)
for m in re.finditer(r'## ([一二三四五六七八九十零百]+[、\u3001])', content):
    end = content.find('\n', m.end())
    title = content[m.start():end].strip() if end > 0 else content[m.start():m.start()+30]
    print('Pos', m.start(), ':', repr(title[:50]))
