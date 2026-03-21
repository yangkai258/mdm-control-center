# Final replacement script - combines all parts and does the file replacement
# This script reads the generated content files and replaces the placeholder in the original

import os

# Read all content parts
parts = []
for fname in ['new_ch13_a.txt', 'new_ch13_b.txt', 'new_ch14.txt', 'new_ch15.txt', 'new_ch16.txt']:
    fpath = r'C:\Users\YKing\.openclaw\workspace\\' + fname
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            parts.append(f.read())
        print(f'Loaded {fname}: {len(parts[-1])} chars')
    else:
        print(f'Missing: {fname}')

new_content = '\n'.join(parts)
print(f'Total new content: {len(new_content)} chars')

# Read original file
orig_path = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(orig_path, 'rb') as f:
    original = f.read()

# Find chapter 13 placeholder start (## 十三、基础管理)
search = '## 十三、基础管理'.encode('utf-8')
idx = original.find(search)
print(f'Chapter 13 placeholder at byte: {idx}')

# Find the separator before it (the --- that precedes the V1.3 footer block)
# We want to keep: original up to (and including) the --- that starts the V1.3 footer
# Then add new content
# Then continue with original from chapter 13 onwards
# The V1.3 footer block is: ---  *本文档版本 V1.3...*  ---  ## 十三、基础管理
# We want to keep the first --- (start of footer) but replace everything from the footer text onwards

# Find the --- right before the V1.3 footer text
footer_text = '本文档版本 V1.3'.encode('utf-8')
footer_idx = original.find(footer_text)
print(f'V1.3 footer text at byte: {footer_idx}')

# Find the --- before the footer text
sep_before_footer = original.rfind('---\n'.encode('utf-8'), 0, footer_idx)
print(f'Separator before footer at: {sep_before_footer}')

# New structure:
# original[:sep_before_footer] = up to the --- before V1.3 footer
# new_content = expanded chapters
# original[idx:] = original chapter 13 onwards (placeholder stubs - keep as they are for now)

# Actually, let's just replace from the first --- of the footer block
# Find the first --- that starts the footer block
sep_start = original.find('---\n'.encode('utf-8'), footer_idx - 200)
if sep_start < 0:
    sep_start = original.rfind('---\n'.encode('utf-8'), 0, footer_idx)
print(f'Separator at: {sep_start}')

# The separator before chapter 13 placeholder is at sep_start
# Keep original[:sep_start], add new content, then original[idx:]
result = original[:sep_start] + new_content.encode('utf-8') + original[idx:]

# Write result
out_path = r'C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md'
with open(out_path, 'wb') as f:
    f.write(result)

print(f'Done! Written {len(result)} bytes to output file')
