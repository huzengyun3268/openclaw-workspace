# -*- coding: utf-8 -*-
import akshare as ak
import json

codes = ['600352', '600893', '300033', '601168', '831330', '600487', '688295', '920046', '430046', '600089', '600114', '301638']
names = {
    '600352': '浙江龙盛', '600893': '航发动力', '300033': '同花顺',
    '601168': '西部矿业', '831330': '普适导航', '600487': '亨通光电',
    '688295': '中复神鹰', '920046': '亿能电力', '430046': '圣博润',
    '600089': '特变电工', '600114': '东睦股份', '301638': '南网数字'
}

stop_loss = {
    '600352': 12.0, '600893': 42.0, '300033': 280.0,
    '601168': 22.0, '831330': 18.0, '600487': 38.0,
    '600089': 25.0, '600114': 25.0, '301638': 28.0
}

holdings = {
    '600352': {'qty': 86700, 'cost': 16.52},
    '600893': {'qty': 9000, 'cost': 49.184},
    '300033': {'qty': 1200, 'cost': 423.488},
    '601168': {'qty': 11000, 'cost': 26.169},
    '831330': {'qty': 7370, 'cost': 20.361},
    '600487': {'qty': 3000, 'cost': 43.998},
    '688295': {'qty': 1500, 'cost': 37.843},
    '920046': {'qty': 200, 'cost': 329.553},
    '430046': {'qty': 10334, 'cost': 0.478},
    '600089': {'qty': 52300, 'cost': 24.765},
    '600114': {'qty': 4900, 'cost': 26.0},
    '301638': {'qty': 1700, 'cost': 32.64},
}

try:
    df = ak.stock_zh_a_spot_em()
    df = df[df['代码'].isin(codes)]

    results = []
    for _, row in df.iterrows():
        code = row['代码']
        name = names.get(code, code)
        price = float(row['最新价'])
        change_pct = float(row.get('涨跌幅', 0))
        qty_info = holdings.get(code, {})
        qty = qty_info.get('qty', 0)
        cost = qty_info.get('cost', 0)
        sl = stop_loss.get(code, None)
        pnl = (price - cost) * qty if qty > 0 else 0
        sl_hit = (sl is not None and price < sl)

        results.append({
            'code': code,
            'name': name,
            'price': price,
            'change_pct': change_pct,
            'qty': qty,
            'cost': cost,
            'stop_loss': sl,
            'pnl': round(pnl, 0),
            'sl_hit': sl_hit
        })

    # Sort by account group
    main = [r for r in results if r['code'] not in ['600089', '600114', '301638']]
    margin = [r for r in results if r['code'] == '600089']
    wife = [r for r in results if r['code'] in ['600114', '301638']]

    print('=== 主账户持仓 ===')
    total_pnl = 0
    for r in main:
        sl_str = f"| 止损{r['stop_loss']}" if r['stop_loss'] else ""
        sl_warning = " ⚠️触及止损!" if r['sl_hit'] else ""
        print(f"{r['name']}({r['code']}): 现价{r['price']} | 涨跌{r['change_pct']}% | 盈亏{r['pnl']}元{sl_str}{sl_warning}")
        total_pnl += r['pnl']
    print(f"主账户浮动盈亏合计: {round(total_pnl, 0)}元")

    print('\n=== 两融账户持仓 ===')
    for r in margin:
        sl_str = f"| 止损{r['stop_loss']}" if r['stop_loss'] else ""
        sl_warning = " ⚠️触及止损!" if r['sl_hit'] else ""
        print(f"{r['name']}({r['code']}): 现价{r['price']} | 涨跌{r['change_pct']}% | 盈亏{r['pnl']}元{sl_str}{sl_warning}")

    print('\n=== 老婆账户持仓 ===')
    for r in wife:
        sl_str = f"| 止损{r['stop_loss']}" if r['stop_loss'] else ""
        sl_warning = " ⚠️触及止损!" if r['sl_hit'] else ""
        print(f"{r['name']}({r['code']}): 现价{r['price']} | 涨跌{r['change_pct']}% | 盈亏{r['pnl']}元{sl_str}{sl_warning}")

    # Check for alerts
    alerts = [r for r in results if r['sl_hit']]
    if alerts:
        print('\n⚠️ 止损预警:')
        for a in alerts:
            print(f"  {a['name']}({a['code']}) 现价{a['price']} < 止损价{a['stop_loss']}")

except Exception as e:
    print(f'获取数据失败: {e}')
