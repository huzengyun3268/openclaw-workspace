# -*- coding: utf-8 -*-
import urllib.request
import sys

# 北交所 圣博润
url = 'http://hq.sinajs.cn/list=sh430046'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn/'
})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode('gbk')
    print(repr(data))
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
