import requests
import json
import time

stocks = [
    ('sh600352', '浙江龙盛'),
    ('sh600893', '航发动力'),
    ('sz300033', '同花顺'),
    ('sh601168', '西部矿业'),
    ('sh600487', '亨通光电'),
    ('sh688295', '中复神鹰'),
    ('sh600114', '东睦股份'),
    ('sz301638', '南网数字'),
    ('sh600089', '特变电工'),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
}

# 腾讯财经API
for code, name in stocks:
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        resp = requests.get(url, headers=headers, timeout=8)
        text = resp.text.strip()
        parts = text.split('~')
        if len(parts) > 4 and parts[1] != '':
            price = float(parts[3]) if parts[3] else 0
            chg_pct = float(parts[32]) if len(parts) > 32 and parts[32] else 0
            print(f'{name}({code}): {price:.2f} ({chg_pct:+.2f}%)')
        else:
            print(f'{name}({code}): 无数据 - {text[:80]}')
    except Exception as e:
        print(f'{name}({code}): 失败 - {e}')
    time.sleep(0.5)

# 尝试东方财富API作为备选
print('\n=== 东方财富API ===')
stocks2 = [
    ('1.600352', '浙江龙盛'),
    ('1.600893', '航发动力'),
    ('0.300033', '同花顺'),
    ('1.601168', '西部矿业'),
    ('1.600487', '亨通光电'),
    ('1.688295', '中复神鹰'),
    ('1.600114', '东睦股份'),
    ('0.301638', '南网数字'),
    ('1.600089', '特变电工'),
]
for secid, name in stocks2:
    try:
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f169,f170,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b'
        resp = requests.get(url, headers=headers, timeout=8)
        data = resp.json()
        if data.get('data'):
            d = data['data']
            price = (d.get('f43', 0)) / 100
            chg = (d.get('f169', 0)) / 100
            chg_pct = (d.get('f170', 0)) / 100
            print(f'{name}({secid}): {price:.2f} ({chg_pct:+.2f}%)')
        else:
            print(f'{name}({secid}): 无数据')
    except Exception as e:
        print(f'{name}({secid}): 失败 - {e}')
    time.sleep(0.5)
