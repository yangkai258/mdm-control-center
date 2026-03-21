import os

files_to_fix = [
    r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue',
    r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceStatus.vue',
    r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\PetConfig.vue',
    r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\OtaFirmware.vue',
    r'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDetail.vue',
]

for fpath in files_to_fix:
    if not os.path.exists(fpath):
        print(f'Not found: {fpath}')
        continue
    
    # Read as binary
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    # Check if it has BOM, skip if not starting with expected template
    if not raw.startswith(b'<template>'):
        print(f'{os.path.basename(fpath)}: Missing <template> at start')
        # Try removing BOM
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
            print(f'  Removed BOM, now starts with: {raw[:20]}')
    
    # Try to decode as GBK (original encoding)
    try:
        content = raw.decode('gbk')
        # Check if it has valid Chinese characters
        if '新建' in content or '设备' in content or '管理' in content:
            print(f'{os.path.basename(fpath)}: Successfully decoded as GBK')
            
            # Now encode as UTF-8 with BOM
            utf8_content = content.encode('utf-8')
            with open(fpath, 'wb') as f:
                f.write(b'\xef\xbb\xbf')  # UTF-8 BOM
                f.write(utf8_content)
            print(f'  Written as UTF-8 with BOM')
        else:
            print(f'{os.path.basename(fpath)}: GBK decode OK but no Chinese found')
    except Exception as e:
        print(f'{os.path.basename(fpath)}: Error: {e}')

print('Done')
