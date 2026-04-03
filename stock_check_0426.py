# -*- coding: utf-8 -*-
import urllib.request
import json
import ssl
import datetime
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ssl._create_default_https_context = ssl._create_unverified_context

# 主账户持仓
positions = {
    '浙江龙盛': ('sh600352', 16.948, 12.0, 76700),
    '同花顺': ('sz300033', 423.488, 280, 1200),
    '亨通光电': ('sh600487', 43.210, 38.0, 3000),
    '航发动力': ('sh600893', 49.184, 42.0, 9000),
    '西部矿业': ('sh601168', 26.169, 22.0, 11000),
    '黄金ETF': ('sh518880', 9.868, None, 24000),
    '普适导航': ('bj831330', 20.361, 18.0, 7370),
    '圣博润': ('sz430046', 0.478, None, 10334),
}

# 老婆账户
wife_positions = {
    '东睦股份': ('sh600114', 31.176, 25.0, 11100),
}

# 两融账户
margin_positions = {
    '特变电工': ('sh600089', 24.765, 25.0, 52300),
}

def get_price(code):
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 4:
                return float(parts[3])
    except Exception as e:
        return None
    return None

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
print(f"📊 持仓监控 {now}\n{'='*50}")

all_positions = list(positions.items()) + [('东睦股份(老婆账户)', wife_positions['东睦股份'])] + [('特变电工(两融)', margin_positions['特变电工'])]

alerts = []
for name, (code, cost, stop, qty) in all_positions:
    price = get_price(code)
    if price is None:
        print(f'{name}({code}): 获取失败')
        continue
    pnl = (price - cost) * qty
    pnl_pct = (price / cost - 1) * 100
    flag = ''
    if stop and price <= stop:
        flag = ' ⚠️ 触及止损!'
        alerts.append(f'{name} 现价{price}，低于止损价{stop}')
    elif stop and price <= cost * 0.95:
        flag = ' ⚡ 低于成本5%'
    
    print(f'{name}: 现价{price:.3f} | 成本{cost:.3f} | 盈亏{pnl:+.2f}({pnl_pct:+.1f}%) | {qty}股{flag}')

print()
if alerts:
    print('🚨 预警:')
    for a in alerts:
        print(f'  {a}')
else:
    print('✅ 目前无触及止损的持仓')
