import os, re

base = r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views'

# Files to fix (the main ones)
target_files = [
    'DeviceDashboard.vue',
    'DeviceStatus.vue', 
    'PetConfig.vue',
    'OtaFirmware.vue',
    'DeviceDetail.vue',
]

for fname in target_files:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        print(f'Not found: {fpath}')
        continue
        
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    original = content
    
    # Fix button texts - wrap with 「」
    # Pattern: >text</a-button>  (after the > of opening tag, before closing tag)
    # This regex finds text immediately followed by </a-button>
    fixes = [
        (r'>新建</a-button>', '>「新建」</a-button>'),
        (r'>编辑</a-button>', '>「编辑」</a-button>'),
        (r'>删除</a-button>', '>「删除」</a-button>'),
        (r'>批量导入</a-button>', '>「批量导入」</a-button>'),
        (r'>导出</a-button>', '>「导出」</a-button>'),
        (r'>刷新</a-button>', '>「刷新」</a-button>'),
        (r'>保存</a-button>', '>「保存」</a-button>'),
        (r'>取消</a-button>', '>「取消」</a-button>'),
        (r'>创建</a-button>', '>「创建」</a-button>'),
        (r'>查询</a-button>', '>「查询」</a-button>'),
        (r'>重置</a-button>', '>「重置」</a-button>'),
        (r'>确认</a-button>', '>「确认」</a-button>'),
        (r'>详情</a-button>', '>「详情」</a-button>'),
        (r'>分配权限</a-button>', '>「分配权限」</a-button>'),
        (r'>新增下级</a-button>', '>「新增下级」</a-button>'),
        (r'>🔄 刷新</a-button>', '>「刷新」</a-button>'),
        (r'>保存设置</a-button>', '>「保存」</a-button>'),
        (r'>保存配置</a-button>', '>「保存」</a-button>'),
        (r'>确认调整</a-button>', '>「确认」</a-button>'),
    ]
    
    for old, new in fixes:
        content = content.replace(old, new)
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(content)
        print(f'Fixed: {fname}')
    else:
        print(f'No changes: {fname}')

print('Done')
