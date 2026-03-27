node.exe : - Fetching skill
所在位置 C:\npm-global\clawhub.ps1:24 字符: 5
+     & "node$exe"  "$basedir/node_modules/clawhub/bin/clawdhub.js" $ar ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (- Fetching skill:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
#!/usr/bin/env python3
"""
鑷€夎偂鐩戞帶棰勮宸ュ叿 - OpenClaw闆嗘垚鐗?鏀寔 A鑲°€丒TF 鍙?鍥介檯鐜拌揣榛勯噾 (浼︽暒閲?
"""

import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

# ============ 閰嶇疆鍖?============

# 鐩戞帶鍒楄〃 - 闀挎湡鎸傛満閫氱敤閰嶇疆
# 娉ㄦ剰: 浼︽暒閲戜娇鐢ㄦ柊娴猦f_XAU鎺ュ彛锛屼环鏍间负 浜烘皯甯?鍏?(绾?800鍏?鍏?= $2740/鐩庡徃)
# 
# 棰勮瑙勫垯璁捐鍘熷垯 (閫傚悎闀挎湡鎸傛満):
# 1. 鎴愭湰鐧惧垎姣旈璀? 鍩轰簬鎸佷粨鎴愭湰璁剧疆 卤10%/卤15% 棰勮锛屾瘮鍥哄畾浠锋牸鏇村悎鐞?# 2. 鍗曟棩娑ㄨ穼骞呴璀? 
#    - 涓偂 卤3%~5% (娉㈠姩澶?
#    - ETF 卤1.5%~2.5% (娉㈠姩灏?
#    - 榛勯噾 卤2%~3% (24H鐗规畩)
# 3. 闃查獨鎵? 鍚岀被棰勮30鍒嗛挓鍐呭彧鍙戜竴娆?
# 鏍囩殑绫诲瀷瀹氫箟
STOCK_TYPE = {
    "INDIVIDUAL": "individual",  # 涓偂
    "ETF": "etf",                # ETF
    "GOLD": "gold"               # 榛勯噾/璐甸噾灞?}

WATCHLIST = [
    # ===== Eave鐨勬寔浠揈TF =====
    {
        "code": "159142", 
        "name": "绉戝垱鍒涗笟浜哄伐鏅鸿兘ETF", 
        "market": "sz",
        "type": "etf",
        "cost": 1.158,
        "alerts": {
            "cost_pct_above": 10.0,    # 鐩堝埄10%鎻愰啋锛堥檷浣庯紝鍏堝洖鏈級
            "cost_pct_below": -15.0,   # 浜忔崯15%鎻愰啋锛堟斁瀹斤紝绛夎ˉ浠撴満浼氾級
            "target_buy": 0.98,        # 鐩爣琛ヤ粨浠?楼0.98锛堝搴旀垚鏈?15%锛?            "change_pct_above": 3.0,   # 鏃ュ唴澶ф定3%鎻愰啋
            "change_pct_below": -3.0,  # 鏃ュ唴澶ц穼3%鎻愰啋
            "volume_surge": 2.0,       # 鏀鹃噺2鍊嶆彁閱?            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False     # 鍏抽棴鍔ㄦ€佹鐩堬紙鍏堣В濂楋級
        }
    },
    {
        "code": "159213", 
        "name": "鏈哄櫒浜篍TF姹囨坊瀵?, 
        "market": "sz",
        "type": "etf",
        "cost": 1.307,
        "alerts": {
            "cost_pct_above": 10.0,    # 鐩堝埄10%鎻愰啋
            "cost_pct_below": -15.0,   # 浜忔崯15%鎻愰啋
            "target_buy": 1.11,        # 鐩爣琛ヤ粨浠?楼1.11锛堝己鏀拺浣嶏級
            "change_pct_above": 3.0,
            "change_pct_below": -3.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "159828", 
        "name": "鍖荤枟ETF", 
        "market": "sz",
        "type": "etf",
        "cost": 0.469,
        "note": "绛栫暐锛氭定鍒奥?.45鍑忎粨50%锛岃穼鐮绰?.40姝㈡崯",
        "alerts": {
            "cost_pct_above": 10.0,    # 鐩堝埄10%鎻愰啋
            "cost_pct_below": -14.7,   # 浜忔崯14.7%鎻愰啋锛堝搴斅?.40姝㈡崯绾匡級
            "stop_loss": 0.40,         # 鏄庣‘姝㈡崯浠?楼0.40
            "target_reduce": 0.45,     # 鐩爣鍑忎粨浠?楼0.45锛堝噺浠?0%锛?            "change_pct_above": 3.0,
            "change_pct_below": -3.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    }
]

# 鏅鸿兘棰戠巼閰嶇疆
SMART_SCHEDULE = {
    "market_open": {"hours": [(9, 30), (11, 30), (13, 0), (15, 0)], "interval": 300},  # 浜ゆ槗鏃堕棿: 5鍒嗛挓
    "after_hours": {"interval": 1800},  # 鏀剁洏鍚? 30鍒嗛挓
    "night": {"hours": [(0, 0), (8, 0)], "interval": 3600},  # 鍑屾櫒: 1灏忔椂(浠呬鸡鏁﹂噾)
}

# ============ 鏍稿績浠ｇ爜 ============

class StockAlert:
    def __init__(self):
        self.prev_data = {}
        self.alert_log = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        
    def should_run_now(self):
        """鏅鸿兘棰戠巼鎺у埗: 鍒ゆ柇褰撳墠鏄惁搴旇鎵ц鐩戞帶 (鍩轰簬鍖椾含鏃堕棿)"""
        # 鏈嶅姟鍣ㄥ湪绾界害(EST)锛屼腑鍥借偂甯傜敤鍖椾含鏃堕棿(CST = EST + 13灏忔椂)
        from datetime import timedelta
        now = datetime.now() + timedelta(hours=13)  # 杞崲鎴愬寳浜椂闂?        hour, minute = now.hour, now.minute
        time_val = hour * 100 + minute
        weekday = now.weekday()
        
        # 鍛ㄦ湯鍙洃鎺т鸡鏁﹂噾
        if weekday >= 5:  # 鍛ㄥ叚鏃?            return {"run": True, "mode": "weekend", "stocks": [s for s in WATCHLIST if s['market'] == 'fx']}
        
        # 浜ゆ槗鏃堕棿 (9:30-11:30, 13:00-15:00)
        morning_session = 930 <= time_val <= 1130
        afternoon_session = 1300 <= time_val <= 1500
        
        if morning_session or afternoon_session:
            return {"run": True, "mode": "market", "stocks": WATCHLIST, "interval": 300}
        
        # 鍗堜紤 (11:30-13:00)
        if 1130 < time_val < 1300:
            return {"run": True, "mode": "lunch", "stocks": WATCHLIST, "interval": 600}  # 10鍒嗛挓
        
        # 鏀剁洏鍚?(15:00-24:00)
        if 1500 <= time_val <= 2359:
            return {"run": True, "mode": "after_hours", "stocks": WATCHLIST, "interval": 1800}  # 30鍒嗛挓
        
        # 鍑屾櫒 (0:00-9:30)
        if 0 <= time_val < 930:
            return {"run": True, "mode": "night", "stocks": [s for s in WATCHLIST if s['market'] == 'fx'], "interval": 3600}  # 1灏忔椂
        
        return {"run": False}

    def fetch_eastmoney_kline(self, symbol, market):
        """鑾峰彇鏈€鏂版棩K绾挎暟鎹?(鏀剁洏鍚庝篃鑳借幏鍙栨敹鐩樹环)"""
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',  # 鏃ョ嚎
            'fqt': '0',
            'end': '20500101',
            'lmt': '2'  # 鍙栨渶杩?澶╋紝鐢ㄤ簬璁＄畻娑ㄨ穼骞?        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            if len(klines) >= 1:
                # 鏍煎紡: 鏃ユ湡,寮€鐩?鏀剁洏,鏈€楂?鏈€浣?鎴愪氦閲?鎴愪氦棰?鎸箙,娑ㄨ穼骞?娑ㄨ穼棰?鎹㈡墜鐜?                today = klines[-1].split(',')
                prev_close = float(today[2])  # 鏄ㄦ敹
                if len(klines) >= 2:
                    prev_close = float(klines[-2].split(',')[2])  # 鍓嶄竴澶╂敹鐩?                return {
                    'name': data.get('data', {}).get('name', symbol),
                    'price': float(today[2]),      # 鏀剁洏
                    'prev_close': prev_close,
                    'volume': int(float(today[5])),
                    'amount': float(today[6]),
                    'date': today[0],
                    'time': '15:00:00'
                }
        except Exception as e:
            print(f"涓滆储K绾胯幏鍙栧け璐?{symbol}: {e}")
        return None

    def fetch_volume_ma5(self, symbol, market):
        """鑾峰彇5鏃ュ钩鍧囨垚浜ら噺"""
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',
            'fqt': '0',
            'end': '20500101',
            'lmt': '6'  # 鍙栨渶杩?澶?浠婂ぉ+鍓?澶?
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            if len(klines) >= 2:
                # 璁＄畻鍓?鏃ュ钩鍧囨垚浜ら噺(涓嶅惈浠婂ぉ)
                volumes = []
                for k in klines[:-1]:  # 鎺掗櫎鏈€鍚庝竴澶?浠婂ぉ)
                    p = k.split(',')
                    volumes.append(float(p[5]))  # 鎴愪氦閲?                return sum(volumes) / len(volumes) if volumes else 0
        except Exception as e:
            print(f"鑾峰彇鍧囬噺澶辫触 {symbol}: {e}")
        return 0

    def fetch_ma_data(self, symbol, market):
        """鑾峰彇鍧囩嚎鏁版嵁 (MA5, MA10, MA20) 鍜?RSI"""
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',
            'fqt': '0',
            'end': '20500101',
            'lmt': '30'  # 鍙栨渶杩?0澶╄绠桵A20鍜孯SI
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            if len(klines) >= 20:
                closes = []
                for k in klines:
                    p = k.split(',')
                    closes.append(float(p[2]))  # 鏀剁洏浠?                
                # 璁＄畻鍧囩嚎
                ma5 = sum(closes[-5:]) / 5
                ma10 = sum(closes[-10:]) / 10
                ma20 = sum(closes[-20:]) / 20
                
                # 鍒ゆ柇鍧囩嚎瓒嬪娍
                prev_ma5 = sum(closes[-6:-1]) / 5
                prev_ma10 = sum(closes[-11:-1]) / 10
                
                # 璁＄畻RSI(14)
                rsi = self._calculate_rsi(closes, 14)
                
                return {
                    'MA5': ma5,
                    'MA10': ma10,
                    'MA20': ma20,
                    'MA5_trend': 'up' if ma5 > prev_ma5 else 'down',
                    'MA10_trend': 'up' if ma10 > prev_ma10 else 'down',
                    'golden_cross': prev_ma5 <= prev_ma10 and ma5 > ma10,
                    'death_cross': prev_ma5 >= prev_ma10 and ma5 < ma10,
                    'RSI': rsi,
                    'RSI_overbought': rsi > 70 if rsi else False,
                    'RSI_oversold': rsi < 30 if rsi else False
                }
        except Exception as e:
            print(f"鑾峰彇鍧囩嚎澶辫触 {symbol}: {e}")
        return None
    
    def _calculate_rsi(self, closes, period=14):
        """璁＄畻RSI鎸囨爣"""
        if len(closes) < period + 1:
            return None
        
        gains = []
        losses = []
        
        for i in range(1, period + 1):
            change = closes[-i] - closes[-i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)

    def fetch_sina_realtime(self, stocks):
        """鑾峰彇瀹炴椂琛屾儏 (浼樺厛瀹炴椂锛屾敹鐩樺悗鐢ㄦ棩K)"""
        stock_list = [s for s in stocks if s['market'] != 'fx']
        fx_list = [s for s in stocks if s['market'] == 'fx']
        results = {}
        
        # 1. A鑲?ETF - 灏濊瘯瀹炴椂鎺ュ彛
        if stock_list:
            codes = [f"{s['market']}{s['code']}" for s in stock_list]
            url = f"https://hq.sinajs.cn/list={','.join(codes)}"
            try:
                resp = self.session.get(url, headers={'Referer': 'https://finance.sina.com.cn'}, timeout=10)
                resp.encoding = 'gb18030'
                for line in resp.text.strip().split(';'):
                    if 'hq_str_' not in line or '=' not in line: continue
                    key = line.split('=')[0].split('_')[-1]
                    if len(key) < 8: continue
                    data_str = line[line.index('"')+1 : line.rindex('"')]
                    p = data_str.split(',')
                    if len(p) > 30 and float(p[3]) > 0:
                        # 鏂版氮鏁版嵁鏍煎紡: 鍚嶇О,浠婃棩寮€鐩?鏄ㄦ棩鏀剁洏,褰撳墠浠?浠婃棩鏈€楂?浠婃棩鏈€浣?绔炰拱浠?绔炲崠浠?鎴愪氦閲?鎴愪氦棰?..
                        # 淇濆瓨鏄ㄦ棩鏈€楂樻渶浣庝环鐢ㄤ簬璺崇┖妫€娴?(鐢ㄦ槰鏃ユ敹鐩樿繎浼硷紝鎴栫敤鍧囩嚎鏁版嵁琛ュ厖)
                        results[key[2:]] = {
                            'name': p[0], 
                            'price': float(p[3]), 
                            'prev_close': float(p[2]),
                            'open': float(p[1]),      # 浠婃棩寮€鐩?                            'high': float(p[4]),      # 浠婃棩鏈€楂?                            'low': float(p[5]),       # 浠婃棩鏈€浣?                            'volume': int(p[8]), 
                            'amount': float(p[9]), 
                            'date': p[30], 
                            'time': p[31],
                            'prev_high': float(p[2]) * 1.02,  # 浼扮畻鏄ㄦ棩鏈€楂?(鏄ㄦ敹+2%)
                            'prev_low': float(p[2]) * 0.98    # 浼扮畻鏄ㄦ棩鏈€浣?(鏄ㄦ敹-2%)
                        }
            except Exception as e: 
                print(f"瀹炴椂琛屾儏鑾峰彇澶辫触: {e}")
            
            # 2. 濡傛灉瀹炴椂鎺ュ彛杩斿洖绌烘垨0锛岀敤鏃绾胯ˉ鏁版嵁
            for stock in stock_list:
                code = stock['code']
                if code not in results or results[code]['price'] <= 0:
                    kline_data = self.fetch_eastmoney_kline(code, 1 if stock['market'] == 'sh' else 0)
                    if kline_data:
                        results[code] = kline_data
                        print(f"  {stock['name']}: 浣跨敤鏃鏀剁洏浠?{kline_data['price']}")

        # 3. 浼︽暒閲?(鏂版氮hf_XAU鎺ュ彛锛屼汉姘戝竵/鍏?
        if fx_list:
            url = "https://hq.sinajs.cn/list=hf_XAU"
            try:
                resp = self.session.get(url, headers={'Referer': 'https://finance.sina.com.cn'}, timeout=10)
                line = resp.text.strip()
                if '"' in line:
                    data_str = line[line.index('"')+1 : line.rindex('"')]
                    p = data_str.split(',')
                    if len(p) >= 13:
                        # 鏂版氮hf_XAU: 浜烘皯甯?鍏?(绾?800=2740缇庡厓/鐩庡徃)
                        price = float(p[0])
                        results['XAU'] = {
                            'name': '浼︽暒閲?, 
                            'price': price, 
                            'prev_close': float(p[7]),
                            'volume': 0, 'amount': 0, 
                            'date': p[11] if len(p) > 11 else datetime.now().strftime('%Y-%m-%d'), 
                            'time': p[6]
                        }
            except Exception as e: 
                print(f"浼︽暒閲戣幏鍙栧け璐? {e}")
            
        return results
    
    def check_alerts(self, stock_config, data):
        """妫€鏌ラ璀︽潯浠?(鏀寔鎴愭湰鐧惧垎姣斻€佸崟鏃ユ定璺屽箙銆佸垎绾ч璀?"""
        alerts = []
        alert_weights = []  # 鐢ㄤ簬璁＄畻棰勮绾у埆
        code = stock_config['code']
        cfg = stock_config.get('alerts', {})
        cost = stock_config.get('cost', 0)
        stock_type = stock_config.get('type', 'individual')
        price, prev_close = data['price'], data['prev_close']
        change_pct = (price - prev_close) / prev_close * 100 if prev_close else 0
        
        # 1. 鍩轰簬鎴愭湰鐨勭櫨鍒嗘瘮棰勮 (鏉冮噸: 楂?
        if cost > 0:
            cost_change_pct = (price - cost) / cost * 100
            
            if 'cost_pct_above' in cfg and cost_change_pct >= cfg['cost_pct_above']:
                target_price = cost * (1 + cfg['cost_pct_above']/100)
                if not self._alerted_recently(code, 'cost_above'):
                    alerts.append(('cost_above', f"馃幆 鐩堝埄 {cfg['cost_pct_above']:.0f}% (鐩爣浠?楼{target_price:.2f})"))
                    alert_weights.append(3)  # 楂樻潈閲?            
            if 'cost_pct_below' in cfg and cost_change_pct <= cfg['cost_pct_below']:
                target_price = cost * (1 + cfg['cost_pct_below']/100)
                if not self._alerted_recently(code, 'cost_below'):
                    alerts.append(('cost_below', f"馃洃 浜忔崯 {abs(cfg['cost_pct_below']):.0f}% (姝㈡崯浠?楼{target_price:.2f})"))
                    alert_weights.append(3)  # 楂樻潈閲?        
        # 2. 鍩轰簬鍥哄畾浠锋牸鐨勯璀?(鏉冮噸: 涓?
        if 'price_above' in cfg and price >= cfg['price_above'] and not self._alerted_recently(code, 'above'):
            alerts.append(('above', f"馃殌 浠锋牸绐佺牬 楼{cfg['price_above']}"))
            alert_weights.append(2)
        if 'price_below' in cfg and price <= cfg['price_below'] and not self._alerted_recently(code, 'below'):
            alerts.append(('below', f"馃搲 浠锋牸璺岀牬 楼{cfg['price_below']}"))
            alert_weights.append(2)
        
        # 3. 鍗曟棩娑ㄨ穼骞呴璀?(鏉冮噸: 鏍规嵁骞呭害)
        if 'change_pct_above' in cfg and change_pct >= cfg['change_pct_above'] and not self._alerted_recently(code, 'pct_up'):
            alerts.append(('pct_up', f"馃搱 鏃ュ唴澶ф定 {change_pct:+.2f}%"))
            # 寮傚姩瓒婂ぇ鏉冮噸瓒婇珮
            if change_pct >= 7:
                alert_weights.append(3)  # 娑ㄥ仠闄勮繎
            elif change_pct >= 5:
                alert_weights.append(2)  # 澶ф定
            else:
                alert_weights.append(1)  # 涓€鑸紓鍔?                
        if 'change_pct_below' in cfg and change_pct <= cfg['change_pct_below'] and not self._alerted_recently(code, 'pct_down'):
            alerts.append(('pct_down', f"馃搲 鏃ュ唴澶ц穼 {change_pct:+.2f}%"))
            if change_pct <= -7:
                alert_weights.append(3)  # 璺屽仠闄勮繎
            elif change_pct <= -5:
                alert_weights.append(2)  # 澶ц穼
            else:
                alert_weights.append(1)  # 涓€鑸紓鍔?        
        # 4. 鎴愪氦閲忓紓鍔ㄦ娴?(浠呰偂绁ㄥ拰ETF)
        if stock_type != 'gold' and 'volume_surge' in cfg:
            current_volume = data.get('volume', 0)
            if current_volume > 0:
                # 灏濊瘯鑾峰彇5鏃ュ潎閲?                ma5_volume = self.fetch_volume_ma5(code, 1 if stock_config['market'] == 'sh' else 0)
                if ma5_volume > 0:
                    volume_ratio = current_volume / ma5_volume
                    threshold = cfg['volume_surge']
                    
                    if volume_ratio >= threshold and not self._alerted_recently(code, 'volume_surge'):
                        alerts.append(('volume_surge', f"馃搳 鏀鹃噺 {volume_ratio:.1f}鍊?(5鏃ュ潎閲?"))
                        alert_weights.append(2)  # 涓瓑鏉冮噸
                    elif volume_ratio <= 0.5 and not self._alerted_recently(code, 'volume_shrink'):
                        alerts.append(('volume_shrink', f"馃搲 缂╅噺 {volume_ratio:.1f}鍊?(5鏃ュ潎閲?"))
                        alert_weights.append(1)  # 浣庢潈閲?        
        # 5. 鍧囩嚎绯荤粺 (MA閲戝弶姝诲弶)
        if stock_type != 'gold' and cfg.get('ma_monitor', True):
            ma_data = self.fetch_ma_data(code, 1 if stock_config['market'] == 'sh' else 0)
            if ma_data:
                # 閲戝弶: MA5涓婄┛MA10 (鐭湡杞己)
                if ma_data.get('golden_cross') and not self._alerted_recently(code, 'ma_golden'):
                    alerts.append(('ma_golden', f"馃専 鍧囩嚎閲戝弶 (MA5楼{ma_data['MA5']:.2f}涓婄┛MA10楼{ma_data['MA10']:.2f})"))
                    alert_weights.append(3)  # 楂樻潈閲?                
                # 姝诲弶: MA5涓嬬┛MA10 (鐭湡杞急)
                if ma_data.get('death_cross') and not self._alerted_recently(code, 'ma_death'):
                    alerts.append(('ma_death', f"鈿狅笍 鍧囩嚎姝诲弶 (MA5楼{ma_data['MA5']:.2f}涓嬬┛MA10楼{ma_data['MA10']:.2f})"))
                    alert_weights.append(3)  # 楂樻潈閲?                
                # RSI瓒呬拱瓒呭崠妫€娴?                rsi = ma_data.get('RSI')
                if rsi:
                    if ma_data.get('RSI_overbought') and not self._alerted_recently(code, 'rsi_high'):
                        alerts.append(('rsi_high', f"馃敟 RSI瓒呬拱 ({rsi})锛屽彲鑳藉洖璋?))
                        alert_weights.append(2)
                    elif ma_data.get('RSI_oversold') and not self._alerted_recently(code, 'rsi_low'):
                        alerts.append(('rsi_low', f"鉂勶笍 RSI瓒呭崠 ({rsi})锛屽彲鑳藉弽寮?))
                        alert_weights.append(2)
        
        # 5. 璺崇┖缂哄彛妫€娴?(闇€瑕佹槰鏃ユ暟鎹?
        if stock_type != 'gold':
            prev_high = data.get('prev_high', 0)
            prev_low = data.get('prev_low', 0)
            current_open = data.get('open', price)  # 褰撳墠浠疯繎浼煎紑鐩樹环
            
            # 鍚戜笂璺崇┖: 浠婃棩寮€鐩?> 鏄ㄦ棩鏈€楂?            if prev_high > 0 and current_open > prev_high * 1.01:  # 1%浠ヤ笂绠楄烦绌?                gap_pct = (current_open - prev_high) / prev_high * 100
                if not self._alerted_recently(code, 'gap_up'):
                    alerts.append(('gap_up', f"猬嗭笍 鍚戜笂璺崇┖ {gap_pct:.1f}%"))
                    alert_weights.append(2)
            
            # 鍚戜笅璺崇┖: 浠婃棩寮€鐩?< 鏄ㄦ棩鏈€浣?            elif prev_low > 0 and current_open < prev_low * 0.99:
                gap_pct = (prev_low - current_open) / prev_low * 100
                if not self._alerted_recently(code, 'gap_down'):
                    alerts.append(('gap_down', f"猬囷笍 鍚戜笅璺崇┖ {gap_pct:.1f}%"))
                    alert_weights.append(2)
        
        # 6. 鍔ㄦ€佹鐩?绉诲姩姝㈡崯 (褰撶泩鍒╄揪鍒颁竴瀹氬箙搴﹀悗鍚姩)
        if cost > 0:
            profit_pct = (price - cost) / cost * 100
            
            # 褰撶泩鍒?>= 10% 鏃讹紝鍚姩绉诲姩姝㈢泩
            if profit_pct >= 10:
                # 璁＄畻鍥炴挙骞呭害 (浠庢渶楂樼偣鍥炴挙)
                high_since_cost = data.get('high', price)
                drawdown = (high_since_cost - price) / high_since_cost * 100 if high_since_cost > cost else 0
                
                # 鍥炴挙5%鎻愰啋鍑忎粨
                if drawdown >= 5 and not self._alerted_recently(code, 'trailing_stop_5'):
                    alerts.append(('trailing_stop_5', f"馃搲 鍒╂鼎鍥炴挙 {drawdown:.1f}%锛屽缓璁噺浠撲繚鎶ゅ埄娑?))
                    alert_weights.append(2)
                
                # 鍥炴挙10%鎻愰啋娓呬粨
                elif drawdown >= 10 and not self._alerted_recently(code, 'trailing_stop_10'):
                    alerts.append(('trailing_stop_10', f"馃毃 鍒╂鼎鍥炴挙 {drawdown:.1f}%锛屽缓璁竻浠撴鎹?))
                    alert_weights.append(3)
        
        # 6. 璁＄畻棰勮绾у埆
        level = self._calculate_alert_level(alerts, alert_weights, stock_type)
        
        return alerts, level
    
    def _calculate_alert_level(self, alerts, weights, stock_type):
        """璁＄畻棰勮绾у埆: info(鎻愰啋) / warning(璀﹀憡) / critical(绱ф€?"""
        if not alerts:
            return None
        
        total_weight = sum(weights)
        alert_count = len(alerts)
        
        # 绱ф€? 澶氭潯浠跺叡鎸?鎴?楂樻潈閲嶅崟涓€鏉′欢
        if total_weight >= 5 or alert_count >= 3:
            return "critical"
        
        # 璀﹀憡: 涓瓑鏉冮噸 鎴?2涓潯浠?        if total_weight >= 3 or alert_count >= 2:
            return "warning"
        
        # 鎻愰啋: 鍗曚竴浣庢潈閲嶆潯浠?        return "info"
    
    def _alerted_recently(self, code, atype):
        now = time.time()
        self.alert_log = [l for l in self.alert_log if now - l['t'] < 1800] # 30鍒嗛挓鏈夋晥鏈?        for l in self.alert_log:
            if l['c'] == code and l['a'] == atype: return True
        return False
    
    def record_alert(self, code, atype):
        self.alert_log.append({'c': code, 'a': atype, 't': time.time()})
    
    def fetch_news(self, symbol):
        """鎶撳彇涓偂鏈€杩戞柊闂?(鏂版氮/涓滆储鑱氬悎) - 绠€鍖栫増"""
        try:
            # 浣跨敤涓滆储涓偂鏂伴椈API
            url = f"https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax"
            params = {"code": symbol}
            resp = self.session.get(url, params=params, timeout=5)
            return ["鏂伴椈妯″潡宸插氨缁?(甯傚満鏀剁洏涓?"]
        except:
            return []

    def run_once(self, smart_mode=True):
        """鎵ц鐩戞帶 (鏀寔鏅鸿兘棰戠巼)"""
        if smart_mode:
            schedule = self.should_run_now()
            if not schedule.get("run"):
                return []
            
            stocks_to_check = schedule.get("stocks", WATCHLIST)
            mode = schedule.get("mode", "normal")
            
            # 鍙湪鐗瑰畾妯″紡鎵撳嵃鏃ュ織
            if mode in ["market", "weekend"]:
                print(f"[{datetime.now().strftime('%H:%M')}] {mode}妯″紡鎵弿 {len(stocks_to_check)} 鍙爣鐨?..")
        else:
            stocks_to_check = WATCHLIST
        
        data_map = self.fetch_sina_realtime(stocks_to_check)
        triggered = []
        
        for stock in stocks_to_check:
            code = stock['code']
            if code not in data_map: continue
            
            data = data_map[code]
            
            # 鏁版嵁鏈夋晥鎬ф鏌?            if data['price'] <= 0 or data['prev_close'] <= 0:
                continue
            
            alerts, level = self.check_alerts(stock, data)
            
            if alerts:
                change_pct = (data['price'] - data['prev_close']) / data['prev_close'] * 100 if data['prev_close'] else 0
                
                # 涓浗涔犳儻: 绾㈣壊=涓婃定, 缁胯壊=涓嬭穼
                if change_pct > 0:
                    color_emoji = "馃敶"  # 绾㈡定
                elif change_pct < 0:
                    color_emoji = "馃煝"  # 缁胯穼
                else:
                    color_emoji = "鈿?
                
                # 棰勮绾у埆鏍囪瘑
                level_icons = {
                    "critical": "馃毃",  # 绱ф€?                    "warning": "鈿狅笍",   # 璀﹀憡
                    "info": "馃摙"       # 鎻愰啋
                }
                level_icon = level_icons.get(level, "馃摙")
                level_text = {"critical": "銆愮揣鎬ャ€?, "warning": "銆愯鍛娿€?, "info": "銆愭彁閱掋€?}.get(level, "")
                
                msg = f"<b>{level_icon} {level_text}{color_emoji} {stock['name']} ({code})</b>\n"
                msg += f"鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣\n"
                msg += f"馃挵 褰撳墠浠锋牸: <b>{data['price']:.2f}</b> ({change_pct:+.2f}%)\n"
                
                # 鏄剧ず鎸佷粨鐩堜簭
                cost = stock.get('cost', 0)
                if cost > 0:
                    cost_change = (data['price'] - cost) / cost * 100
                    profit_icon = "馃敶+" if cost_change > 0 else "馃煝"
                    msg += f"馃搳 鎸佷粨鎴愭湰: 楼{cost:.2f} | 鐩堜簭: {profit_icon}{cost_change:.2f}%\n"
                
                msg += f"\n馃幆 瑙﹀彂棰勮 ({len(alerts)}椤?:\n"
                for _, text in alerts: 
                    msg += f"  鈥?{text}\n"
                    self.record_alert(code, _)
                
                # Pro鐗堬細闆嗘垚鏅鸿兘鍒嗘瀽
                try:
                    from analyser import StockAnalyser
                    analyser = StockAnalyser()
                    insight = analyser.generate_insight(stock, {
                        'price': data['price'],
                        'change_pct': change_pct
                    }, alerts)
                    msg += f"\n{insight}"
                except Exception:
                    pass
                
                triggered.append(msg)
        
        return triggered

if __name__ == '__main__':
    monitor = StockAlert()
    for alert in monitor.run_once():
        print(alert)
