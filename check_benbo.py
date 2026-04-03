# -*- coding: utf-8 -*-
import urllib.request

url = 'https://qt.gtimg.cn/q=sz430046'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'})
r = urllib.request.urlopen(req, timeout=10)
raw = r.read().decode('gbk')
import sys
sys.stdout.buffer.write(raw.encode('utf-8'))
