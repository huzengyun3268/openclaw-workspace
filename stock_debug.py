# -*- coding: utf-8 -*-
import requests
from datetime import datetime

stocks = {
    '600352': ('浙江龙盛', 106700, 15.91),
    '600089': ('特变电工', 52300, 24.765),
    '301667': ('纳百川', 3000, 82.715),
    '920046': ('亿能电力', 12731, 35.936),
    '300033': ('同花顺', 600, 511.22),
    '831330': ('普适导航', 6370, 20.415),
    '300189': ('神农种业', 5000, 17.099),
    '430046': ('圣博润', 10334, 0.478),
    '600114': ('东睦股份_老婆', 9200, 32.428),
    '301638': ('南网数字_老婆', 1700, 32.635),
}

# Build code mapping
code_list = []
for code in stocks:
    if code.startswith('6'):
        code_list.append('sh' + code)
    elif code.startswith('92'):
        code_list.append('bj' + code)
    elif code.startswith('83') or code.startswith('43'):
        code_list.append('bj' + code)
    else:
        code_list.append('sz' + code)

codes_str = ','.join(code_list)
url = 'https://qt.gtimg.cn/q=' + codes_str

print('URL: ' + url)

try:
    resp = requests.get(url, timeout=15)
    resp.encoding = 'gbk'
    raw = resp.text
    print('Response length: ' + str(len(raw)))
    print('First 500 chars:')
    print(raw[:500])
except Exception as e:
    print('API请求失败: ' + str(e))
