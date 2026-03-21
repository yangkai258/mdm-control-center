# Cleanup script: remove duplicate old placeholder content
# The current file has: header + new ch13-16 + old ch13-22+appendixes
# We want: header + new ch13-16 + old ch16-22 + appendixes

with open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md', 'rb') as f:
    content = f.read()

print(f'File size before: {len(content)}')

# Find the first occurrence of old chapter 13 heading (in the duplicate section)
old_ch13_heading = '## 十三、基础管理（档案/调度/字典等）'.encode('utf-8')
dup_old_ch13_pos = content.find(old_ch13_heading)
print(f'Duplicate old ch13 at: {dup_old_ch13_pos}')

# Find the second V1.3 footer (marks start of appendixes in old placeholder)
v1_3_positions = []
pos = 0
while True:
    pos = content.find('本文档版本 V1.3'.encode('utf-8'), pos)
    if pos == -1:
        break
    v1_3_positions.append(pos)
    pos += 1
print(f'V1.3 positions: {v1_3_positions}')

# The first V1.3 at v1_3_positions[0] is inside the old ch13 placeholder
# The second V1.3 at v1_3_positions[1] is the appendix footer
# We want to remove from dup_old_ch13_pos to v1_3_positions[1]

# The V1.3 footer at v1_3_positions[1] is followed by the actual appendix content
# Let's see what comes after it
print(f'Around second V1.3 ({v1_3_positions[1]}): {repr(content[v1_3_positions[1]:v1_3_positions[1]+100])}')

# The appendixes section starts after the V1.3 footer text
# Footer text is: *本文档版本 V1.3，编写日期 2026-03-20*
# That's about 43 bytes + trailing \r\n
footer_text = '本文档版本 V1.3，编写日期 2026-03-20*'.encode('utf-8')
appendix_start_in_old = content.find(footer_text, v1_3_positions[1])
print(f'Footer text at: {appendix_start_in_old}')
# After the footer text, there's \r\n\r\n and then the appendix content
# Actually v1_3_positions[1] is the START of '本文档版本'
appendix_content_start = appendix_start_in_old + len(footer_text)
# Skip any trailing \r\n
while appendix_content_start < len(content) and content[appendix_content_start:appendix_content_start+2] in [b'\r\n', b'\n', b'  ']:
    if content[appendix_content_start:appendix_content_start+2] == b'\r\n':
        appendix_content_start += 2
    elif content[appendix_content_start:appendix_content_start+1] == b'\n':
        appendix_content_start += 1
    else:
        break

print(f'Appendix content starts at: {appendix_content_start}')
print(f'From there: {repr(content[appendix_content_start:appendix_content_start+200])}')

# The appendix content from the old placeholder section should be KEPT
appendix_content = content[appendix_content_start:]
print(f'Appendix size: {len(appendix_content)}')

# Result: keep everything up to dup_old_ch13_pos, then add appendix_content
result = content[:dup_old_ch13_pos] + appendix_content

print(f'Result size: {len(result)}')

# Write result
with open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md', 'wb') as f:
    f.write(result)

print('Done!')
