import urllib.request
import json

stocks = {
    "浙江龙盛": "sh600352",
    "航发动力": "sh600893",
    "同花顺": "sz300033",
    "西部矿业": "sh601168",
    "普适导航": "bj831330",
    "亨通光电": "sh600487",
    "中复神鹰": "sh688295",
    "圣博润": "sz430046",
}

for name, code in stocks.items():
    url = f"https://qt.gtimg.cn/q={code}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 32:
                price = parts[3]
                change = parts[31]
                pct = parts[32]
                print(f"{name}({code[-6:]}): {price} 涨跌额:{change} 涨跌幅:{pct}%")
    except Exception as e:
        print(f"{name}: 获取失败 {e}")
