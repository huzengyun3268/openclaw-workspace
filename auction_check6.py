# -*- coding: utf-8 -*-
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 持仓股票
codes = [
    ('sh600352', '浙江龙盛', 15.952, 12.0),
    ('sz300033', '同花顺', 423.488, 280.0),
    ('bz920046', '亿能电力', 329.555, 27.0),
    ('sz000988', '华工科技', 116.87, 0.0),
    ('sh688295', '中复神鹰', 37.843, 0.0),
    ('sh600487', '亨通光电', 42.391, 0.0),
    ('sz300499', '高澜股份', 41.625, 38.0),
    ('sh601168', '西部矿业', 24.863, 0.0),
    ('sh600893', '航发动力', 47.196, 0.0),
]

results = []
for code, name, cost, stop_loss in codes:
    url = f"https://qt.gtimg.cn/q={code}"
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://gu.qq.com'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.encoding = 'gbk'
        text = r.text.strip()
        parts = text.split('~')
        if len(parts) > 40:
            price_str = parts[3]
            close_str = parts[4]
            open_str = parts[5]
            high_str = parts[33]
            low_str = parts[34]
            pct_str = parts[32]
            
            try:
                price = float(price_str)
                close = float(close_str)
                open_p = float(open_str)
                high = float(high_str)
                low = float(low_str)
                pct = float(pct_str)
                
                if price == 0:
                    status = "【停牌/无数据】"
                else:
                    profit = round((price - cost) * 10000, 0) / 10000  # 每手盈亏
                    profit_pct = round((price - cost) / cost * 100, 2)
                    
                    # 判断状态
                    if pct <= -9.5:
                        status = "【跌停竞价】⚠️"
                    elif pct >= 9.5:
                        status = "【涨停竞价】🔥"
                    elif pct > 3:
                        status = "【大幅高开】"
                    elif pct < -3:
                        status = "【大幅低开】⚠️"
                    elif pct > 0:
                        status = "【高开】"
                    elif pct < 0:
                        status = "【低开】"
                    else:
                        status = "【平开】"
                    
                    results.append(f"{name}({code}): 现价={price} 涨幅={pct}% {status} 成本={cost} 浮盈亏={profit:.2f}({profit_pct}%)")
                    if stop_loss > 0 and price < stop_loss:
                        results.append(f"  ⚠️ 【止损警告】现价{price} < 止损{stop_loss}")
            except Exception as e:
                results.append(f"{name}: 数据解析异常: {e}")
        else:
            results.append(f"{name}: 数据格式异常")
    except Exception as e:
        results.append(f"{name}: 获取失败: {e}")

print("=== 集合竞价监控 09:17 ===")
for r in results:
    print(r)
