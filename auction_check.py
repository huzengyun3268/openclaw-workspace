# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings('ignore')

import akshare as ak
import datetime

# 指数实时行情
print("=== 指数行情 ===")
try:
    indices = ak.stock_zh_index_spot()
    key_indices = ['上证指数', '深证成指', '创业板指', '科创50', '沪深300']
    today = datetime.date.today().strftime('%Y-%m-%d')
    for _, row in indices.iterrows():
        name = str(row.get('名称', ''))
        if any(k in name for k in key_indices):
            price = row.get('最新价', 0)
            chg = row.get('涨跌幅', 0)
            print(f"{name}: {price} ({chg:+.2f}%)")
except Exception as e:
    print(f"指数数据: {e}")

# 涨跌停统计
print("\n=== 涨跌统计 ===")
try:
    spot = ak.stock_zh_a_spot_em()
    up10 = len(spot[spot['涨跌幅'] >= 9.9])
    down10 = len(spot[spot['涨跌幅'] <= -9.9])
    up5 = len(spot[(spot['涨跌幅'] >= 4.9) & (spot['涨跌幅'] < 9.9)])
    down5 = len(spot[(spot['涨跌幅'] <= -4.9) & (spot['涨跌幅'] > -9.9)])
    flat = len(spot[abs(spot['涨跌幅']) < 0.1])
    print(f"涨停(>=10%): {up10}  跌停(<=10%): {down10}")
    print(f"涨5-10%: {up5}  跌5-10%: {down5}  涨跌停: {flat}")
    total = len(spot)
    advance = len(spot[spot['涨跌幅'] > 0])
    decline = len(spot[spot['涨跌幅'] < 0])
    print(f"上涨: {advance}  下跌: {decline}  平: {total-advance-decline}  总: {total}")
except Exception as e:
    print(f"涨跌停统计: {e}")

# 持仓个股竞价数据
print("\n=== 持仓个股竞价 ===")
stocks = {
    '浙江龙盛': '600352',
    '同花顺': '300033',
    '华工科技': '000988',
    '中复神鹰': '688295',
    '亨通光电': '600487',
    '高澜股份': '300499',
    '西部矿业': '601168',
    '航发动力': '600893',
    '亿能电力': '920046',
    '东睦股份': '600114',
    '南网数字': '301638',
}
try:
    spot = ak.stock_zh_a_spot_em()
    codes = list(stocks.values())
    held = spot[spot['代码'].isin(codes)]
    for _, row in held.iterrows():
        name = row.get('名称', '')
        price = row.get('最新价', 0)
        chg = row.get('涨跌幅', 0)
        vol = row.get('成交量', 0)
        amount = row.get('成交额', 0)
        high52 = row.get('52周最高', 0)
        low52 = row.get('52周最低', 0)
        print(f"{name}({row.get('代码','')}): {price} ({chg:+.2f}%) 额:{amount/1e8:.1f}亿")
except Exception as e:
    print(f"持仓数据: {e}")

print(f"\n=== 时间 {datetime.datetime.now().strftime('%H:%M:%S')} ===")
