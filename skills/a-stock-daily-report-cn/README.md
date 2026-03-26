馃搱 鑾峰彇 A 鑲″競鍦烘瘡鏃ヨ〃鐜版姤鍛?
## 蹇€熷紑濮?
### 1. 瀹夎渚濊禆

```bash
pip install requests
```

### 2. 杩愯鑴氭湰

```bash
cd /home/node/.openclaw/workspace/skills/a-stock-daily-report
python3 scripts/a_stock_daily_report.py
```

### 3. 鍦ㄤ唬鐮佷腑浣跨敤

```python
from scripts.a_stock_daily_report import AStockDailyReport

report = AStockDailyReport()

# 鑾峰彇瀹屾暣鎶ュ憡
print(report.generate_report())

# 鎴栬€呭崟鐙幏鍙栨暟鎹?indices = report.get_index_data()      # 澶х洏鎸囨暟
sectors = report.get_hot_sectors(10)   # 鐑棬鏉垮潡
leaders = report.get_sector_leaders("BK1128", 3)  # 鏌愭澘鍧楅緳澶磋偂
```

## 鍔熻兘鐗规€?
鉁?**澶х洏鎸囨暟** - 涓婅瘉銆佹繁璇併€佸垱涓氭澘瀹炴椂鏁版嵁
鉁?**鐑棬鏉垮潡** - 鎸夋定骞呮帓搴忕殑 Top 10 姒傚康鏉垮潡
鉁?**榫欏ご鑲?* - 鐑棬鏉垮潡鐨勯娑ㄤ釜鑲?鉁?**甯傚満绠€璇?* - 鑷姩鐢熸垚鐨勫競鍦哄垎鏋?鉁?**鏃犻渶 API Key** - 浣跨敤涓滄柟璐㈠瘜鍏紑鎺ュ彛

## 杈撳嚭绀轰緥

```
馃搱 A 鑲″競鍦烘棩鎶?馃搮 2026 骞?03 鏈?10 鏃?23:22

銆愬ぇ鐩樻寚鏁般€?  涓婅瘉鎸囨暟锛?098.59 鐐?(+1.00%)
  娣辫瘉鎴愭寚锛?4239.30 鐐?(-0.83%)
  鍒涗笟鏉挎寚锛?281.94 鐐?(-0.81%)

銆愷煍?浠婃棩鏈€鐑澘鍧?Top 10銆?  馃敟 1. CPO 姒傚康锛?518.76 (+6.66%)
  馃敟 2. 鍏夐€氫俊妯″潡锛?082.79 (+5.69%)
  ...

銆愷煆?鏉垮潡榫欏ご鑲°€?  CPO 姒傚康:
    鈥?铇呬笢鍏?(920045): +17.04% 馃殌
    ...
```

## 鐩綍缁撴瀯

```
a-stock-daily-report/
鈹溾攢鈹€ SKILL.md                    # Skill 璇存槑鏂囨。
鈹溾攢鈹€ README.md                   # 鏈枃浠?鈹斺攢鈹€ scripts/
    鈹斺攢鈹€ a_stock_daily_report.py # 涓昏剼鏈?```

## 娉ㄦ剰浜嬮」

鈿狅笍 鏁版嵁浠呭湪浜ゆ槗鏃舵瀹炴椂鏇存柊锛堝伐浣滄棩 9:30-15:00锛?鈿狅笍 闈炰氦鏄撴椂娈垫樉绀烘渶鍚庢敹鐩樹环
鈿狅笍 浠呬緵鍙傝€冿紝涓嶆瀯鎴愭姇璧勫缓璁?
## 璁稿彲璇?
MIT License
