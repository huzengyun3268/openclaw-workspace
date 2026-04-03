import tushare as ts
from datetime import datetime

ts.set_token('28babf6c11e9753b9c0e9c0af36a75f48fb18b47add9c7c3e2eacb6d0')
pro = ts.pro_api()

positions = [
    ('浙江龙盛', 'sh600352', 76700, 16.948, 12.0),
    ('同花顺', 'sz300033', 1200, 423.488, 280.0),
    ('亨通光电', 'sh600487', 3000, 43.210, 38.0),
    ('航发动力', 'sh600893', 9000, 49.184, 42.0),
    ('西部矿业', 'sh601168', 11000, 26.169, 22.0),
    ('黄金ETF', 'sh518880', 24000, 9.868, None),
    ('圣博润', 'sz430046', 10334, 0.478, None),
]

print(f"=== 持仓监控 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
for name, code, vol, cost, stop_loss in positions:
    try:
        df = pro.ts_daily(ts_code=code).head(1)
        if df.empty:
            print(f"{name}({code}): 无今日数据")
            continue
        price = df.iloc[0]['close']
        pre_close = df.iloc[0]['pre_close']
        chg_pct = (price - pre_close) / pre_close * 100
        profit = (price - cost) * vol
        flag = ""
        if stop_loss and price < stop_loss:
            flag = " ⚠️止损"
        elif price < cost * 0.9:
            flag = " 🔴深套"
        print(f"{name}: 现价{price:.3f} 涨跌{chg_pct:+.2f}% 盈亏{profit:+.0f}元{flag}")
    except Exception as e:
        print(f"{name}({code}): 获取失败 {e}")
