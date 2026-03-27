import akshare as ak
import pandas as pd

codes = ['600352', '600893', '300033', '601168', '831330', '600487', '688295', '920046', '430046']
names = {'600352':'浙江龙盛','600893':'航发动力','300033':'同花顺','601168':'西部矿业','831330':'普适导航','600487':'亨通光电','688295':'中复神鹰','920046':'亿能电力','430046':'圣博润'}

# 成本价（从USER.md）
cost = {'600352':16.943,'600893':49.184,'300033':423.488,'601168':26.169,'831330':20.361,'600487':43.998,'688295':37.843,'920046':329.553,'430046':0.478}
# 止损价
stop = {'600352':12.0,'600893':42.0,'300033':280,'601168':22.0,'831330':18.0,'600487':38.0,'920046':'观察','430046':'无'}

try:
    df = ak.stock_zh_a_spot_em()
    df = df[df['代码'].isin(codes)][['代码','名称','最新价','涨跌幅','成交量','成交额']]
    print('=== 主账户持仓监控 2026-03-27 09:15 ===')
    for _, row in df.iterrows():
        code = row['代码']
        name = names.get(code, row['名称'])
        price = float(row['最新价'])
        change = float(row['涨跌幅'])
        vol = int(row['成交量']) if pd.notna(row['成交量']) else 0
        amount = float(row['成交额'])/10000 if pd.notna(row['成交额']) else 0
        cost_p = cost.get(code, 0)
        loss_pct = (price - cost_p) / cost_p * 100 if cost_p > 0 else 0
        stop_p = stop.get(code, 'N/A')
        stop_flag = ''
        if isinstance(stop_p, float) and price <= stop_p:
            stop_flag = ' ⚠️触及止损'
        elif isinstance(stop_p, float) and price <= stop_p * 1.05:
            stop_flag = ' ⚡逼近止损'
        print(f'{code} {name}: 现价={price:.3f}, 涨幅={change:+.2f}%, 成本={cost_p:.3f}, 盈亏={loss_pct:+.1f}%, 止损={stop_p}{stop_flag}')
        print(f'   成交量={vol}, 成交额={amount:.1f}万')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
