# -*- coding: utf-8 -*-
fp = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(fp, 'rb') as f:
    raw = f.read()

text = '## \u5341\u4e00\u3001\u4f1a\u5458\u8425\u9500\u7ba1\u7406\u7cfb\u7edf'
encoded = text.encode('utf-8')
pos = raw.find(encoded)
print('Member system heading at:', pos)

ui_text = '## \u4e8c\u5341\u4e00\u3001UI\u8bbe\u8ba1\u89c4\u8303'
ui_enc = ui_text.encode('utf-8')
pos2 = raw.find(ui_enc)
print('UI chapter at:', pos2)
print('Total size:', len(raw))

if pos > 0:
    print('\nContext around member system:')
    print(raw[pos:pos+200])
    print('\nContext before:')
    print(raw[pos-200:pos])
