import os, re

base = r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views'

# Use hex escapes to avoid encoding issues
# "新建" = \xe6\x96\xb0\xe5\xbb\xba
# "「新建" = \xe3\x80\x8c\xe6\x96\xb0\xe5\xbb\xba

replacements = [
    # 新建 -> 「新建
    (b'>\xe6\x96\xb0\xe5\xbb\xba</a-button>', b'>\xe3\x80\x8c\xe6\x96\xb0\xe5\xbb\xba\xe3\x80\x8d</a-button>'),
    # 删除 -> 「删除
    (b'>\xe5\x88\xa0\xe9\x99\xa4</a-button>', b'>\xe3\x80\x8c\xe5\x88\xa0\xe9\x99\xa4\xe3\x80\x8d</a-button>'),
    # 编辑 -> 「编辑
    (b'>\xe7\xbc\x96\xe8\xbe\x91</a-button>', b'>\xe3\x80\x8c\xe7\xbc\x96\xe8\xbe\x91\xe3\x80\x8d</a-button>'),
    # 导出 -> 「导出
    (b'>\xe5\xaf\xbc\xe5\x87\xba</a-button>', b'>\xe3\x80\x8c\xe5\xaf\xbc\xe5\x87\xba\xe3\x80\x8d</a-button>'),
    # 刷新 -> 「刷新
    (b'>\xe5\x88\xb7\xe6\x96\xb0</a-button>', b'>\xe3\x80\x8c\xe5\x88\xb7\xe6\x96\xb0\xe3\x80\x8d</a-button>'),
    # 保存 -> 「保存
    (b'>\xe4\xbf\x9d\xe5\xad\x98</a-button>', b'>\xe3\x80\x8c\xe4\xbf\x9d\xe5\xad\x98\xe3\x80\x8d</a-button>'),
    # 取消 -> 「取消
    (b'>\xe5\x8f\x96\xe6\xb6\x88</a-button>', b'>\xe3\x80\x8c\xe5\x8f\x96\xe6\xb6\x88\xe3\x80\x8d</a-button>'),
    # 批量导入 -> 「批量导入
    (b'>\xe9\x87\x8f\xe9\x87\x8f\xe5\x85\xa5\xe5\xaf\xbc\xe5\x85\xa5</a-button>', b'>\xe3\x80\x8c\xe9\x87\x8f\xe9\x87\x8f\xe5\x85\xa5\xe5\xaf\xbc\xe5\x85\xa5\xe3\x80\x8d</a-button>'),
]

files = ['DeviceStatus.vue', 'PetConfig.vue', 'OtaFirmware.vue']

for fname in files:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        continue
    
    with open(path, 'rb') as f:
        raw = f.read()
    
    original = raw
    for old, new in replacements:
        raw = raw.replace(old, new)
    
    if raw != original:
        with open(path, 'wb') as f:
            f.write(raw)
        print(f'Fixed: {fname}')
    else:
        print(f'No changes: {fname}')

print('Done')
