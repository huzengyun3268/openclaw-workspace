# -*- coding: utf-8 -*-
import akshare as ak
from datetime import datetime

stocks = {
    '600352': ('浙江龙盛', 106700, 15.91),
    '600089': ('特变电工', 52300, 24.765),
    '301667': ('纳百川', 3000, 82.715),
    '920046': ('亿能电力', 12731, 35.936),
    '300033': ('同花顺', 600, 511.22),
    '831330': ('普适导航', 6370, 20.415),
    '300189': ('神农种业', 5000, 17.099),
    '430046': ('圣博润', 10334, 0.478),
    '600114': ('东睦股份_老婆', 9200, 32.428),
    '301638': ('南网数字_老婆', 1700, 32.635),
}

print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('='*80)

df = ak.stock_zh_a_spot_em()

results = []
total_profit = 0
total_cost = 0
total_value = 0

for code, (name, qty, cost) in stocks.items():
    try:
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            change_pct = float(row['涨跌幅'].values[0])
            profit = (price - cost) * qty
            profit_pct = (price / cost - 1) * 100
            results.append({
                'name': name, 'code': code, 'qty': qty, 'cost': cost,
                'price': price, 'change_pct': change_pct,
                'profit': profit, 'profit_pct': profit_pct
            })
            total_profit += profit
            total_cost += cost * qty
            total_value += price * qty
        else:
            results.append({'name': name, 'code': code, 'error': '未找到'})
    except Exception as e:
        results.append({'name': name, 'code': code, 'error': str(e)})

for r in results:
    if 'error' in r:
        print(f"{r['name']}({r['code']}): 错误 - {r['error']}")
    else:
        sign = '+' if r['profit'] >= 0 else ''
        print(f"{r['name']}({r['code']}): 现价={r['price']:.3f} 涨跌={r['change_pct']:+.2f}% 持仓={r['qty']}股 成本={r['cost']:.3f} 盈亏={sign}{r['profit']:.0f}({sign}{r['profit_pct']:.1f}%)")

print('='*80)
sign = '+' if total_profit >= 0 else ''
print(f'总盈亏: {sign}{total_profit:.0f}元  总成本: {total_cost:.0f}元  总市值: {total_value:.0f}元  收益率: {sign}{(total_profit/total_cost*100):.2f}%')
