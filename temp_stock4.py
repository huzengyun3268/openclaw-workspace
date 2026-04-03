import urllib.request, json

url = 'https://qt.gtimg.cn/q=sh600352,sh600893,sz300033,sh601168,bj831330,sh600487,sh688295,sz430046,sh600114,sh600089'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    raw = r.read()

# Try gbk decode
html = raw.decode('gbk', 'ignore')

# Parse: v_sh600352="1~name~code~price~...
pm = {}
for line in html.strip().split('\n'):
    if '=' in line:
        key_val = line.split('=', 1)
        code_with_prefix = key_val[0].replace('v_', '')
        fields = key_val[1].strip('"').split('~')
        if len(fields) >= 4:
            code = fields[1]
            try:
                price = float(fields[3])
                if code and price > 0:
                    pm[code] = price
            except:
                pass

# Write result to file
with open('C:\\Users\\Administrator\\.openclaw\\workspace\\stock_prices.json', 'w', encoding='utf-8') as f:
    json.dump(pm, f, ensure_ascii=False)

print('DONE: ' + str(len(pm)) + ' stocks')
