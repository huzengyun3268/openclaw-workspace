# -*- coding: utf-8 -*-
import urllib.request, json, sys

url = "https://stockboot.jiuma.cn/api/dynamic-select/execute"
headers = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0'}
condition = "涨幅大于3%小于10%;非ST;非一字涨停"
data = json.dumps({"sentence": condition}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method='POST')
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode('utf-8'))

print("CONDITION:", condition)
print("TOTAL:", result['data']['totalCount'])
for s in result['data']['stocks']:
    print(f"{s['code']} {s['name']} {round(s['changeRate'],2)}%")
