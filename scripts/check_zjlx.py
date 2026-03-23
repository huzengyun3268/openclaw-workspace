# -*- coding: utf-8 -*-
import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 浙江龙盛基本信息
url = 'http://push2.eastmoney.com/api/qt/stock/get?secid=1.600352&fields=f57,f58,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f56,f57,f58,f59,f60,f116,f117,f162,f163,f164,f170'
try:
    r = requests.get(url, timeout=10)
    data = r.json()
    d = data.get('data', {})
    print(f"股票名称: {d.get('f58', 'N/A')}")
    print(f"代码: 600352")
    print(f"现价: {d.get('f43', 'N/A')}")
    print(f"涨跌额: {d.get('f44', 'N/A')}")
    print(f"涨跌幅: {d.get('f45', 'N/A')}%")
    print(f"今开: {d.get('f46', 'N/A')}")
    print(f"昨收: {d.get('f47', 'N/A')}")
    print(f"成交量(手): {d.get('f47', 'N/A')}")
    print(f"成交额: {d.get('f47', 'N/A')}")
    print(f"52周最高: {d.get('f170', 'N/A')}")
    print(f"52周最低: {d.get('f168', 'N/A')}")
    print(f"市值: {d.get('f116', 'N/A')}")
    print(f"市盈率TTM: {d.get('f162', 'N/A')}")
    print(f"市净率: {d.get('f167', 'N/A')}")
    print(f"股息率: {d.get('f173', 'N/A')}")
except Exception as e:
    print(f'Error: {e}')

# 获取资金流向
url2 = 'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?secid=1.600352&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&klt=1&fqt=1&beg=20260310&end=20260320'
try:
    r2 = requests.get(url2, timeout=10)
    data2 = r2.json()
    print('\n资金流向:')
    print(json.dumps(data2.get('data', {}), ensure_ascii=False, indent=2))
except Exception as e:
    print(f'资金流向Error: {e}')
