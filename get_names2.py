# -*- coding: utf-8 -*-
import urllib.request, json

codes = ['sz002471', 'sh688011', 'sz002491']
url = "https://stockboot.jiuma.cn/api/quote/batch"
headers = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0'}
data = json.dumps(codes).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method='POST')
with urllib.request.urlopen(req, timeout=10) as r:
    result = json.loads(r.read().decode('utf-8'))

fields = result['data']['fields']
items = result['data']['items']
for item in items:
    d = dict(zip(fields, item))
    print(f"{d.get('code','')} {d.get('name','')} {d.get('changeRate','')}% {d.get('volRatio','')}")
