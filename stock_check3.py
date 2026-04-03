# -*- coding: utf-8 -*-
import urllib.request
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

stocks = {
    'sh600352': ('浙江龙盛', 16.948, 12.0, 76700),
    'sz300033': ('同花顺', 423.488, 280, 1200),
    'sh600487': ('亨通光电', 43.210, 38.0, 3000),
    'sh600893': ('航发动力', 49.184, 42.0, 9000),
    'sh601168': ('西部矿业', 26.169, 22.0, 11000),
    'sh518880': ('黄金ETF', 9.868, None, 24000),
    'sz430046': ('圣博润', 0.478, None, 10334),
    'sh600114': ('东睦股份(老婆)', 31.176, 25.0, 11100),
    'sh600089': ('特变电工(两融)', 24.765, 25.0, 52300),
}

print(f"=== 持仓监控 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

# 东方财富API
url = "http://push2.eastmoney.com/api/qt/ulist.np/get"
params = {
    'fltt': 2,
    'invt': 2,
    'secid': ','.join(stocks.keys()),
    'fields': 'f1,f2,f3,f4,f12,f14',
    'ut': 'b2884a393a59ad64002292a3e90d46a5',
}

try:
    import urllib.parse
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    req = urllib.request.Request(full_url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('Referer', 'http://quote.eastmoney.com/')
    response = urllib.request.urlopen(req, timeout=10)
    data = json.loads(response.read().decode('utf-8'))
    
    price_map = {}
    if data.get('data') and data['data'].get('diff'):
        for item in data['data']['diff']:
            code = item.get('f12')
            name = item.get('f14')
            price = item.get('f2')  # 现价
            change = item.get('f3')  # 涨跌幅%
            if price != '-' and price is not None:
                price_map[code] = (name, float(price), float(change) if change != '-' else 0)
    
    total_pnl = 0
    for code, (name, cost, stop, shares) in stocks.items():
        if code in price_map:
            name_q, price, change_pct = price_map[code]
            pnl = (price - cost) * shares
            pnl_pct = (price / cost - 1) * 100
            warn = ''
            if stop and price <= stop:
                warn = ' [预警：触及止损]'
            elif stop and price <= stop * 1.05:
                warn = ' [预警：接近止损]'
            print(f"{name}")
            print(f"  现价={price:.3f} 涨幅={change_pct:+.2f}% | 成本={cost:.3f} 盈亏={pnl_pct:+.1f}%({pnl/10000:+.1f}万){warn}")
            if stop:
                dist = ((price - stop) / stop * 100)
                print(f"  止损={stop} 距止损={dist:+.1f}%")
            total_pnl += pnl
        else:
            print(f"{name}({code}): 数据获取失败")
    
    print(f"\n总盈亏: {total_pnl/10000:+.2f}万元")

except Exception as e:
    print(f"东方财富API失败: {str(e)}")
    import traceback
    traceback.print_exc()
