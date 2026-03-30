import akshare as ak
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get major indices
try:
    indices = ak.stock_zh_index_spot_em()
    major = indices[indices['代码'].isin(['000001', '399001', '399006', '000688'])]
    for _, row in major.iterrows():
        print(f"INDEX|{row['名称']}|{row['代码']}|{row['最新价']}|{row['涨跌幅']}")
except Exception as e:
    print(f"INDEX_ERROR: {e}")

# Try getting bj stocks from a different source
try:
    bj = ak.stock_bid_ask_em(symbol='831330')
    print(f"普适导航 bid-ask: {bj}")
except Exception as e:
    print(f"普适导航_ERROR: {e}")

try:
    bj2 = ak.stock_bid_ask_em(symbol='430046')
    print(f"圣博润 bid-ask: {bj2}")
except Exception as e:
    print(f"圣博润_ERROR: {e}")
