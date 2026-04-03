import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Try sina finance API for OTC stocks
codes = [('普适导航', 'bj831330'), ('圣博润', 'sz430046')]
for name, code in codes:
    try:
        url = f'http://hq.sinajs.cn/list={code}'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://finance.sina.com.cn'
        })
        with urllib.request.urlopen(req, timeout=8) as r:
            data = r.read().decode('gbk')
            # format: var hq_str_bj831330="name,price,change,pct,..."
            start = data.find('"') + 1
            end = data.find('"', start)
            fields = data[start:end].split(',')
            if len(fields) > 4:
                price = float(fields[1])
                pct = float(fields[3]) if fields[3] else 0.0
                print(f'{name}({code}): {price:.3f} ({pct:+.2f}%)')
            else:
                print(f'{name}({code}): DATA ERROR {fields}')
    except Exception as e:
        print(f'{name}: ERROR {e}')
