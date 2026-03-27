# -*- coding: utf-8 -*-
import urllib.request
import sys

# Sina Finance real-time quotes - use correct format
# Shanghai: shXXXXXX, Shenzhen: szXXXXXX, Beijing: bjXXXXXX
codes = [
    'sh600352',  # 浙江龙盛
    'sh600893',  # 航发动力
    'sz300033',  # 同花顺
    'sh601168',  # 西部矿业
    'bj831330',  # 普适导航
    'sh600487',  # 亨通光电
    'sh688295',  # 中复神鹰
    'bj920046',  # 亿能电力
    'bj430046',  # 圣博润
]

url = 'https://hq.sinajs.cn/list=' + ','.join(codes)

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://finance.sina.com.cn',
})

try:
    resp = urllib.request.urlopen(req, timeout=15)
    raw = resp.read()
    # Try gbk first, fallback to utf-8
    try:
        content = raw.decode('gbk')
    except:
        content = raw.decode('utf-8', errors='replace')
    
    # Parse each line
    for line in content.strip().split('\n'):
        if '=' not in line:
            continue
        var = line.split('=')[0].replace('hq_str_', '').replace('"', '').strip()
        data = line.split('"')[1] if '"' in line else ''
        fields = data.split(',')
        if len(fields) < 10:
            continue
        
        code = var[2:] if var.startswith(('sh','sz','bj')) else var
        name = fields[0]
        prev_close = fields[2]
        price = fields[3]
        try:
            chg_pct = (float(price) - float(prev_close)) / float(prev_close) * 100
            print(f"{name}|{code}|{price}|{chg_pct:+.2f}%")
        except:
            print(f"{name}|{code}|{price}|N/A")
            
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
