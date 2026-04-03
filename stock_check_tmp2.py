#!/usr/bin/env python3
import urllib.request
import json

# 腾讯股票API
symbols_tc = [
    'sh600352', 'sh600893', 'sz300033', 'sh601168', 'bj831330',
    'sh600487', 'sh688295', 'sh430046', 'sh601318', 'sh601857'
]

url = 'https://qt.gtimg.cn/q=' + ','.join(symbols_tc)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk', errors='replace')
    lines = raw.strip().split('\n')
    
    for line in lines:
        parts = line.split('~')
        if len(parts) > 32:
            code = parts[2]  # sh600352
            name = parts[1]
            price = parts[3]
            yclose = parts[4]
            change_pct = parts[32] if len(parts) > 32 else 'N/A'
            volume = parts[6]  # 成交量（手）
            
            try:
                pct = float(change_pct)
            except:
                pct = 0
                
            print(f"{name}({code}) 现价:{price} 涨跌:{change_pct}% 成交量:{volume}手")
except Exception as e:
    print(f"错误: {e}")
