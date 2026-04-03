import urllib.request
import re

url = 'https://qt.gtimg.cn/q=sh600352,sh600893,sz300033,sh601168,bj831330,sh600487,sh688295,sz430046,sh600114,sh600089'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('gbk', 'ignore')

pm = {}
for line in html.split('\n'):
    parts = line.split('~')
    if len(parts) >= 4:
        try:
            code_raw = parts[1]
            price = float(parts[3])
            if code_raw and price > 0 and len(code_raw) == 6:
                pm[code_raw] = price
        except:
            pass

print(str(pm))
