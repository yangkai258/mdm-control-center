# -*- coding: utf-8 -*-
import os

path = r"C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MODULE_DEVICE_SHADOW.md"

with open(path, 'rb') as f:
    raw = f.read()

# Find all '## 九' sections
target = b'## \xe4\xb9\x9d'
idx = raw.find(target)
while idx >= 0:
    line_end = raw.find(b'\n', idx)
    line = raw[idx:line_end]
    print(f'at byte {idx}: {line.decode("utf-8", errors="replace")}')
    idx = raw.find(target, idx + 1)
