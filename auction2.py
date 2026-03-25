# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings('ignore')
import requests
import json

# ============ 指数行情（东方财富） ============
print("=== 指数行情 ===")
try:
    url = "http://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "fltt": 2,
        "invt": 2,
        "fields": "f12,f14,f3,f4,f2",
        "secids": "1.000001,0.399001,0.399006,1.000688,1.000300",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "cb": "jQuery"
    }
    r = requests.get(url, params=params, timeout=10)
    text = r.text
    # JSONP callback removal
    if text.startswith('jQuery'):
        text = text[text.index('(')+1:text.rindex(')')]
    data = json.loads(text)
    names = {"1.000001":"上证指数","0.399001":"深证成指","0.399006":"创业板指","1.000688":"科创50","1.000300":"沪深300"}
    for item in data.get("data",{}).get("diff",{}).values():
        code = item.get("f12","")
        secid = item.get("f12","")
        name = names.get(item.get("f12",""), item.get("f14",""))
        price = item.get("f2",0)
        chg = item.get("f3",0)
        print(f"{name}: {price} ({chg:+.2f}%)")
except Exception as e:
    print(f"指数: {e}")

# ============ 涨跌统计 ============
print("\n=== 涨跌统计 ===")
try:
    url2 = "http://push2.eastmoney.com/api/qt/stock/get"
    params2 = {
        "secid": "1.000001",
        "fields": "f57,f58,f60,f107,f162,f163,f168,f169",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
    }
    # 涨跌停数量用东财行情
    url3 = "http://push2.eastmoney.com/api/qt/clist/get"
    params3 = {
        "pn": 1, "pz": 1,
        "po": 1, "np": 1,
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": 2, "invt": 2,
        "fid": "f3",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23",
        "fields": "f12,f14,f3,f4",
    }
    r3 = requests.get(url3, params=params3, timeout=10)
    d3 = r3.json()
    total = d3.get("data",{}).get("total",0)
    # 涨停数
    params_zt = dict(params3)
    params_zt["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.gt=9.9"
    r_zt = requests.get(url3, params=params_zt, timeout=10)
    zt_count = r_zt.json().get("data",{}).get("total",0)
    params_dt = dict(params3)
    params_dt["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.lt=-9.9"
    r_dt = requests.get(url3, params=params_dt, timeout=10)
    dt_count = r_dt.json().get("data",{}).get("total",0)
    print(f"涨停: {zt_count}  跌停: {dt_count}  总A股(估算): {total}")
except Exception as e:
    print(f"涨跌停: {e}")

# ============ 持仓个股 ============
print("\n=== 持仓个股 ===")
stocks = [
    ("浙江龙盛", "600352"),
    ("同花顺", "300033"),
    ("华工科技", "000988"),
    ("中复神鹰", "688295"),
    ("亨通光电", "600487"),
    ("高澜股份", "300499"),
    ("西部矿业", "601168"),
    ("航发动力", "600893"),
    ("亿能电力", "920046"),
    ("东睦股份", "600114"),
    ("南网数字", "301638"),
]
codes_with_market = []
for name, code in stocks:
    if code.startswith("6"):
        codes_with_market.append(("1."+code, name, code))
    else:
        codes_with_market.append(("0."+code, name, code))

secids = ",".join([s[0] for s in codes_with_market])
try:
    url4 = "http://push2.eastmoney.com/api/qt/ulist.np/get"
    params4 = {
        "fltt": 2, "invt": 2,
        "fields": "f12,f14,f2,f3,f4,f5,f6,f15,f16,f17,f18",
        "secids": secids,
        "ut": "b2884a393a59ad64002292a3e90d46a5",
    }
    r4 = requests.get(url4, params=params4, timeout=10)
    d4 = r4.json()
    items = d4.get("data",{}).get("diff",{})
    for secid, item in items.items():
        name = item.get("f14","")
        price = item.get("f2",0)
        chg = item.get("f3",0)
        vol = item.get("f5",0)
        amount = item.get("f6",0)
        high = item.get("f15",0)
        low = item.get("f16",0)
        open_p = item.get("f17",0)
        prev_close = item.get("f18",0)
        
        # 判断竞价方向
        direction = ""
        if open_p > 0 and prev_close > 0:
            if open_p > prev_close:
                direction = "高开"
            elif open_p < prev_close:
                direction = "低开"
            else:
                direction = "平开"
        
        vol_str = ""
        if vol > 1e6:
            vol_str = f"{vol/1e6:.1f}万手"
        elif vol > 1e3:
            vol_str = f"{vol/1e3:.0f}百手"
        
        if amount > 1e8:
            amount_str = f"{amount/1e8:.2f}亿"
        elif amount > 1e4:
            amount_str = f"{amount/1e4:.0f}万"
        else:
            amount_str = f"{amount:.0f}"
        
        print(f"{name}({item.get('f12','')}): 现价{price} ({chg:+.2f}%) 开:{open_p} {direction} 量:{vol_str} 额:{amount_str} 高:{high} 低:{low}")
except Exception as e:
    print(f"持仓数据: {e}")
    import traceback
    traceback.print_exc()
