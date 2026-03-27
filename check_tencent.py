# -*- coding: utf-8 -*-
import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

# 腾讯行情接口
# sh=沪市, sz=深市, bj=北交所
codes = [
    ('bj920046', '亿能电力', 27.0, 329.553, 200),
    ('bj430046', '圣博润', 0, 0.478, 10334),
]

for tcode, name, stoploss, cost, qty in codes:
    try:
        url = 'http://qt.gtimg.cn/q=' + tcode
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://gu.qq.com',
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('gbk', errors='replace')
            parts = content.split('~')
            if len(parts) > 10:
                price = float(parts[3]) if parts[3] else 0
                pct = float(parts[32]) if parts[32] else 0
                pnl = (price - cost) * qty
                flag = ''
                if stoploss > 0 and price < stoploss:
                    flag = '[!!STOP!!]'
                elif stoploss > 0 and price < stoploss * 1.05:
                    flag = '[!NEAR]'
                print('[OK] %s %s: %.3f %+.2f%% PnL %+.0f %s' % (name, tcode, price, pct, pnl, flag))
            else:
                print('[X] %s: bad data: %s' % (name, content[:100]))
    except Exception as e:
        print('[X] %s: %s' % (name, str(e)[:100]))
