# -*- coding: utf-8 -*-
import base64

# Read all base64 parts and decode
parts = []
for i in range(1, 10):
    try:
        with open(f"C:\\Users\\YKing\\.openclaw\\workspace\\part_{chr(96+i)}_b64.txt", "r") as f:
            b64 = f.read().strip()
        decoded = base64.b64decode(b64).decode("utf-8")
        parts.append(decoded)
        print(f"Part {chr(96+i)}: {len(decoded)} chars")
    except:
        break

new_chapters = "\n".join(parts)
print(f"Total new chapters: {len(new_chapters)} chars")

# Read original file
with open(r"C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD.md", "rb") as f:
    original = f.read()

# Find chapter 13 placeholder start (十三、基础管理)
search = "## 十三、基础管理".encode("utf-8")
idx = original.find(search)
print(f"Chapter 13 placeholder starts at byte: {idx}")

# Find the separator before it
sep = "---\n\n\n\n".encode("utf-8")  # 4 newlines
sep_pos = original.rfind(sep, 0, idx)
print(f"Separator at byte: {sep_pos}")

# Keep: original up to sep_pos (exclusive) + separator + new chapters + original from idx onward
result = original[:sep_pos] + new_chapters.encode("utf-8") + original[idx:]

# Write result
with open(r"C:\Users\YKing\.openclaw\workspace\mdm-project\docs\MULTI_TENANT_PRD_NEW.md", "wb") as f:
    f.write(result)

print(f"Written {len(result)} bytes to NEW file")
print("Done!")
