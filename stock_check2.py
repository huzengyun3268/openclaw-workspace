# -*- coding: utf-8 -*-
import requests

stocks = ['600352', '600089', '301667', '920046', '300033', '831330', '300189', '430046']
names = ['浙江龙盛', '特变电工', '纳百川', '亿能电力', '同花顺', '普适导航', '神农种业', '圣博润']
shares = [106700, 52300, 3000, 12731, 600, 6370, 5000, 10334]
costs = [15.91, 24.765, 82.715, 35.936, 511.22, 20.415, 17.099, 0.478]

fs_codes = []
for c in stocks:
    if c.startswith('6'):
        fs_codes.append('sh' + c)
    elif c.startswith('9'):
        fs_codes.append('bj' + c)
    else:
        fs_codes.append('sz' + c)

url = 'https://hq.sinajs.cn/list=' + ','.join(fs_codes)
headers = {'Referer': 'https://finance.sina.com.cn'}
try:
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'gbk'
    lines = r.text.strip().split('\n')
    print('=== 持仓监控 2026-03-24 14:30 ===')
    total_m = 0.0
    total_c = 0.0
    total_p = 0.0
    for i, line in enumerate(lines):
        parts = line.split('=')
        if len(parts) < 2:
            print(names[i] + '(' + stocks[i] + '): 数据获取失败')
            continue
        data = parts[1].strip('";\n\r ')
        fields = data.split(',')
        if len(fields) > 4:
            price = float(fields[3])
            prev = float(fields[2])
            chg = (price - prev) / prev * 100
            cost = costs[i]
            m = price * shares[i]
            p = (price - cost) * shares[i]
            pct = (price - cost) / cost * 100
            sign_c = '+' if chg >= 0 else ''
            sign_p = '+' if p >= 0 else ''
            msg = '%s(%s): 现价=%.3f 涨跌=%s%.2f%% | 市值=%.0f 盈亏=%s%.0f(%s%.1f%%)' % (
                names[i], stocks[i], price, sign_c, chg, m, sign_p, p, sign_p, pct)
            print(msg)
            total_m += m
            total_c += cost * shares[i]
            total_p += p
        else:
            print(names[i] + '(' + stocks[i] + '): 数据不完整 ' + data)
    sign_tp = '+' if total_p >= 0 else ''
    total_pct = total_p / total_c * 100
    sign_tpp = '+' if total_pct >= 0 else ''
    print('\n--- 合计 ---')
    msg2 = '总市值: %.0f | 总成本: %.0f | 总盈亏: %s%.0f(%s%.1f%%)' % (
        total_m, total_c, sign_tp, total_p, sign_tpp, total_pct)
    print(msg2)
except Exception as e:
    print('获取失败: ' + str(e))
