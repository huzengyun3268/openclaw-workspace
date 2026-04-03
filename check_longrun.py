import urllib.request, re

try:
    url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param=sh600352,day,2026-02-01,2026-04-01,100,qfq'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://gu.qq.com'})
    r = urllib.request.urlopen(req, timeout=10)
    txt = r.read().decode('utf-8')
    
    idx = txt.find('qfqday')
    if idx >= 0:
        start = txt.find('[', idx)
        # Find the closing bracket - look for ]] at the end
        end = txt.find(']]', start)
        raw = txt[start:end+1]
        items = re.findall(r'\["([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)"\]', raw)
        print(f"共 {len(items)} 条数据")
        print(f"{'日期':<12} {'开':<7} {'收':<7} {'高':<7} {'低':<7} {'成交量(万)':<10} {'涨跌%'}")
        for it in items[-15:]:
            date, o, c, h, low, vol = it
            vol_w = int(float(vol))/10000
            chg_pct = (float(c)-float(o))/float(o)*100
            vol_scale = '极高' if vol_w > 500 else ('高' if vol_w > 300 else '平' if vol_w > 150 else '缩')
            print(f"{date:<12} {float(o):<7.2f} {float(c):<7.2f} {float(h):<7.2f} {float(low):<7.2f} {vol_w:<10.0f} {chg_pct:>+5.2f}% {vol_scale}")
    else:
        print("未找到qfqday数据")
except Exception as e:
    print(f"失败: {e}")
    import traceback; traceback.print_exc()
