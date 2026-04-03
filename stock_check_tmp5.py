#!/usr/bin/env python3
import urllib.request
import json
import sys

url = 'https://hq.sinajs.cn/list=sh600352,sh600893,sz300033,sh601168,bj831330,sh600487,sh688295,bx430046,sh601318,sh601857'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn'
})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk', errors='replace')
    lines = raw.strip().split('\n')
    
    results = {}
    for line in lines:
        if '=' not in line:
            continue
        code = line.split('_')[1].split('=')[0]
        parts = line.split('"')
        if len(parts) < 2:
            continue
        fields = parts[1].split(',')
        if len(fields) < 10:
            results[code] = {'error': 'no data'}
            continue
        try:
            name = fields[0]
            price = float(fields[3])
            yclose = float(fields[2])
            change_pct = round((price - yclose) / yclose * 100, 2)
            results[code] = {
                'name': name,
                'price': price,
                'change_pct': change_pct,
                'yclose': yclose
            }
        except Exception as e:
            results[code] = {'error': str(e)}
    
    with open('C:/Users/Administrator/.openclaw/workspace/stock_check_output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("done")
except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)
