import requests
import json

codes = ['sh600352', 'sz300033', 'sh600487', 'sh600893', 'sh601168', 'sh518880', 'sz430046', 'sh600114', 'sh600089']
names = {'sh600352':'浙江龙盛','sz300033':'同花顺','sh600487':'亨通光电','sh600893':'航发动力','sh601168':'西部矿业','sh518880':'黄金ETF','sz430046':'圣博润','sh600114':'东睦股份','sh600089':'特变电工'}

print('=== 持仓监控 09:30 ===')
for code in codes:
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        r = requests.get(url, timeout=5)
        content = r.text
        # 格式: v_sh600352="...name~price~chg~chg_pct..."
        parts = content.split('~')
        if len(parts) > 10:
            price = float(parts[3])
            chg = float(parts[31]) if parts[31] else 0
            chg_pct = float(parts[32]) if parts[32] else 0
            name = names.get(code, parts[1])
            arrow = '↑' if chg_pct > 0 else '↓' if chg_pct < 0 else '-'
            print(f"{name}({code}) {price:.3f} {arrow}{abs(chg_pct):.2f}%")
        else:
            print(f"{code} 数据解析失败")
    except Exception as e:
        print(f"{code} 错误: {e}")
