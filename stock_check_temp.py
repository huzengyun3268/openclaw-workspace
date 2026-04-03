# -*- coding: utf-8 -*-
stocks = {
    'sh600352': ('\u6d59\u6c5f\u9f99\u76db', 76700, 16.948, 12.0, 12.92, -2.27),
    'sz300033': ('\u540c\u82b1\u987a', 1200, 423.488, 280, 293.15, -1.66),
    'sh600487': ('\u4ea8\u901a\u5149\u7535', 3000, 43.210, 38.0, 58.16, 8.93),
    'sh600893': ('\u822a\u53d1\u52a8\u529b', 9000, 49.184, 42.0, 48.52, -2.57),
    'sh601168': ('\u897f\u90e8\u77ff\u4e1a', 11000, 26.169, 22.0, 25.54, 0.16),
    'sh518880': ('\u9ec4\u91d1ETF', 24000, 9.868, None, 9.819, 0.83),
    'sh600114': ('\u4e1c\u58a9\u80a1\u4efd(\u8001\u5a46)', 11100, 31.176, 25.0, 27.34, -0.62),
    'sh600089': ('\u7279\u53d8\u7535\u5de5(\u4e24\u878d)', 52300, 24.765, 25.0, 25.51, -2.52),
}

total_3293 = 0
total_2r = 0
total_wife = 0

for code, (name, vol, cost, stop, cur, pct) in stocks.items():
    pnl = (cur - cost) * vol
    if '\u8001\u5a46' in name:
        total_wife += pnl
    elif '\u4e24\u878d' in name:
        total_2r += pnl
    else:
        total_3293 += pnl
    dist = cur - stop if stop else None
    dist_pct = (dist/stop*100) if stop else None
    if stop and dist < 0.5:
        flag = '!!NEAR STOPLOSS!!'
    elif stop and dist < 1.0:
        flag = '!near stop!'
    elif pct > 5:
        flag = 'STRONG'
    else:
        flag = ''
    print(f'{name}: {cur}({pct:+.2f}%) | pnl {pnl/10000:+.1f}w | stop {stop} | dist {dist:.2f}({dist_pct:.1f}%) {flag}')

print(f'Main: {total_3293/10000:+.1f}w | Wife: {total_wife/10000:+.1f}w | Margin: {total_2r/10000:+.1f}w')
