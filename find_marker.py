# -*- coding: utf-8 -*-
with open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md', 'rb') as f:
    original = f.read()

search = b'## \xe5\x8d\x81\xe4\xb8\x89\xe3\x80\x81\xe5\x9f\xba\xe7\xa1\x80'
idx = original.find(search)
print('Chapter 13 placeholder starts at byte:', idx)
print('File size:', len(original))
# Show 200 bytes before
context = original[idx-200:idx]
print('Context before chapter 13:')
print(context.decode('utf-8', errors='replace'))
