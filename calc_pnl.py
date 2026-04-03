import sys
sys.stdout.reconfigure(encoding='utf-8')
stocks = [
    ('浙江龙盛', 'sh600352', 76700, 16.948, 12.92),
    ('同花顺', 'sz300033', 1200, 423.488, 293.39),
    ('亨通光电', 'sh600487', 3000, 43.210, 57.87),
    ('航发动力', 'sh600893', 9000, 49.184, 48.52),
    ('西部矿业', 'sh601168', 11000, 26.169, 25.36),
    ('黄金ETF', 'sh518880', 24000, 9.868, 9.832),
    ('圣博润', 'sz430046', 10334, 0.478, 0.478),
    ('东睦股份(老婆)', 'sh600114', 11100, 31.176, 27.28),
    ('特变电工(两融)', 'sh600089', 52300, 24.765, 25.52),
]
total_pnl = 0
total_cost = 0
total_mv = 0
stop_loss_map = {
    '浙江龙盛': 12.0, '同花顺': 280.0, '亨通光电': 38.0,
    '航发动力': 42.0, '西部矿业': 22.0, '东睦股份(老婆)': 25.0,
    '特变电工(两融)': 25.0
}
for name, code, vol, cost, price in stocks:
    pnl = (price - cost) * vol
    pnl_pct = (price / cost - 1) * 100
    mv = price * vol
    total_pnl += pnl
    total_cost += cost * vol
    total_mv += mv
    sl = stop_loss_map.get(name, None)
    if sl and price < sl:
        status = ' <<< 止损触发!'
    elif sl and price < cost * 0.95:
        status = ' *接近止损'
    elif pnl > 0:
        status = ' 浮盈'
    else:
        status = ' 浮亏'
    print(f'{name}: 现价{price:.3f} 盈亏{pnl:+8.2f}万({pnl_pct:+6.1f}%) 市值{mv:8.2f}万 SL={sl if sl else "-"}{status}')
print('---')
print(f'合计盈亏: {total_pnl:+8.2f}万  总市值: {total_mv:.2f}万  总成本: {total_cost:.2f}万')
