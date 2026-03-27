# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

stocks = [
    ('600352', '浙江龙盛', 13.180, 12.0),
    ('600893', '航发动力', 47.960, 42.0),
    ('300033', '同花顺', 295.52, 280),
    ('601168', '西部矿业', 25.04, 22.0),
    ('831330', '普适导航', 19.97, 18.0),
    ('600487', '亨通光电', 48.01, 38.0),
    ('688295', '中复神鹰', 61.04, None),
    ('920046', '亿能电力', 28.20, None),
    ('430046', '圣博润', 0.30, None),
    ('600089', '特变电工', None, 25.0),
    ('600114', '东睦股份', None, 25.0),
    ('301638', '南网数字', None, 28.0),
]

print("获取实时行情...")
try:
    df = ak.stock_zh_a_spot_em()
    print(f"成功获取 {len(df)} 只股票数据")
except Exception as e:
    print(f"获取数据失败: {e}")
    df = None

print("\n=== 主账户持仓 ===")
if df is not None:
    for code, name, last_price, stop_loss in stocks[:9]:
        try:
            row = df[df['代码'] == code]
            if not row.empty:
                price = float(row['最新价'].values[0])
                chg_pct = float(row['涨跌幅'].values[0])
                vol = row['成交量'].values[0]
                if stop_loss:
                    distance = (price - stop_loss) / price * 100
                    warn = " ⚠️ 止损附近!" if distance < 5 else ""
                    print(f"{name}({code}): 现价={price} | 涨跌={chg_pct}% | 止损={stop_loss} | 距止损={distance:.1f}%{warn}")
                else:
                    print(f"{name}({code}): 现价={price} | 涨跌={chg_pct}%")
            else:
                print(f"{name}({code}): 未找到数据")
        except Exception as e:
            print(f"{name}({code}): 获取失败 {e}")

print("\n=== 两融账户 ===")
if df is not None:
    code, name, last_price, stop_loss = stocks[9]
    try:
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            chg_pct = float(row['涨跌幅'].values[0])
            distance = (price - stop_loss) / price * 100
            warn = " ⚠️ 止损附近!" if distance < 5 else ""
            print(f"{name}({code}): 现价={price} | 涨跌={chg_pct}% | 止损={stop_loss} | 距止损={distance:.1f}%{warn}")
    except Exception as e:
        print(f"{name}({code}): 获取失败 {e}")

print("\n=== 老婆账户 ===")
if df is not None:
    for code, name, last_price, stop_loss in stocks[10:]:
        try:
            row = df[df['代码'] == code]
            if not row.empty:
                price = float(row['最新价'].values[0])
                chg_pct = float(row['涨跌幅'].values[0])
                distance = (price - stop_loss) / price * 100
                warn = " ⚠️ 止损附近!" if distance < 5 else ""
                print(f"{name}({code}): 现价={price} | 涨跌={chg_pct}% | 止损={stop_loss} | 距止损={distance:.1f}%{warn}")
            else:
                print(f"{name}({code}): 未找到数据")
        except Exception as e:
            print(f"{name}({code}): 获取失败 {e}")
