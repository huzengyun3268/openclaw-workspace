# -*- coding: utf-8 -*-
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 用腾讯股票接口测试
codes = ['sh600352', 'sz300033', 'sz000988', 'sh600487']

for code in codes:
    url = f"https://qt.gtimg.cn/q={code}"
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://gu.qq.com'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.encoding = 'gbk'
        text = r.text.strip()
        parts = text.split('~')
        if len(parts) > 40:
            name = parts[1]
            price = parts[3]
            close_p = parts[4]
            open_p = parts[5]
            high = parts[33]
            low = parts[34]
            pct = parts[32]
            vol = parts[36]
            print(f"{name}: 现价={price} 昨收={close_p} 今开={open_p} 涨幅={pct}% 最高={high} 最低={low}")
        else:
            print(f"{code}: 数据异常")
    except Exception as e:
        print(f"{code}: 失败 {e}")
