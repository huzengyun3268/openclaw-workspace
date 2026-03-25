# -*- coding: utf-8 -*-
import urllib.request

def get_data(codes):
    url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk')
    return raw

outfile = r'C:\Users\Administrator\.openclaw\workspace\debug_out.txt'
sdata = get_data(['sh600352'])
for line in sdata.strip().split(';'):
    if '=' not in line:
        continue
    content = line.split('=',1)[1].strip().strip('"').strip(';')
    fields = content.split('~')
    lines = []
    for i, f in enumerate(fields[:40]):
        lines.append(f'{i}: {f}')
    with open(outfile, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    print("debug written")
