#!/usr/bin/env python3
import urllib.request
import json
import re

url = 'https://hq.sinajs.cn/list=sh600352,sh600893,sz300033,sh601168,bj831330,sh600487,sh688295,bx430046,sh601318,sh601857'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn'
})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk', errors='replace')
    
    # Parse each line: var hq_str_sh600352="..."
    pattern = r'hq_str_(\w+)="([^"]*)"'
    matches = re.findall(pattern, raw)
    
    results = {}
    for code, data in matches:
        fields = data.split(',')
        if len(fields) < 10:
            results[code] = {'error': 'no data', 'raw': data[:50]}
            continue
        try:
            results[code] = {
                'name': fields[0],
                'open': float(fields[1]),
                'yclose': float(fields[2]),
                'price': float(fields[3]),
                'high': float(fields[4]),
                'low': float(fields[5]),
                'change_pct': round((float(fields[3]) - float(fields[2])) / float(fields[2]) * 100, 2)
            }
        except Exception as e:
            results[code] = {'error': str(e), 'fields_count': len(fields)}
    
    with open('C:/Users/Administrator/.openclaw/workspace/stock_check_output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("done")
except Exception as e:
    print(f"Error: {e}")
