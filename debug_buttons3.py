import re
f = open(r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue', 'r', encoding='utf-8-sig')
content = f.read()
f.close()

# Check exact patterns
patterns = [
    '">新建</a-button>',
    '">删除</a-button>', 
    '">批量导入</a-button>',
    '">导出</a-button>',
    '">刷新</a-button>',
]

for p in patterns:
    found = p in content
    print(f'Pattern {repr(p)}: {found}')
    if not found:
        # Try to find similar
        idx = content.find(p[:6])
        if idx >= 0:
            print(f'  Found partial at {idx}: {repr(content[idx:idx+30])}')
