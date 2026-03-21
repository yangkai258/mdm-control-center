import os, re

base = r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\acro-design-pro-vite\src\views'

files = ['DeviceDashboard.vue', 'DeviceStatus.vue', 'PetConfig.vue', 'OtaFirmware.vue']

for fname in files:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        continue
    
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    # Find button patterns in raw bytes and replace
    # Button closing tag: </a-button>
    button_end = b'</a-button>'
    
    # We need to find patterns like: >TEXT</a-button> where TEXT is button text
    # And replace with >「TEXT」</a-button>
    
    # Let's use a simpler approach - find all occurrences and replace manually
    
    # List of button texts we want to fix (in UTF-8 bytes)
    # "新建" in UTF-8 is: e6 96 b0 e5 bb ba
    # "删除" in UTF-8 is: e5 88 a0 e9 99 a4
    # etc.
    
    replacements = [
        (b'>\xe6\x96\xb0\xe5\xbb\xba</a-button>', b'>\xe3\x80\x8c\xe6\x96\xb0\xe5\xbb\xba\xe3\x80\x8d</a-button>'),  # 新建
        (b'>\xe5\x88\xa0\xe9\x99\xa4</a-button>', b'>\xe3\x80\x8c\xe5\x88\xa0\xe9\x99\xa4\xe3\x80\x8d</a-button>'),  # 删除
        (b'>\xe5\x87\xba\xe5\x8a\x9e</a-button>', b'>\xe3\x80\x8c\xe5\x87\xba\xe5\x8a\x9e\xe3\x80\x8d</a-button>'),  # 导出
        (b'>\xe9\x87\x8f\xe9\x98\x85</a-button>', b'>\xe3\x80\x8c\xe9\x87\x8f\xe9\x98\x85\xe3\x80\x8d</a-button>'),  # 刷新
    ]
    
    new_raw = raw
    changed = False
    for old_bytes, new_bytes in replacements:
        if old_bytes in new_raw:
            new_raw = new_raw.replace(old_bytes, new_bytes)
            changed = True
            print(f'{fname}: Found and replaced {old_bytes}')
    
    # Also fix: 批量导入 (e69 bens 批量, e5afbc 导入)
    batch_import = b'>\xe9\x87\x8f\xe9\x87\x8f\xe5\x85\xa5\xe5\xaf\xbc\xe5\x85\xa5'
    if batch_import in new_raw:
        new_new = new_raw.replace(batch_import, b'>\xe3\x80\x8c\xe9\x87\x8f\xe9\x87\x8f\xe5\x85\xa5\xe5\xaf\xbc\xe5\x85\xa5\xe3\x80\x8d')
        if new_new != new_raw:
            new_raw = new_new
            changed = True
            print(f'{fname}: Found and replaced 批量导入')
    
    if changed:
        with open(fpath, 'wb') as f:
            f.write(new_raw)
        print(f'Written: {fname}')
    else:
        print(f'No changes: {fname}')
