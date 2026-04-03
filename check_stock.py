import urllib.request, sys

codes = {
    'sh601168': '西部矿业',
    'sh600487': '亨通光电',
    'sh600352': '浙江龙盛',
    'sh600893': '航发动力',
    'sz300033': '同花顺',
    'sh600114': '东睦股份',
    'sh600089': '特变电工',
    'sh518880': '黄金ETF'
}

results = []
for code, name in codes.items():
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=8)
        txt = r.read().decode('gbk')
        parts = txt.split('~')
        if len(parts) > 31:
            price = parts[3]
            change = parts[31]
            results.append(f"{name}|{price}|{change}")
    except Exception as e:
        results.append(f"{name}|查询失败|-")

for r in results:
    print(r)
