# -*- coding: utf-8 -*-
import urllib.request
import sys

stocks = {
    '亿能电力(bj920046)': 'bj920046',
    '浙江龙盛(sh600352)': 'sh600352',
    '航发动力(sh600893)': 'sh600893',
    '同花顺(sz300033)': 'sz300033',
    '西部矿业(sh601168)': 'sh601168',
    '普适导航(bj831330)': 'bj831330',
    '亨通光电(sh600487)': 'sh600487',
    '中复神鹰(sh688295)': 'sh688295',
    '圣博润(sz430046)': 'sz430046',
    '特变电工(sh600089)': 'sh600089',
    '东睦股份(sh600114)': 'sh600114',
    '南网数字(sz301638)': 'sz301638',
}

print('=== 持仓监控 15:30 ===')
print('')
for name, code in stocks.items():
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        raw = resp.read().decode('gbk')
        fields = raw.split('~')
        if len(fields) > 4:
            price = fields[3]
            pct = fields[32] if len(fields) > 32 else '0'
            try:
                pct_f = float(pct)
                arrow = '↑' if pct_f > 0 else '↓' if pct_f < 0 else '-'
                print(f'{name}: {price}元  {arrow}{abs(pct_f)}%')
            except:
                print(f'{name}: {price}元  {pct}%')
        else:
            print(f'{name}: 数据格式错误')
    except Exception as e:
        print(f'{name}: 查询失败-{e}')

print('')
print('止损提醒:')
stop_loss = {
    '亿能电力(bj920046)': 27.0,
    '浙江龙盛(sh600352)': 12.0,
    '航发动力(sh600893)': 42.0,
    '同花顺(sz300033)': 280.0,
    '西部矿业(sh601168)': 22.0,
    '普适导航(bj831330)': 18.0,
    '亨通光电(sh600487)': 38.0,
    '特变电工(sh600089)': 25.0,
    '东睦股份(sh600114)': 25.0,
    '南网数字(sz301638)': 28.0,
}
for name, sl in stop_loss.items():
    code = stocks.get(name, '')
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        raw = resp.read().decode('gbk')
        fields = raw.split('~')
        if len(fields) > 4:
            price = float(fields[3])
            if price <= sl:
                print(f'⚠️ {name} 现价{price}元 <= 止损{sl}元! 立即止损!')
            elif price <= sl * 1.03:
                print(f'🔶 {name} 现价{price}元 接近止损{sl}元')
            else:
                print(f'✅ {name} 现价{price}元 vs 止损{sl}元')
    except:
        pass
