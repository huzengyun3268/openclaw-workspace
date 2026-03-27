# -*- coding: utf-8 -*-
import urllib.request

codes = ['sh600352', 'sh600893', 'sz300033', 'sh601168', 'bj831330', 'sh600487', 'sh688295', 'bj920046', 'bj430046']
url = 'https://hq.sinajs.cn/list=' + ','.join(codes)

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn',
})

results = {}
try:
    resp = urllib.request.urlopen(req, timeout=15)
    raw = resp.read()
    content = raw.decode('gbk', errors='replace')
    
    for line in content.strip().split('\n'):
        print(f"LINE: {line[:200]}")
        if '=' not in line:
            continue
        var = line.split('=')[0].replace('hq_str_', '').strip()
        print(f"VAR: {var}")
        try:
            idx1 = line.index('"')
            idx2 = line.index('"', idx1+1)
            data = line[idx1+1:idx2]
        except:
            print("  PARSE ERROR")
            continue
        fields = data.split(',')
        print(f"  fields count: {len(fields)}, fields[0]={fields[0]}, [1]={fields[1]}, [3]={fields[3] if len(fields)>3 else 'N/A'}")
        if len(fields) >= 6:
            price = float(fields[3])
            prev_close = float(fields[1])
            chg = (price - prev_close) / prev_close * 100
            results[var] = {'price': price, 'chg': chg}
            print(f"  -> price={price}, chg={chg:.2f}%")
except Exception as e:
    print(f"Error: {e}")

print("\n=== RESULTS ===")
for k, v in results.items():
    print(f"{k}: {v}")
