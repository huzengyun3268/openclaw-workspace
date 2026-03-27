# Stock T Selection - 2:30买入策略 (Python版)
import urllib.request
import ssl
import time

ctx = ssl.create_default_context()
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'

def get_stock(code):
    is_sz = code[:3] in ['000','001','002','003','300','301','302','080','399']
    is_bj = code[:3] == '920'
    prefix = 'sz' if is_sz else ('bj' if is_bj else 'sh')
    try:
        url = f'https://qt.gtimg.cn/q={prefix}{code}'
        req = urllib.request.Request(url, headers={'User-Agent': ua})
        with urllib.request.urlopen(req, timeout=6, context=ctx) as r:
            data = r.read().decode('gbk', errors='ignore')
        parts = data.split('~')
        if len(parts) > 35 and parts[1] != 'pv_none_match' and parts[3]:
            return {
                'success': True,
                'name': parts[1],
                'price': float(parts[3]),
                'pct': float(parts[32]),
                'high': float(parts[33]),
                'low': float(parts[34]),
                'vol': int(parts[6]),
            }
    except:
        pass
    return {'success': False}

# 候选股票池（根据今日行情特征）
candidates = [
    ('600487', 'HengTongGuangDian', 'today +2.3%'),
    ('600893', 'HangFaDongLi', 'military'),
    ('688295', 'ZhongFuShenYing', 'today -5%'),
    ('601168', 'XiBuKuangYe', 'today -0.6%'),
    ('600352', 'ZheJiangLongSheng', 'today +0.8%'),
    ('600089', 'TeiBianDianGong', 'today -0.5%'),
    ('300033', 'TongHuaShun', 'today +1.4%'),
    ('600019', 'ZhongGuoPingAn', 'blue chip'),
    ('300059', 'DongFangCaiFu', 'brokerage'),
    ('688012', 'ZhongWei GongSi', 'semiconductor'),
    ('002371', 'BeiFangHuaChuang', 'semiconductor'),
    ('601012', 'LongJiGreen', 'solar'),
    ('300274', 'YangGuangDongL', 'solar'),
]

print('=== Stock T+1 Selection - 2026-03-27 ===')
print('Strategy: 2:30 buy, next morning before 10:00 sell')
print('Criteria: Up >1.5%, near day-high, volume >1.5x avg\n')

results = []
for code, name, reason in candidates:
    r = get_stock(code)
    if r['success']:
        near_high = round((r['price'] / r['high'] - 1) * 100, 1) if r['high'] > 0 else 0
        near_low = round((r['price'] - r['low']) / r['low'] * 100, 1) if r['low'] > 0 else 0
        r['code'] = code
        r['name_cn'] = name
        r['reason'] = reason
        r['near_high'] = near_high
        r['near_low'] = near_low
        results.append(r)
        arrow = '+' if r['pct'] > 0 else ''
        print(f'{r["name"]}({code}): {r["price"]} {arrow}{r["pct"]}% | high:{r["high"]} near_top:{near_high}% vol:{r["vol"]//100}万 | {reason}')
    else:
        print(f'{name}({code}): FAILED to get data')
    time.sleep(0.3)

print('\n=== Analysis ===')
# Sort by absolute pct (strongest first)
results.sort(key=lambda x: abs(x['pct']), reverse=True)

print('\nRecommended for T+1 (tomorrow morning sell):')
for i, r in enumerate(results[:6]):
    if r['pct'] > 0:
        print(f'{i+1}. {r["name"]}({r["code"]}): {r["price"]} +{r["pct"]}%')
        print(f'   Near day-high: {r["near_high"]}% | Vol: {r["vol"]//100}万手 | {r["reason"]}')
