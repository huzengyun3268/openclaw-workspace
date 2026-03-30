# -*- coding: utf-8 -*-
import urllib.request, json

url = "https://stockboot.jiuma.cn/api/dynamic-select/execute"
headers = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0'}
# 涨幅3-5%，量比大于1，流通市值50-200亿，非ST
condition = "涨幅大于3%小于5%;量比大于1;流通市值大于50亿小于200亿;非ST"
data = json.dumps({"sentence": condition}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method='POST')
with urllib.request.urlopen(req, timeout=15) as resp:
    result = json.loads(resp.read().decode('utf-8'))

print("CONDITION:", condition)
print("TOTAL:", result['data']['totalCount'])
for s in result['data']['stocks']:
    name = s.get('name', 'N/A')
    change = round(s.get('changeRate', 0), 2)
    extra = s.get('extraFields', {})
    vol_ratio = extra.get(list(extra.keys())[0], '') if extra else ''
    print(f"{s['code']} {name} {change}%  {vol_ratio}")
