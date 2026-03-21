# Fixed replacement script
import os

# Read all content parts
parts = []
for fname in ['new_ch13_a.txt', 'new_ch13_b.txt', 'new_ch14.txt', 'new_ch15.txt', 'new_ch16.txt']:
    fpath = r'C:\Users\YKing\.openclaw\workspace\\' + fname
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            parts.append(f.read())
        print(f'Loaded {fname}: {len(parts[-1])} chars')

new_content = '\n'.join(parts)
print(f'Total new content: {len(new_content)} chars')

# Read original file
orig_path = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(orig_path, 'rb') as f:
    original = f.read()

# The file uses CRLF line endings
CRLF = b'---\r\n'

# Find chapter 13 placeholder start
ch13_search = '## 十三、基础管理'.encode('utf-8')
ch13_idx = original.find(ch13_search)
print(f'Chapter 13 placeholder at byte: {ch13_idx}')

# Find V1.3 footer text
footer_search = '本文档版本 V1.3'.encode('utf-8')
footer_idx = original.find(footer_search)
print(f'V1.3 footer text at byte: {footer_idx}')

# The --- that starts the V1.3 footer block is BEFORE the footer text
# But the --- we want to keep (before new content) is the one that comes AFTER the footer
# Find the --- that is after the footer text
# Footer text ends approximately at footer_idx + len('本文档版本 V1.3，编写日期 2026-03-20*')
# Let's find the first --- that is AFTER the footer_idx
sep_after_footer = original.find(CRLF, footer_idx)
print(f'--- after footer at: {sep_after_footer}')

# The separator to keep is the one that starts the V1.3 block (before footer)
# But we want to keep content up to AND INCLUDING this separator
# So we keep original[:sep_before_footer_start + len(CRLF)]
# where sep_before_footer is the --- before the footer text
sep_before_footer = original.rfind(CRLF, 0, footer_idx)
print(f'--- before footer at: {sep_before_footer}')

# sep_before_footer is the START of the --- that begins the V1.3 block
# The --- itself is 5 bytes: '---\r\n'
# So we want to keep original[:sep_before_footer] (NOT including the ---)
# Then add new content
# Then add original from ch13_idx onwards (old placeholder, to be replaced)

# But actually: we want to REPLACE the entire V1.3 block (including its leading ---)
# with new content. So we need:
# original[:sep_before_footer] + new_content + original[ch13_idx:]

# sep_before_footer is the START of the '---' that precedes the footer
# The footer block structure is:
# [sep_before_footer] ---  (4 CRLF)  *V1.3 footer*  (4 CRLF)  ## 十三、基础管理
# We want to keep up to sep_before_footer (NOT including the ---),
# but we could also keep the --- as a section separator. Let's keep it.

# Actually looking at the byte layout:
# sep_before_footer = 79432 (start of '---' before footer)
# The '---' at 79432 is the START of the V1.3 footer section
# We want to keep this '---' as the section separator before our new chapters

# So:
# result = original[:sep_before_footer] + '\n' + new_content + original[ch13_idx:]
# Where sep_before_footer = 79432

# Wait, but original[:79432] includes the '---' at 79432? No, original[:79432] 
# is everything UP TO but NOT INCLUDING byte 79432.
# The '---' starts at 79432, so original[:79432] ends at 79431 (before the ---)

# We want to KEEP the '---' at 79432 as the section separator before new content.
# So we should do: original[:sep_before_footer + len(CRLF)] + new_content + original[ch13_idx:]
# = original[:79432 + 5] = original[:79437] (includes the '---' and its CRLF)

result = original[:sep_before_footer + len(CRLF)] + new_content.encode('utf-8') + original[ch13_idx:]

# Write result
out_path = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(out_path, 'wb') as f:
    f.write(result)

print(f'Done! Written {len(result)} bytes to output file')
print(f'Expected size: {sep_before_footer + len(CRLF)} + {len(new_content)} + {len(original) - ch13_idx} = {sep_before_footer + len(CRLF) + len(new_content) + len(original) - ch13_idx}')
