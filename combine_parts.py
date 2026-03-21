# -*- coding: utf-8 -*-
import os

filepath = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'

# Read current file
with open(filepath, 'r', encoding='utf-8') as f:
    current = f.read()

print(f'Current file size: {len(current)} chars')

# Find where section 11 starts in current file (should NOT exist in new content)
# Section 11 was NOT in the old document structure (old had 8 chapters)
# So we need to find the last valid content from my new sections
# The new content ends at section 10.4.3 (限制用户管理 API)
# Let's find the last valid section marker

# Search for the end of 10.4.3 - the last API in section 10
end_markers = [
    '删除限制用户',  # 10.4.3 last API
    '## 十一、流程管理',  # section 11 start
]

# Find the earliest of these markers - that's where new content ends
positions = {}
for marker in end_markers:
    pos = current.find(marker)
    if pos >= 0:
        positions[marker] = pos
        print(f'Found "{marker}" at {pos}')

# Find the end of the current valid content
# The file should end somewhere in section 10 or early 11
# If section 11 is not found, the file has old corrupted content
# Let's find the last good section ending

# Find the last occurrence of a section 10.x heading
import re
# Find all section markers like "## 10.x"
section_pattern = r'## 10\.\d+'
matches = list(re.finditer(section_pattern, current))
if matches:
    last_10 = matches[-1]
    print(f'Last section 10.x at: {last_10.start()}, text: {current[last_10.start():last_10.start()+50]}')

# Find where the old corrupted content starts (look for section numbers >= 12)
old_markers = ['## 12.', '12.5.1.6', '## 十三', '## 十四', '13.', '## 十八', '## 十九', '## 二十']
for marker in old_markers:
    pos = current.find(marker)
    if pos >= 0:
        print(f'Old marker "{marker}" found at {pos}')
