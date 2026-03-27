# -*- coding: utf-8 -*-
import urllib.request

codes = 'sh600352,sh600893,sz300033,sh601168,bj831330,sh600487,sh688295,bj920046,bj430046'
url = f'https://hq.sinajs.cn/list={codes}'

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn',
})

try:
    resp = urllib.request.urlopen(req, timeout=15)
    raw = resp.read()
    content = raw.decode('gbk', errors='replace')
    # Save raw response
    with open('C:/Users/Administrator/.openclaw/workspace/stock_raw.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Got {len(content)} bytes")
    for line in content.strip().split('\n')[:3]:
        print(line[:150])
except Exception as e:
    print(f"Error: {e}")
