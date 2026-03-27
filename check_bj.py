# -*- coding: utf-8 -*-
import urllib.request, json, ssl, sys
sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

codes = [('920046','亿能电力'), ('430046','圣博润')]

for code, name in codes:
    try:
        # Try 北交所
        url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.%s&fields=f43,f169,f170,f57,f58' % code
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://quote.eastmoney.com/',
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            raw = r.read()
            if raw[:3] == b'\x00\x00\x00' or raw[:4] == b'\x00\x00\x00\x00':
                data = json.loads(raw[4:].decode('utf-8'))
            else:
                data = json.loads(raw.decode('utf-8'))
            if data.get('data'):
                d = data['data']
                price = float(d.get('f43', 0)) / 100 if d.get('f43') else 0
                pct = float(d.get('f170', 0)) / 100 if d.get('f170') else 0
                print('[OK] %s %s: %.3f %+.2f%%' % (name, code, price, pct))
            else:
                print('[X] %s %s: no data' % (name, code))
        # Try 新三板
        try:
            url2 = 'http://push2.eastmoney.com/api/qt/stock/get?secid=0.%s&fields=f43,f169,f170,f57,f58' % code
            req2 = urllib.request.Request(url2, headers={
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'http://quote.eastmoney.com/',
            })
            with urllib.request.urlopen(req2, timeout=10) as r2:
                raw2 = r2.read()
                if raw2:
                    print('  Raw (HTTP):', raw2[:200])
        except:
            pass
    except Exception as e:
        print('[X] %s %s: %s' % (name, code, str(e)[:100]))
