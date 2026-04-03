# -*- coding: utf-8 -*-
import requests
import json
import sys

# Holdings: (tencent_code, name, shares, cost, stop_loss, account)
holdings = [
    ('sh600352', '浙江龙盛', 76700, 16.948, 12.0, 'main'),
    ('sz300033', '同花顺', 1200, 423.488, 280, 'main'),
    ('sh600487', '亨通光电', 3000, 43.210, 38.0, 'main'),
    ('sh600893', '航发动力', 9000, 49.184, 42.0, 'main'),
    ('sh601168', '西部矿业', 11000, 26.169, 22.0, 'main'),
    ('sh518880', '黄金ETF', 24000, 9.868, 0, 'main'),
    ('bj831330', '普适导航', 7370, 20.361, 18.0, 'main'),
    ('sz430046', '圣博润', 10334, 0.478, 0, 'main'),
    ('sh600114', '东睦股份', 11100, 31.176, 25.0, 'wife'),
    ('sh600089', '特变电工', 52300, 24.765, 25.0, 'margin'),
]

results = []
for code, name, shares, cost, stop, account in holdings:
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        resp = requests.get(url, timeout=5)
        data = resp.text
        parts = data.split('~')
        if len(parts) > 4:
            current_price = float(parts[3])
            prev_close = float(parts[4])
            change_pct = (current_price - prev_close) / prev_close * 100
            pnl = (current_price - cost) * shares
            results.append({
                'name': name, 'code': code, 'price': current_price,
                'cost': cost, 'change_pct': change_pct,
                'pnl': pnl, 'stop': stop, 'account': account
            })
    except:
        pass

# Write JSON to file
output_path = r'C:\Users\Administrator\.openclaw\workspace\stock_check_result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('Done')
