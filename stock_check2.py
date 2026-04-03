# -*- coding: utf-8 -*-
import urllib.request
import json
from datetime import datetime

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

# 腾讯行情API
base_url = "https://qt.gtimg.cn/q="

# 拼接股票代码列表
codes_str = ','.join(stocks.keys())

try:
    req = urllib.request.Request(base_url + codes_str)
    req.add_header('User-Agent', 'Mozilla/5.0')
    response = urllib.request.urlopen(req, timeout=10)
    content = response.read().decode('gbk')
    lines = content.strip().split('\n')
    
    price_data = {}
    for line in lines:
        if 'v_' in line:
            parts = line.split('~')
            if len(parts) > 35:
                code = parts[0].replace('v_', '')
                price = float(parts[3]) if parts[3] else 0
                yesterday_close = float(parts[4]) if parts[4] else price
                change_pct = ((price - yesterday_close) / yesterday_close * 100) if yesterday_close else 0
                name = parts[1]
                price_data[code] = (name, price, change_pct)
    
    total_pnl = 0
    for code, (name, cost, stop, shares) in stocks.items():
        if code in price_data:
            name_q, price, change_pct = price_data[code]
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
    print(f"获取数据失败: {str(e)}")
