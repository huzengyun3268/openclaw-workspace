# -*- coding: utf-8 -*-
import json
import akshare as ak
import pandas as pd
from datetime import datetime

today = datetime.now().strftime('%Y%m%d')
result = {'date': today, 'zt': [], 'strong': [], 'dt': []}

# 今日涨停股池
try:
    df = ak.stock_zt_pool_em(date=today)
    if df is not None and not df.empty:
        cols = [c for c in ['代码','名称','涨停统计','流通市值','换手率','连板数'] if c in df.columns]
        sub = df[cols].head(15)
        result['zt'] = sub.to_dict(orient='records')
        result['zt_count'] = len(df)
except Exception as e:
    result['zt_error'] = str(e)

# 今日强势股
try:
    df_qs = ak.stock_zt_pool_strong_em(date=today)
    if df_qs is not None and not df_qs.empty:
        cols = [c for c in ['代码','名称','涨停统计','流通市值','换手率'] if c in df_qs.columns]
        sub = df_qs[cols].head(15)
        result['strong'] = sub.to_dict(orient='records')
        result['strong_count'] = len(df_qs)
except Exception as e:
    result['strong_error'] = str(e)

# 今日跌停股池
try:
    df_dt = ak.stock_zt_pool_dtgc_em(date=today)
    if df_dt is not None and not df_dt.empty:
        cols = [c for c in ['代码','名称','流通市值'] if c in df_dt.columns]
        sub = df_dt[cols].head(10)
        result['dt'] = sub.to_dict(orient='records')
        result['dt_count'] = len(df_dt)
except Exception as e:
    result['dt_error'] = str(e)

with open(r'C:\Users\Administrator\.openclaw\workspace\auction_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Done')
