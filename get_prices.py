import urllib.request
import json

codes = [
    ('600352', '浙江龙盛', '1.600352'),
    ('600893', '航发动力', '1.600893'),
    ('300033', '同花顺', '0.300033'),
    ('601168', '西部矿业', '1.601168'),
    ('831330', '普适导航', '0.831330'),
    ('600487', '亨通光电', '1.600487'),
    ('688295', '中复神鹰', '1.688295'),
    ('920046', '亿能电力', '0.920046'),
    ('430046', '圣博润', '0.430046'),
    ('600089', '特变电工', '1.600089'),
]

secids = ','.join([x[2] for x in codes])
url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f3,f4,f5&secids=' + secids
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = json.loads(resp.read())

name_map = {x[0]: x[1] for x in codes}
for item in data['data']['diff']:
    code = item['f12']
    name = name_map.get(code, item['f14'])
    price = item['f3']
    chg = item['f4']
    vol = item['f5']
    print(f"{name}({code}): 最新={price} 涨跌={chg}%")
