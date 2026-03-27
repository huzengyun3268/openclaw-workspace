# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

codes = ['600352', '600893', '300033', '601168', '831330', '600487', '688295', '920046', '430046', '600114', '301638', '600089']
names = {
    '600352': '浙江龙盛', '600893': '航发动力', '300033': '同花顺',
    '601168': '西部矿业', '831330': '普适导航', '600487': '亨通光电',
    '688295': '中复神鹰', '920046': '亿能电力', '430046': '圣博润',
    '600114': '东睦股份', '301638': '南网数字', '600089': '特变电工'
}

stops = {
    '600352': 12.0, '600893': 42.0, '300033': 280, '601168': 22.0,
    '831330': 18.0, '600487': 38.0, '688295': None, '920046': None,
    '430046': None, '600114': 25.0, '301638': 28.0, '600089': 25.0
}

cost = {
    '600352': 16.52, '600893': 49.184, '300033': 423.488, '601168': 26.169,
    '831330': 20.361, '600487': 43.998, '688295': 37.843, '920046': 329.553,
    '430046': 0.478, '600114': 26.0, '301638': 32.64, '600089': 24.765
}

positions = {
    '600352': 86700, '600893': 9000, '300033': 1200, '601168': 11000,
    '831330': 7370, '600487': 3000, '688295': 1500, '920046': 200,
    '430046': 10334, '600114': 4900, '301638': 1700, '600089': 52300
}

try:
    df = ak.stock_zh_a_spot_em()
    df = df[df['代码'].isin(codes)][['代码', '名称', '最新价', '涨跌幅', '最高', '最低', '成交额']]
    df = df.set_index('代码')

    alerts = []
    print(f"{'代码':<8} {'名称':<10} {'最新价':>8} {'涨跌幅':>8} {'成本价':>8} {'止损价':>8} {'盈亏额':>10} {'状态':<6}")
    print("-" * 80)

    total_pnl = 0
    for code in codes:
        if code not in df.index:
            print(f"{code:<8} {names[code]:<10} -- 获取失败--")
            continue
        row = df.loc[code]
        price = float(row['最新价'])
        chg = float(row['涨跌幅'])
        stop = stops[code]
        c = cost[code]
        pos = positions[code]
        pnl = (price - c) * pos
        total_pnl += pnl

        status = "OK"
        alert = ""
        if stop and price <= stop:
            status = "止损!"
            alert = f"⚠️ {names[code]} 现价{price} <= 止损{stop}"
            alerts.append(alert)
        elif stop and price <= stop * 1.05:
            status = "⚠️警戒"

        pnl_str = f"{pnl:+.0f}"
        stop_str = f"{stop}" if stop else "-"
        print(f"{code:<8} {names[code]:<10} {price:>8.3f} {chg:>7.2f}% {c:>8.3f} {stop_str:>8} {pnl_str:>10} {status}")

    print("-" * 80)
    print(f"主账户+老婆账户+两融 浮动盈亏合计: {total_pnl:+.0f} 元")

    if alerts:
        print("\n🚨 止损警报:")
        for a in alerts:
            print(f"  {a}")
    else:
        print("\n✅ 暂无止损警报")

except Exception as e:
    print(f"获取数据失败: {e}")
    import traceback
    traceback.print_exc()
