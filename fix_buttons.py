# -*- coding: utf-8 -*-
import os, sys, re

base = r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views'

replacements = [
    # Main action bar buttons
    ('>新建</a-button>', '>「新建」</a-button>'),
    ('>编辑</a-button>', '>「编辑」</a-button>'),
    ('>删除</a-button>', '>「删除」</a-button>'),
    ('>批量导入</a-button>', '>「批量导入」</a-button>'),
    ('>导出</a-button>', '>「导出」</a-button>'),
    ('>刷新</a-button>', '>「刷新」</a-button>'),
    ('>保存</a-button>', '>「保存」</a-button>'),
    ('>取消</a-button>', '>「取消」</a-button>'),
    ('>创建</a-button>', '>「创建」</a-button>'),
    # Filter/form buttons
    ('>查询</a-button>', '>「查询」</a-button>'),
    ('>重置</a-button>', '>「重置」</a-button>'),
    # Confirm buttons
    ('>确认</a-button>', '>「确认」</a-button>'),
    ('>确认调整</a-button>', '>「确认」</a-button>'),
    # Emoji button
    ('>🔄 刷新</a-button>', '>「刷新」</a-button>'),
    ('🔄 刷新', '「刷新」'),
    # Action column buttons
    ('>详情</a-button>', '>「详情」</a-button>'),
    ('>分配权限</a-button>', '>「分配权限」</a-button>'),
    # Tree node action buttons
    ('>新增下级</a-button>', '>「新增下级」</a-button>'),
    ('>编辑</a-button>', '>「编辑」</a-button>'),
    ('>删除</a-button>', '>「删除」</a-button>'),
    # Radio buttons
    ('>新建</a-radio>', '>「新建」</a-radio>'),
    # Save without button (form submit)
    ('>保存</a-button>', '>「保存」</a-button>'),
    # Specific text replacements
    ('>保存设置</a-button>', '>「保存」</a-button>'),
    ('>保存成功</a-button>', '>「保存」</a-button>'),
    # 树节点内的按钮
    (">新增下级</a-button>", ">「新增下级」</a-button>"),
    ("<a-button type='text' size='mini' @click.stop='openCreateModal(node)'>新增下级</a-button>", "<a-button type='text' size='mini' @click.stop=\"openCreateModal(node)\">「新增下级」</a-button>"),
    ("<a-button type='text' size='mini' @click.stop='openEditModal(node)'>编辑</a-button>", "<a-button type='text' size='mini' @click.stop=\"openEditModal(node)\">「编辑」</a-button>"),
    ("<a-button type='text' size='mini' status='danger' @click.stop='handleDeleteOne(node)'>删除</a-button>", "<a-button type='text' size='mini' status='danger' @click.stop=\"handleDeleteOne(node)\">「删除」</a-button>"),
]

# Files to process
vue_files = []
for root, dirs, files in os.walk(base):
    for fname in files:
        if fname.endswith('.vue'):
            vue_files.append(os.path.join(root, fname))

fixed_count = 0
for fpath in sorted(vue_files):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    if content != original:
        with open(fpath, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(content)
        rel = os.path.relpath(fpath, base)
        print(f'Fixed: {rel}')
        fixed_count += 1

print(f'\nTotal files fixed: {fixed_count}')
