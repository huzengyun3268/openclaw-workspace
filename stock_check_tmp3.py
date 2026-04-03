#!/usr/bin/env python3
import urllib.request
import json

# 用东方财富的实时行情接口
symbols = ['600352', '600893', '300033', '601168', '831330', '600487', '688295', '430046', '601318', '601857']
codes = ','.join([f'1.{s}' for s in symbols])
url = f'http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&secid=1.600352&fields=f2,f3,f4,f12,f14&cb=callback'
# 用新浪的接口
url2 = 'https://hq.sinajs.cn/list=sh600352,sh600893,sz300033,sh601168,bj831330,sh600487,sh688295,bz430046,sh601318,sh601857'
req = urllib.request.Request(url2, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.sina.com.cn'
})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk', errors='replace')
    print(raw[:5000])
except Exception as e:
    print(f"错误: {e}")
