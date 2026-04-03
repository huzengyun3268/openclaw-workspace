# -*- coding: utf-8 -*-
import urllib.request, json

stocks = [
    ('浙江龙盛', '600352', 'sh'),
    ('航发动力', '600893', 'sh'),
    ('同花顺', '300033', 'sz'),
    ('西部矿业', '601168', 'sh'),
    ('普适导航', '831330', 'bj'),
    ('亨通光电', '600487', 'sh'),
    ('中复神鹰', '688295', 'sh'),
    ('圣博润', '430046', 'bj'),
    ('东睦股份', '600114', 'sh'),
    ('特变电工', '600089', 'sh'),
]

results = []
for name, code, mkt in stocks:
    try:
        url = f'https://qt.gtimg.cn/q={mkt}{code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = r.read().decode('gbk')
        parts = data.split('~')
        if len(parts) > 4:
            price = parts[3]
            pct = parts[32] if len(parts) > 32 else 'N/A'
            change = parts[31] if len(parts) > 31 else 'N/A'
            results.append({'name': name, 'code': mkt+code, 'price': price, 'change': change, 'pct': pct})
        else:
            results.append({'name': name, 'code': mkt+code, 'error': '解析失败'})
    except Exception as e:
        results.append({'name': name, 'code': mkt+code, 'error': str(e)})

with open(r'C:\Users\Administrator\.openclaw\workspace\auction_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('Done')
