import urllib.request
import json
import re

codes = ['sh600352', 'sz300033', 'bj831330', 'sz000988', 'sh688295', 
         'sh600487', 'sz300499', 'sh601168', 'sh600893', 'bj920046', 
         'bj430046', 'sh600114', 'sz301638', 'sh600089']

names = {
    'sh600352': '浙江龙盛', 'sz300033': '同花顺', 'bj831330': '普适导航', 'sz000988': '华工科技',
    'sh688295': '中复神鹰', 'sh600487': '亨通光电', 'sz300499': '高澜股份', 'sh601168': '西部矿业',
    'sh600893': '航发动力', 'bj920046': '亿能电力', 'bj430046': '圣博润', 'sh600114': '东睦股份',
    'sz301638': '南网数字', 'sh600089': '特变电工',
}

code_str = ','.join(codes)
url = f'https://qt.gtimg.cn/q={code_str}'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode('gbk')
    
    results = []
    lines = content.strip().split('\n')
    for line in lines:
        if 'pvtsugq' in line or 'v_qihuo' in line:
            continue
        m = re.search(r'="([^"]+)"', line)
        if m:
            fields = m.group(1).split('~')
            if len(fields) > 32:
                code_raw = fields[0]  # e.g. sh600352
                name = names.get(code_raw, fields[1])
                price = fields[3]
                chg_pct = fields[32]
                amount = fields[37]  # 成交额万元
                chg_val = fields[31]
                results.append(f'{name}: {price} ({chg_pct}%) 成交额:{amount}万')
    
    print(json.dumps(results, ensure_ascii=False))
except Exception as e:
    print(f'Error: {e}')
