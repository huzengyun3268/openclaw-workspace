# -*- coding: utf-8 -*-
import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 用新浪财经接口
codes = ['sh600352', 'sz300033', 'sz000988', 'sh688295', 'sh600487', 'sz300499', 'sh601168', 'sh600893', 'bj920046']

results = []
for sina_code in codes:
    url = f"http://hq.sinajs.cn/list={sina_code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://finance.sina.com.cn/'
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.encoding = 'gbk'
        text = r.text.strip()
        content = text.split('"')[1] if '"' in text else ''
        if content and len(content.split(',')) >= 10:
            parts = content.split(',')
            name = parts[0]
            open_p = parts[1]
            close_p = parts[2]
            price = parts[3]
            high = parts[4]
            low = parts[5]
            
            # 判断是否停牌
            try:
                price_f = float(price) if price else 0
                close_f = float(close_p) if close_p else 1
                if price_f == 0:
                    status = "【停牌】"
                else:
                    pct = round((price_f - close_f) / close_f * 100, 2)
                    change = round(price_f - close_f, 2)
                    status = f"涨跌={change}({pct}%)"
            except:
                status = "数据异常"
            
            results.append(f"{name}: 现价={price} 今开={open_p} {status} 最高={high} 最低={low}")
        else:
            results.append(f"{sina_code}: 无数据")
    except Exception as e:
        results.append(f"{sina_code}: 失败 {e}")

print("=== 集合竞价监控 09:17 ===")
for r in results:
    print(r)
