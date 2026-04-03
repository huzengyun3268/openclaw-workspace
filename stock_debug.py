import requests
import time

codes = [
    ('sh600352', '浙江龙盛'),
    ('sz300033', '同花顺'),
    ('sh600487', '亨通光电'),
    ('sh600893', '航发动力'),
    ('sh601168', '西部矿业'),
    ('sh518880', '黄金ETF'),
    ('sz430046', '圣博润'),
    ('sh600114', '东睦(老婆)'),
    ('sh600089', '特变(两融)'),
]

code_str = ','.join([c for c, _ in codes])
url = f'http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids={code_str}'

try:
    resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    print('Status:', resp.status_code)
    print('Response:', resp.text[:500])
except Exception as e:
    print(f'错误: {e}')
