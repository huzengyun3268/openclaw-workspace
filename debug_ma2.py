import urllib.request, re, sys, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'

def check_stock(code_market):
    try:
        url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code_market},day,,,40,qfq'
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://gu.qq.com'})
        r = urllib.request.urlopen(req, timeout=8)
        txt = r.read().decode('utf-8')
        print(f'Raw response length: {len(txt)}')
        print(f'First 300 chars: {txt[:300]}')
        
        idx = txt.find('qfqday')
        print(f'qfqday index: {idx}')
        if idx < 0:
            # Try without qfqday
            idx2 = txt.find('day')
            print(f' day index: {idx2}')
            if idx2 >= 0:
                start = txt.find('[', idx2)
                end = txt.find(']]', start)
                print(f'Found data at [{start}:{end}], length: {end-start}')
    except Exception as e:
        print(f'Error: {e}')

# Test with several stocks
for code in ['sh600519', 'sh600249', 'sz300461', 'sh688428', 'sz301130']:
    print(f'\n=== {code} ===')
    check_stock(code)
