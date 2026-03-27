# -*- coding: utf-8 -*-
import urllib.request
import sys

codes = [
    ('sh600352', '浙江龙盛'),
    ('sh600893', '航发动力'),
    ('sz300033', '同花顺'),
    ('sh601168', '西部矿业'),
    ('bj831330', '普适导航'),
    ('sh600487', '亨通光电'),
    ('sh688295', '中复神鹰'),
    ('bj920046', '亿能电力'),
    ('bj430046', '圣博润'),
]

url = 'https://hq.sinajs.cn/list=' + ','.join([c[0] for c in codes])

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://finance.sina.com.cn',
})

try:
    resp = urllib.request.urlopen(req, timeout=15)
    raw = resp.read()
    try:
        content = raw.decode('gbk')
    except:
        content = raw.decode('utf-8', errors='replace')
    
    # Debug: print raw lines
    for line in content.strip().split('\n'):
        print(repr(line[:100]), file=sys.stderr)
        if '=' not in line:
            continue
        var_part = line.split('=')[0]
        data_part = line[line.find('"')+1:line.rfind('"')]
        fields = data_part.split(',')
        print(f"  fields count: {len(fields)}", file=sys.stderr)
        if len(fields) > 3:
            print(f"{fields[0]}|{fields[3]}|{fields[2]}")
            
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
