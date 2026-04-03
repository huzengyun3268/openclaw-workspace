#!/usr/bin/env python3
import urllib.request
import sys

url = 'https://hq.sinajs.cn/list=sh600352,sh600893,sz300033,sh601168,bj831330,sh600487,sh688295,bx430046,sh601318,sh601857'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn'
})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk', errors='replace')
    lines = raw.strip().split('\n')
    
    holdings = {
        'sh600352': {'name': '浙江龙盛', 'cost': 16.52, 'stop': 12.0, 'shares': 86700},
        'sh600893': {'name': '航发动力', 'cost': 49.184, 'stop': 42.0, 'shares': 9000},
        'sz300033': {'name': '同花顺', 'cost': 423.488, 'stop': 280.0, 'shares': 1200},
        'sh601168': {'name': '西部矿业', 'cost': 26.169, 'stop': 22.0, 'shares': 11000},
        'bj831330': {'name': '普适导航', 'cost': 20.361, 'stop': 18.0, 'shares': 7370},
        'sh600487': {'name': '亨通光电', 'cost': 45.47, 'stop': 38.0, 'shares': 4000},
        'sh688295': {'name': '中复神鹰', 'cost': 56.85, 'stop': 0, 'shares': 3000},
        'bx430046': {'name': '圣博润', 'cost': 0.478, 'stop': 0, 'shares': 10334},
        'sh601318': {'name': '中国平安', 'cost': 0, 'stop': 0, 'shares': 0},
        'sh601857': {'name': '中国石油', 'cost': 0, 'stop': 0, 'shares': 0},
    }
    
    total_pl = 0
    print("=== 主账户持仓监控 10:17 ===")
    print(f"{'股票':<10} {'现价':>7} {'涨跌%':>6} {'成本':>7} {'盈亏':>9} {'止损':>6} {'状态'}")
    print("-" * 70)
    
    for line in lines:
        if '=' not in line:
            continue
        parts = line.split('"')
        if len(parts) < 2:
            continue
        code_part = line.split('_')[1].split('=')[0]
        
        fields = parts[1].split(',')
        if len(fields) < 10:
            print(f"{code_part}: 无数据")
            continue
            
        try:
            name = fields[0]
            price = float(fields[3])
            yclose = float(fields[2])
            change_pct = (price - yclose) / yclose * 100
            h = holdings.get(code_part, {})
            cost = h.get('cost', 0)
            stop = h.get('stop', 0)
            shares = h.get('shares', 0)
            
            if cost > 0:
                pl = (price - cost) * shares
                total_pl += pl
                pl_str = f"{pl:+.1f}万"
                status = ""
                if price <= stop and stop > 0:
                    status = "⚠️ 触及止损"
                elif price > cost * 1.05:
                    status = "✅ 强势"
                elif price < cost * 0.95:
                    status = "❗ 跌破成本"
                print(f"{name:<8} {price:>7.3f} {change_pct:>+5.2f}% {cost:>7.3f} {pl_str:>9} {stop:>6.2f} {status}")
            else:
                print(f"{name:<8} {price:>7.3f} {change_pct:>+5.2f}% {'--':>7} {'--':>9} {'--':>6}")
        except Exception as e:
            print(f"解析错误 {code_part}: {e}")
    
    print("-" * 70)
    print(f"持仓浮动盈亏合计: {total_pl:+.1f}万元")
    
except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)
