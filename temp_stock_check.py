# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

stocks = [
    ('600352', '浙江龙盛', 15.952, 12.0),
    ('300033', '同花顺', 423.488, 280.0),
    ('000988', '华工科技', 116.87, None),
    ('688295', '中复神鹰', 37.843, None),
    ('600487', '亨通光电', 42.391, None),
    ('300499', '高澜股份', 41.625, 38.0),
    ('601168', '西部矿业', 24.863, None),
    ('600893', '航发动力', 47.196, None),
    ('920046', '亿能电力', 329.555, 27.0),
    ('600089', '特变电工', 24.765, 25.0),
]

print('=== 持仓监控 13:45 ===')
try:
    df = ak.stock_zh_a_spot_em()
    for code, name, cost, stop_loss in stocks:
        try:
            row = df[df['代码'] == code]
            if not row.empty:
                price = float(row['最新价'].values[0])
                change_pct = float(row['涨跌幅'].values[0])
                profit = (price - cost) * 100 if '300' not in code and '688' not in code and '920' not in code else 0
                # 估算盈亏（简化，假设沪市1手=100股，深市/科创/北交所同理）
                if '920' in code or '830' in code:
                    shares = 200 if '920' in code else 7370
                elif '688' in code:
                    shares = 1500
                else:
                    shares = 1000 if code.startswith(('6','0')) else 1000
                
                if code == '600352':
                    shares = 106700
                elif code == '300033':
                    shares = 1200
                elif code == '000988':
                    shares = 1000
                elif code == '688295':
                    shares = 1500
                elif code == '600487':
                    shares = 2000
                elif code == '300499':
                    shares = 1500
                elif code == '601168':
                    shares = 2000
                elif code == '600893':
                    shares = 1000
                elif code == '920046':
                    shares = 200
                elif code == '600089':
                    shares = 52300

                pnl = (price - cost) * shares
                pct = (price - cost) / cost * 100
                warn = ''
                if stop_loss and price <= stop_loss:
                    warn = ' ⚠️触及止损!'
                elif stop_loss and price < stop_loss * 1.05:
                    warn = ' ⚠️接近止损!'
                print(f'{code} {name}: {price:.3f} ({change_pct:+.2f}%) | 成本{cost:.3f} | 盈亏{pnl:+.0f}元({pct:+.1f}%){warn}')
            else:
                print(f'{code} {name}: 未找到')
        except Exception as e:
            print(f'{code} {name}: ERROR {e}')
except Exception as e:
    print(f'获取行情失败: {e}')
    import traceback
    traceback.print_exc()
