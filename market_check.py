# -*- coding: utf-8 -*-
import akshare as ak
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 三大指数
df = ak.stock_zh_index_spot_em()
idx = df[df['代码'].isin(['000001', '399001', '399006'])]
cols = ['代码', '名称', '最新价', '涨跌幅', '成交量', '成交额']
print("=== 三大指数 ===")
print(idx[cols].to_string(index=False))

# 涨跌家数
print("\n=== 市场概况 ===")
spot = ak.stock_zh_a_spot_em()
up = len(spot[spot['涨跌幅'] > 0])
down = len(spot[spot['涨跌幅'] < 0])
flat = len(spot[spot['涨跌幅'] == 0])
print(f"上涨: {up} 下跌: {down} 平盘: {flat}")

# 成交额前20
print("\n=== 成交额前20 ===")
top = spot.nlargest(20, '成交额')[['代码', '名称', '最新价', '涨跌幅', '成交额']]
print(top.to_string(index=False))

# 北向资金
try:
    hk = ak.stock_hsgt_north_net_flow_in_em()
    print("\n=== 北向资金 ===")
    print(hk.tail(5).to_string(index=False))
except:
    print("北向数据获取失败")
