import os, re

base = r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\acro-design-pro-vite\src\views'

# Button patterns to fix - wrap with 「」
# The patterns match text content inside <a-button>...</a-button> tags
button_fixes = [
    # Direct text after tag (with optional attributes)
    ('">新建</a-button>', '">「新建」</a-button>'),
    ('">编辑</a-button>', '">「编辑」</a-button>'),
    ('">删除</a-button>', '">「删除」</a-button>'),
    ('">批量导入</a-button>', '">「批量导入」</a-button>'),
    ('">导出</a-button>', '">「导出」</a-button>'),
    ('">刷新</a-button>', '">「刷新」</a-button>'),
    ('">保存</a-button>', '">「保存」</a-button>'),
    ('">取消</a-button>', '">「取消」</a-button>'),
    ('">创建</a-button>', '">「创建」</a-button>'),
    ('">查询</a-button>', '">「查询」</a-button>'),
    ('">重置</a-button>', '">「重置」</a-button>'),
    ('">确认</a-button>', '">「确认」</a-button>'),
    ('">详情</a-button>', '">「详情」</a-button>'),
    ('">分配权限</a-button>', '">「分配权限」</a-button>'),
    ('">新增下级</a-button>', '">「新增下级」</a-button>'),
    # Emoji + text
    ('">🔄 刷新</a-button>', '">「刷新」</a-button>'),
    # Specific button texts
    ('">保存设置</a-button>', '">「保存」</a-button>'),
    ('">保存配置</a-button>', '">「保存」</a-button>'),
    ('">确认调整</a-button>', '">「确认」</a-button>'),
    # Radio buttons
    ('">新建</a-radio>', '">「新建」</a-radio>'),
    # Template button icons (no closing >)
    ('>🔄 刷新', '>「刷新」'),
    ('>刷新</a-button>', '>「刷新」</a-button>'),
]

# Files to process
vue_files = []
for root, dirs, files in os.walk(base):
    for fname in files:
        if fname.endswith('.vue'):
            vue_files.append(os.path.join(root, fname))

fixed_count = 0
for fpath in sorted(vue_files):
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    original = content
    for old, new in button_fixes:
        content = content.replace(old, new)
    if content != original:
        with open(fpath, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(content)
        rel = os.path.relpath(fpath, base)
        print(f'Fixed: {rel}')
        fixed_count += 1

print(f'\nTotal files fixed: {fixed_count}')
