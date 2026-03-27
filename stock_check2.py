# -*- coding: utf-8 -*-
import subprocess
import json

stocks = [
    {"code": "600352", "name": "\u6d59\u6c5f\u9f99\u76db", "secid": "1.600352", "cost": 16.52, "stop": 12.0, "pos": 86700},
    {"code": "600893", "name": "\u822a\u53d1\u52a8\u529b", "secid": "1.600893", "cost": 49.184, "stop": 42.0, "pos": 9000},
    {"code": "300033", "name": "\u540c\u82b1\u987a", "secid": "0.300033", "cost": 423.488, "stop": 280, "pos": 1200},
    {"code": "601168", "name": "\u897f\u90e8\u77ff\u4e1a", "secid": "1.601168", "cost": 26.169, "stop": 22.0, "pos": 11000},
    {"code": "831330", "name": "\u666e\u9002\u5bfc\u822a", "secid": "0.831330", "cost": 20.361, "stop": 18.0, "pos": 7370},
    {"code": "600487", "name": "\u4ea8\u901a\u5149\u7535", "secid": "1.600487", "cost": 43.998, "stop": 38.0, "pos": 3000},
    {"code": "688295", "name": "\u4e2d\u590d\u795e\u9e70", "secid": "1.688295", "cost": 37.843, "stop": None, "pos": 1500},
    {"code": "920046", "name": "\u4ebf\u80fd\u7535\u529b", "secid": "0.920046", "cost": 329.553, "stop": None, "pos": 200},
    {"code": "430046", "name": "\u5723\u5e1d\u6da6", "secid": "0.430046", "cost": 0.478, "stop": None, "pos": 10334},
    {"code": "600114", "name": "\u4e1c\u589f\u80a1\u4efd", "secid": "1.600114", "cost": 26.0, "stop": 25.0, "pos": 4900},
    {"code": "301638", "name": "\u5357\u7f51\u6570\u5b57", "secid": "0.301638", "cost": 32.64, "stop": 28.0, "pos": 1700},
    {"code": "600089", "name": "\u7279\u53d8\u7535\u5de5", "secid": "1.600089", "cost": 24.765, "stop": 25.0, "pos": 52300},
]

alerts = []
total_pnl = 0

print("\u2705 \u6301\u4ed3\u76d1\u63a7 2026-03-27 13:45")
print("-" * 75)
print(f"{'\u80a1\u7968':<8} {'\u540d\u79f0':<10} {'\u6700\u65b0\u4ef7':>8} {'\u6da8\u8dcc\u5e45':>8} {'\u6210\u672c':>8} {'\u6b62\u635f':>6} {'\u76c8\u4e8f':>10} {'\u72b6\u6001'}")
print("-" * 75)

for s in stocks:
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={s['secid']}&fields=f43,f170,f57,f58"
    try:
        result = subprocess.run(
            ["powershell", "-Command", 
             f"Invoke-RestMethod -Uri '{url}' -Headers @{{'Referer'='https://finance.eastmoney.com'}} -TimeoutSec 10 | ConvertTo-Json -Compress"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if data.get("data"):
                price = data["data"]["f43"] / 100
                chg_pct = data["data"]["f170"] / 100
                pnl = (price - s["cost"]) * s["pos"]
                total_pnl += pnl
                
                status = "OK"
                alert = None
                if s["stop"] and price <= s["stop"]:
                    status = "\u6b62\u635f!"
                    alert = f"\u26a0\ufe0f {s['name']} \u73b0\u4ef7{price:.3f} <= \u6b62\u635f{s['stop']}"
                elif s["stop"] and price <= s["stop"] * 1.05:
                    status = "\u8b66\u620f"
                
                stop_str = f"{s['stop']}" if s["stop"] else "-"
                print(f"{s['code']:<8} {s['name']:<10} {price:>8.3f} {chg_pct:>+7.2f}% {s['cost']:>8.3f} {stop_str:>6} {pnl:>+10.1f} {status}")
                
                if alert:
                    alerts.append(alert)
            else:
                print(f"{s['code']:<8} {s['name']:<10} [\u65e0\u6570\u636e]")
        else:
            print(f"{s['code']:<8} {s['name']:<10} [\u8bf7\u6c42\u5931\u8d25]")
    except Exception as e:
        print(f"{s['code']:<8} {s['name']:<10} [\u9519\u8bef: {str(e)[:20]}]")

print("-" * 75)
print(f"\u6291\u4ed3\u8d44\u4ea7\u6d6e\u52a8\u76c8\u4e8f\u5408\u8ba1: {total_pnl:+.1f} \u5143")

if alerts:
    print("\n\ud83d\udea8 \u6b62\u635f\u8b66\u62a5:")
    for a in alerts:
        print(f"  {a}")
else:
    print("\n\ud83d\udfe2 \u6682\u65e0\u6b62\u635f\u8b66\u62a5")
