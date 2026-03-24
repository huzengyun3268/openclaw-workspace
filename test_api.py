# -*- coding: utf-8 -*-
import requests
stocks = {'600352': '浙江龙盛', '600089': '特变电工'}
code_list = []
for code in stocks:
    if code.startswith('6'):
        code_list.append('sh' + code)
    else:
        code_list.append('sz' + code)
url = 'https://qt.gtimg.cn/q=' + ','.join(code_list)
print('URL: ' + url)
resp = requests.get(url, timeout=15)
resp.encoding = 'gbk'
raw = resp.text
print('Raw length: ' + str(len(raw)))
print(repr(raw[:200]))
lines = raw.strip().split('\n')
print('Line count: ' + str(len(lines)))
for i, line in enumerate(lines):
    print('Line ' + str(i) + ' len=' + str(len(line)) + ' startswith v=' + str(line.startswith('v_')))
    if len(line) > 5:
        print('  first 100 chars: ' + repr(line[:100]))
