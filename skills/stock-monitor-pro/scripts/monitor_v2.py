#!/usr/bin/env python3
"""
鑷€夎偂鐩戞帶棰勮宸ュ叿 V2 - 鍙嶇埇铏紭鍖栫増
鏀寔 A鑲°€丒TF
浼樺寲: Session绾A缁戝畾銆佸畬鏁磋姹傚ご銆?-10鍒嗛挓闅忔満寤惰繜銆佸鏁版嵁婧愬啑浣?"""

import requests
import json
import time
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# ============ 閰嶇疆鍖?============

WATCHLIST = [
    {
        "code": "600352",
        "name": "浙江龙盛",
        "market": "sh",
        "type": "stock",
        "cost": 16.948,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 12.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "300033",
        "name": "同花顺",
        "market": "sz",
        "type": "stock",
        "cost": 423.488,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 280.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "600487",
        "name": "亨通光电",
        "market": "sh",
        "type": "stock",
        "cost": 43.210,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 38.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "600893",
        "name": "航发动力",
        "market": "sh",
        "type": "stock",
        "cost": 49.184,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 42.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "601168",
        "name": "西部矿业",
        "market": "sh",
        "type": "stock",
        "cost": 26.169,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 22.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "518880",
        "name": "黄金ETF",
        "market": "sh",
        "type": "etf",
        "cost": 9.868,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -5.0,
            "stop_loss": 0,
            "change_pct_above": 2.5,
            "change_pct_below": -2.5,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "831330",
        "name": "普适导航",
        "market": "bj",
        "type": "stock",
        "cost": 20.361,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 18.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "430046",
        "name": "圣博润",
        "market": "sz",
        "type": "stock",
        "cost": 0.478,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "600114",
        "name": "东睦股份",
        "market": "sh",
        "type": "stock",
        "cost": 31.176,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 25.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "600089",
        "name": "特变电工",
        "market": "sh",
        "type": "stock",
        "cost": 24.765,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "stop_loss": 25.0,
            "change_pct_above": 4.0,
            "change_pct_below": -4.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    }
]

# UA姹?- Session鍚姩鏃堕殢鏈洪€夋嫨涓€涓?USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Edg/119.0.0.0"
]

# ============ 鏍稿績浠ｇ爜 ============

class StockAlert:
    def __init__(self):
        self.prev_data = {}
        self.alert_log = []
        self.failed_sources = {}  # 璁板綍鍚勬暟鎹簮澶辫触娆℃暟
        self.source_cooldown = {}  # 鏁版嵁婧愬喎鍗存椂闂?        self.error_notifications = {}  # 閿欒閫氱煡璁板綍锛堥槻閲嶅锛?        self.NOTIFICATION_COOLDOWN = 1800  # 閿欒閫氱煡鍐峰嵈30鍒嗛挓
        
        # 鏃ユ姤鐩稿叧
        self.daily_report_sent = False  # 浠婃棩鏃ユ姤鏄惁宸插彂閫?        self.daily_data = {}  # 瀛樺偍褰撴棩鏁版嵁鐢ㄤ簬鏃ユ姤
        self.today_date = datetime.now().strftime('%Y-%m-%d')
        
        # Session绾A缁戝畾 - 鏁翠釜鐢熷懡鍛ㄦ湡浣跨敤鍚屼竴涓猆A
        self.user_agent = random.choice(USER_AGENTS)
        print(f"[鍒濆鍖朷 浣跨敤UA: {self.user_agent[:60]}...")
        
        # 鍒涘缓甯﹀畬鏁磋姹傚ご鐨剆ession
        self.session = requests.Session()
        self._setup_session_headers()
        
    def _setup_session_headers(self):
        """璁剧疆瀹屾暣鐨勬祻瑙堝櫒鎸囩汗璇锋眰澶?""
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0"
        })
        
    def _random_delay(self, min_sec=0.5, max_sec=3.0):
        """璇锋眰鍓嶉殢鏈哄欢杩燂紝妯℃嫙鐪熶汉鎿嶄綔闂撮殧"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        return delay
        
    def _is_source_available(self, source_name):
        """妫€鏌ユ暟鎹簮鏄惁鍙敤锛堝喎鍗存湡宸茶繃锛?""
        if source_name in self.source_cooldown:
            if time.time() < self.source_cooldown[source_name]:
                return False
        return True
        
    def _mark_source_failed(self, source_name, cooldown_minutes=5):
        """鏍囪鏁版嵁婧愬け璐ワ紝杩涘叆鍐峰嵈鏈?""
        self.failed_sources[source_name] = self.failed_sources.get(source_name, 0) + 1
        # 杩炵画澶辫触3娆′互涓婏紝鍐峰嵈30鍒嗛挓
        if self.failed_sources[source_name] >= 3:
            cooldown_minutes = 30
        self.source_cooldown[source_name] = time.time() + cooldown_minutes * 60
        print(f"[鏁版嵁婧怾 {source_name} 鏍囪涓哄け璐ワ紝鍐峰嵈{cooldown_minutes}鍒嗛挓")
        
    def _mark_source_success(self, source_name):
        """鏍囪鏁版嵁婧愭垚鍔燂紝閲嶇疆澶辫触璁℃暟"""
        if source_name in self.failed_sources:
            del self.failed_sources[source_name]

    def should_run_now(self):
        """鏅鸿兘棰戠巼鎺у埗: 3-10鍒嗛挓闅忔満"""
        now = datetime.now() + timedelta(hours=13)  # 鍖椾含鏃堕棿
        hour, minute = now.hour, now.minute
        time_val = hour * 100 + minute
        weekday = now.weekday()
        
        # 鍛ㄦ湯浣庨
        if weekday >= 5:
            return {"run": True, "mode": "weekend", "stocks": WATCHLIST, "interval": random.randint(600, 1800)}
        
        # 浜ゆ槗鏃堕棿 (9:30-11:30, 13:00-15:00)
        morning_session = 930 <= time_val <= 1130
        afternoon_session = 1300 <= time_val <= 1500
        
        if morning_session or afternoon_session:
            # 浜ゆ槗娲昏穬鏃舵锛?-6鍒嗛挓闅忔満
            return {"run": True, "mode": "market", "stocks": WATCHLIST, "interval": random.randint(180, 360)}
        
        # 鍗堜紤 (11:30-13:00)
        if 1130 < time_val < 1300:
            return {"run": True, "mode": "lunch", "stocks": WATCHLIST, "interval": random.randint(300, 600)}
        
        # 鏀剁洏鍚?(15:00-24:00)
        if 1500 <= time_val <= 2359:
            return {"run": True, "mode": "after_hours", "stocks": WATCHLIST, "interval": random.randint(900, 1800)}
        
        # 鍑屾櫒 (0:00-9:30)
        if 0 <= time_val < 930:
            return {"run": True, "mode": "night", "stocks": WATCHLIST, "interval": random.randint(1800, 3600)}
        
        return {"run": False}

    # ============ 澶氭暟鎹簮鑾峰彇 ============
    
    def fetch_sina_realtime(self, stocks):
        """鏁版嵁婧?: 鏂版氮璐㈢粡瀹炴椂琛屾儏"""
        source_name = "sina"
        if not self._is_source_available(source_name):
            return None, "鍐峰嵈涓?
            
        stock_list = [s for s in stocks if s['market'] != 'fx']
        if not stock_list:
            return {}, None
            
        codes = [f"{s['market']}{s['code']}" for s in stock_list]
        url = f"https://hq.sinajs.cn/list={','.join(codes)}"
        
        try:
            self._random_delay(0.3, 1.0)
            resp = self.session.get(url, headers={'Referer': 'https://finance.sina.com.cn'}, timeout=10)
            resp.encoding = 'gb18030'
            
            results = {}
            for line in resp.text.strip().split(';'):
                if 'hq_str_' not in line or '=' not in line: 
                    continue
                key = line.split('=')[0].split('_')[-1]
                if len(key) < 8: 
                    continue
                data_str = line[line.index('"')+1 : line.rindex('"')]
                p = data_str.split(',')
                if len(p) > 30 and float(p[3]) > 0:
                    results[key[2:]] = {
                        'name': p[0], 
                        'price': float(p[3]), 
                        'prev_close': float(p[2]),
                        'open': float(p[1]),
                        'high': float(p[4]),
                        'low': float(p[5]),
                        'volume': int(p[8]), 
                        'amount': float(p[9]), 
                        'date': p[30], 
                        'time': p[31],
                        'source': 'sina'
                    }
            
            if results:
                self._mark_source_success(source_name)
                return results, None
            return None, "杩斿洖鏁版嵁涓虹┖"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    def fetch_tencent_realtime(self, stocks):
        """鏁版嵁婧?: 鑵捐璐㈢粡瀹炴椂琛屾儏 (澶囩敤)"""
        source_name = "tencent"
        if not self._is_source_available(source_name):
            return None, "鍐峰嵈涓?
            
        stock_list = [s for s in stocks if s['market'] != 'fx']
        if not stock_list:
            return {}, None
            
        codes = [f"{s['market']}{s['code']}" for s in stock_list]
        url = f"https://qt.gtimg.cn/q={','.join(codes)}"
        
        try:
            self._random_delay(0.3, 1.0)
            resp = self.session.get(url, timeout=10)
            resp.encoding = 'gb18030'
            
            results = {}
            for line in resp.text.strip().split(';'):
                if 'v_' not in line or '=' not in line:
                    continue
                key = line.split('=')[0].split('_')[-1]
                data_str = line[line.index('"')+1 : line.rindex('"')]
                p = data_str.split('~')
                if len(p) > 40:
                    # 鑵捐鏍煎紡: 鑲＄エ鍚嶇О~鑲＄エ浠ｇ爜~褰撳墠浠锋牸~鏄ㄦ敹~浠婂紑...
                    results[key[2:]] = {
                        'name': p[1],
                        'price': float(p[3]),
                        'prev_close': float(p[4]),
                        'open': float(p[5]),
                        'high': float(p[33]),
                        'low': p[34],
                        'volume': int(p[36]),
                        'amount': float(p[37]),
                        'source': 'tencent'
                    }
            
            if results:
                self._mark_source_success(source_name)
                return results, None
            return None, "杩斿洖鏁版嵁涓虹┖"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    def fetch_eastmoney_kline(self, symbol, market):
        """鏁版嵁婧?: 涓滄柟璐㈠瘜K绾挎暟鎹?(鍧囩嚎/RSI/鎴愪氦閲?"""
        source_name = "eastmoney"
        if not self._is_source_available(source_name):
            return None, "鍐峰嵈涓?
            
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',
            'fqt': '0',
            'end': '20500101',
            'lmt': '30'
        }
        
        try:
            self._random_delay(0.5, 1.5)
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            
            if len(klines) >= 20:
                self._mark_source_success(source_name)
                return klines, None
            return None, "鏁版嵁涓嶈冻"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    def fetch_ths_kline(self, symbol, market):
        """鏁版嵁婧?: 鍚岃姳椤篕绾挎暟鎹?(澶囩敤)"""
        source_name = "ths"
        if not self._is_source_available(source_name):
            return None, "鍐峰嵈涓?
            
        # 鍚岃姳椤轰唬鐮佹牸寮?        ths_code = f"{market}{symbol}"
        url = f"http://d.10jqka.com.cn/v6/line/{ths_code}/01/all.js"
        
        try:
            self._random_delay(0.5, 1.5)
            headers = {
                'Referer': f'http://stockpage.10jqka.com.cn/{symbol}/',
                'User-Agent': self.user_agent
            }
            resp = self.session.get(url, headers=headers, timeout=10)
            
            # 鍚岃姳椤鸿繑鍥炵殑鏄疛SONP鏍煎紡锛岄渶瑕佽В鏋?            text = resp.text
            if '(' in text and ')' in text:
                json_str = text[text.index('(')+1:text.rindex(')')]
                data = json.loads(json_str)
                
                # 瑙ｆ瀽K绾挎暟鎹?                klines = data.get('data', '').split(';')
                if len(klines) >= 20:
                    self._mark_source_success(source_name)
                    return klines, None
            return None, "瑙ｆ瀽澶辫触"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    # ============ 鎶€鏈寚鏍囪绠?============
    
    def calculate_indicators(self, klines):
        """浠嶬绾胯绠楁妧鏈寚鏍?""
        if not klines or len(klines) < 20:
            return None
            
        closes = []
        volumes = []
        
        for k in klines:
            if isinstance(k, str):
                p = k.split(',')
                if len(p) >= 6:
                    closes.append(float(p[2]))  # 鏀剁洏浠?                    volumes.append(float(p[5]))  # 鎴愪氦閲?            elif isinstance(k, dict):
                closes.append(float(k.get('close', 0)))
                volumes.append(float(k.get('volume', 0)))
        
        if len(closes) < 20:
            return None
            
        # 璁＄畻鍧囩嚎
        ma5 = sum(closes[-5:]) / 5
        ma10 = sum(closes[-10:]) / 10
        ma20 = sum(closes[-20:]) / 20
        
        prev_ma5 = sum(closes[-6:-1]) / 5
        prev_ma10 = sum(closes[-11:-1]) / 10
        
        # 璁＄畻5鏃ュ潎閲?        volume_ma5 = sum(volumes[-6:-1]) / 5 if len(volumes) >= 6 else 0
        today_volume = volumes[-1] if volumes else 0
        
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
            'RSI_oversold': rsi < 30 if rsi else False,
            'volume_ma5': volume_ma5,
            'volume_ratio': today_volume / volume_ma5 if volume_ma5 > 0 else 0
        }
    
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

    # ============ 涓荤洃鎺ч€昏緫 ============
    
    def get_stock_data(self, stock):
        """鑾峰彇鍗曞彧鑲＄エ鐨勫畬鏁存暟鎹紙澶氭簮闄嶇骇锛?""
        code = stock['code']
        market = 0 if stock['market'] == 'sh' else 1  # 涓滆储鐢ㄧ殑甯傚満浠ｇ爜
        
        result = {
            'code': code,
            'name': stock['name'],
            'price': 0,
            'prev_close': 0,
            'change_pct': 0,
            'volume': 0,
            'indicators': None,
            'sources_used': [],
            'errors': []
        }
        
        # Step 1: 鑾峰彇瀹炴椂浠锋牸锛堜紭鍏堢骇: 鏂版氮 鈫?鑵捐锛?        realtime_data = None
        
        # 灏濊瘯鏂版氮
        sina_data, sina_err = self.fetch_sina_realtime([stock])
        if sina_data and code in sina_data:
            realtime_data = sina_data[code]
            result['sources_used'].append('sina')
        else:
            if sina_err:
                result['errors'].append(f"鏂版氮: {sina_err}")
        
        # 鏂版氮澶辫触锛屽皾璇曡吘璁?        if not realtime_data:
            tencent_data, tencent_err = self.fetch_tencent_realtime([stock])
            if tencent_data and code in tencent_data:
                realtime_data = tencent_data[code]
                result['sources_used'].append('tencent')
            else:
                if tencent_err:
                    result['errors'].append(f"鑵捐: {tencent_err}")
        
        if realtime_data:
            result['price'] = realtime_data['price']
            result['prev_close'] = realtime_data.get('prev_close', realtime_data['price'])
            result['volume'] = realtime_data.get('volume', 0)
            result['change_pct'] = round((result['price'] - result['prev_close']) / result['prev_close'] * 100, 2)
        else:
            result['errors'].append("鏃犳硶鑾峰彇瀹炴椂浠锋牸")
            return result
        
        # Step 2: 鑾峰彇鎶€鏈寚鏍囷紙浼樺厛绾? 涓滆储 鈫?鍚岃姳椤猴級
        klines = None
        
        # 灏濊瘯涓滆储
        em_klines, em_err = self.fetch_eastmoney_kline(code, market)
        if em_klines:
            klines = em_klines
            result['sources_used'].append('eastmoney')
        else:
            if em_err:
                result['errors'].append(f"涓滆储: {em_err}")
        
        # 涓滆储澶辫触锛屽皾璇曞悓鑺遍『
        if not klines:
            ths_klines, ths_err = self.fetch_ths_kline(code, stock['market'])
            if ths_klines:
                klines = ths_klines
                result['sources_used'].append('ths')
            else:
                if ths_err:
                    result['errors'].append(f"鍚岃姳椤? {ths_err}")
        
        # 璁＄畻鎶€鏈寚鏍?        if klines:
            result['indicators'] = self.calculate_indicators(klines)
        else:
            result['errors'].append("鏃犳硶鑾峰彇鎶€鏈寚鏍?)
        
        return result

    def check_alerts(self, stock, data):
        """妫€鏌ラ璀︽潯浠?""
        alerts = []
        config = stock['alerts']
        price = data['price']
        cost = stock['cost']
        change_pct = data['change_pct']
        indicators = data.get('indicators')
        
        if price <= 0:
            return alerts
        
        # 1. 鎴愭湰鐧惧垎姣旈璀?        cost_change_pct = round((price - cost) / cost * 100, 2)
        if config.get('cost_pct_above') and cost_change_pct >= config['cost_pct_above']:
            alerts.append({
                'level': 'warning',
                'type': 'cost_profit',
                'message': f"鐩堝埄 {cost_change_pct}% (鐩爣 {config['cost_pct_above']}%)"
            })
        if config.get('cost_pct_below') and cost_change_pct <= config['cost_pct_below']:
            alerts.append({
                'level': 'warning', 
                'type': 'cost_loss',
                'message': f"浜忔崯 {abs(cost_change_pct)}% (闃堝€?{abs(config['cost_pct_below'])}%)"
            })
        
        # 2. 鏃ュ唴娑ㄨ穼骞呴璀?        if config.get('change_pct_above') and change_pct >= config['change_pct_above']:
            alerts.append({
                'level': 'info',
                'type': 'rise',
                'message': f"鏃ュ唴澶ф定 {change_pct}%"
            })
        if config.get('change_pct_below') and change_pct <= config['change_pct_below']:
            alerts.append({
                'level': 'info',
                'type': 'fall',
                'message': f"鏃ュ唴澶ц穼 {abs(change_pct)}%"
            })
        
        # 3. 鎶€鏈寚鏍囬璀︼紙濡傛灉鏈夋暟鎹級
        if indicators:
            # 鎴愪氦閲忓紓鍔?            if config.get('volume_surge') and indicators.get('volume_ratio', 0) >= config['volume_surge']:
                alerts.append({
                    'level': 'info',
                    'type': 'volume',
                    'message': f"鏀鹃噺 {indicators['volume_ratio']:.1f}鍊?
                })
            
            # 鍧囩嚎閲戝弶姝诲弶
            if config.get('ma_monitor'):
                if indicators.get('golden_cross'):
                    alerts.append({
                        'level': 'warning',
                        'type': 'golden_cross',
                        'message': f"鍧囩嚎閲戝弶 (MA5:{indicators['MA5']:.2f} > MA10:{indicators['MA10']:.2f})"
                    })
                if indicators.get('death_cross'):
                    alerts.append({
                        'level': 'warning',
                        'type': 'death_cross',
                        'message': f"鍧囩嚎姝诲弶 (MA5:{indicators['MA5']:.2f} < MA10:{indicators['MA10']:.2f})"
                    })
            
            # RSI瓒呬拱瓒呭崠
            if config.get('rsi_monitor'):
                if indicators.get('RSI_overbought'):
                    alerts.append({
                        'level': 'info',
                        'type': 'rsi_high',
                        'message': f"RSI瓒呬拱 {indicators['RSI']}"
                    })
                if indicators.get('RSI_oversold'):
                    alerts.append({
                        'level': 'info',
                        'type': 'rsi_low',
                        'message': f"RSI瓒呭崠 {indicators['RSI']}"
                    })
        
        return alerts

    def format_message(self, stock, data, alerts):
        """鏍煎紡鍖栭璀︽秷鎭?""
        if not alerts:
            return None
        
        price = data['price']
        cost = stock['cost']
        change_pct = data['change_pct']
        cost_change_pct = round((price - cost) / cost * 100, 2) if cost > 0 else 0
        
        # 纭畾绾у埆
        high_priority = [a for a in alerts if a['level'] == 'warning']
        level_icon = "馃毃" if len(high_priority) >= 2 else ("鈿狅笍" if high_priority else "馃摙")
        level_text = "绱ф€? if len(high_priority) >= 2 else ("璀﹀憡" if high_priority else "鎻愰啋")
        
        # 棰滆壊鏍囪瘑
        color_icon = "馃敶" if change_pct >= 0 else "馃煝"
        profit_icon = "馃敶" if cost_change_pct >= 0 else "馃煝"
        
        msg_lines = [
            f"{level_icon}銆恵level_text}銆憑color_icon} {stock['name']} ({stock['code']})",
            "鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣",
            f"馃挵 褰撳墠浠锋牸: 楼{price:.3f} ({change_pct:+.2f}%)",
            f"馃搳 鎸佷粨鎴愭湰: 楼{cost:.3f} | 鐩堜簭: {profit_icon}{cost_change_pct:+.1f}%"
        ]
        
        # 棰勮璇︽儏
        if alerts:
            msg_lines.append("")
            msg_lines.append(f"馃幆 瑙﹀彂棰勮 ({len(alerts)}椤?:")
            for alert in alerts:
                icon = {"cost_profit": "馃幆", "cost_loss": "馃洃", "rise": "馃搱", "fall": "馃搲",
                       "volume": "馃搳", "golden_cross": "馃専", "death_cross": "鈿?,
                       "rsi_high": "馃敟", "rsi_low": "鉂勶笍"}.get(alert['type'], "鈥?)
                msg_lines.append(f"  {icon} {alert['message']}")
        
        # 鏁版嵁婧愪俊鎭?        msg_lines.append("")
        msg_lines.append(f"馃摗 鏁版嵁鏉ユ簮: {' 鈫?'.join(data.get('sources_used', ['鏈煡']))}")
        
        return "\n".join(msg_lines)

    def run_once(self):
        """鎵ц涓€娆＄洃鎺у惊鐜?""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 寮€濮嬫壂鎻?..")
        
        messages = []
        
        for stock in WATCHLIST:
            print(f"  妫€鏌?{stock['name']}...")
            
            # 鑾峰彇鏁版嵁
            data = self.get_stock_data(stock)
            
            if data['errors'] and not data['sources_used']:
                print(f"    鉂?瀹屽叏澶辫触: {'; '.join(data['errors'])}")
                continue
            
            print(f"    鉁?浠锋牸: 楼{data['price']:.3f} (鏉ユ簮: {'鈫?.join(data['sources_used'])})")
            
            # 妫€鏌ラ璀?            alerts = self.check_alerts(stock, data)
            
            if alerts:
                msg = self.format_message(stock, data, alerts)
                if msg:
                    messages.append(msg)
                    print(f"    馃敂 瑙﹀彂 {len(alerts)} 涓璀?)
                # 璁板綍棰勮娆℃暟鐢ㄤ簬鏃ユ姤
                data['alert_count'] = len(alerts)
            else:
                data['alert_count'] = 0
            
            # 淇濆瓨鏁版嵁鐢ㄤ簬鏃ユ姤
            self.daily_data[stock['code']] = data
            
            # 閿欒鎻愮ず锛堜絾涓嶅奖鍝嶅姛鑳斤級
            if data['errors'] and data['sources_used']:
                print(f"    鈿狅笍 閮ㄥ垎澶辫触: {'; '.join(data['errors'])}")
        
        return messages

    def check_and_notify_errors(self):
        """妫€鏌ユ暟鎹簮閿欒骞跺彂閫侀€氱煡"""
        notifications = []
        now = time.time()
        
        for source, fail_count in self.failed_sources.items():
            # 杩炵画澶辫触3娆′互涓婏紝鎴栧垰杩涘叆30鍒嗛挓鍐峰嵈
            if fail_count >= 3:
                # 閬垮厤閲嶅閫氱煡锛氭瘡灏忔椂鍙€氱煡涓€娆?                last_notify_key = f"error_notified_{source}"
                last_notify = getattr(self, last_notify_key, 0)
                
                if now - last_notify > 1800:  # 30鍒嗛挓鍐峰嵈
                    cooldown_end = self.source_cooldown.get(source, 0)
                    remaining = int((cooldown_end - now) / 60) if cooldown_end > now else 0
                    
                    notifications.append({
                        'source': source,
                        'fail_count': fail_count,
                        'cooldown_minutes': remaining
                    })
                    setattr(self, last_notify_key, now)
        
        return notifications
    
    def format_error_notification(self, errors):
        """鏍煎紡鍖栭敊璇€氱煡娑堟伅"""
        if not errors:
            return None
        
        lines = [
            "鈿狅笍銆愭暟鎹簮寮傚父鎻愰啋銆?,
            "鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣",
            "浠ヤ笅鏁版嵁婧愯繛缁け璐ワ紝宸茶繘鍏ュ喎鍗存湡锛?,
            ""
        ]
        
        source_names = {
            'sina': '鏂版氮璐㈢粡',
            'tencent': '鑵捐璐㈢粡', 
            'eastmoney': '涓滄柟璐㈠瘜',
            'ths': '鍚岃姳椤?
        }
        
        for err in errors:
            name = source_names.get(err['source'], err['source'])
            lines.append(f"鈥?{name}: 澶辫触{err['fail_count']}娆★紝鍐峰嵈{err['cooldown_minutes']}鍒嗛挓")
        
        lines.extend([
            "",
            "馃搳 褰撳墠鐘舵€侊細",
            "鈥?瀹炴椂浠锋牸鐩戞帶锛氭甯革紙鏂版氮/鑵捐澶囩敤锛?,
            "鈥?鎶€鏈寚鏍囩洃鎺э細鍙兘鍙楅檺锛堝潎绾?RSI/鎴愪氦閲忥級",
            "",
            "馃挕 寤鸿锛?,
            "濡傛寔缁け璐ワ紝鍙€冭檻閮ㄧ讲WARP浠ｇ悊鎴栬皟鏁磋姹傞鐜?
        ])
        
        return "\n".join(lines)

    def _reset_daily_report_flag(self):
        """閲嶇疆鏃ユ姤鍙戦€佹爣蹇楋紙鏂扮殑涓€澶╋級"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        if current_date != self.today_date:
            self.today_date = current_date
            self.daily_report_sent = False
            self.daily_data = {}
            print(f"[鏃ユ姤] 鏃ユ湡宸插垏鎹㈣嚦 {current_date}锛岄噸缃棩鎶ユ爣蹇?)

    def _check_and_send_daily_report(self, mode):
        """妫€鏌ュ苟鍙戦€佹敹鐩樻棩鎶?""
        # 閲嶇疆鏃ユ湡鏍囧織
        self._reset_daily_report_flag()
        
        # 鍙湪鏀剁洏鍚庢ā寮忎笖鏈彂閫佽繃鏃ユ姤鏃跺彂閫?        if mode != 'after_hours' or self.daily_report_sent:
            return
        
        # 妫€鏌ュ綋鍓嶆椂闂存槸鍚﹀湪15:00-15:30涔嬮棿锛堝寳浜椂闂达級
        now = datetime.now() + timedelta(hours=13)  # 杞崲涓哄寳浜椂闂?        hour, minute = now.hour, now.minute
        time_val = hour * 100 + minute
        
        if not (1500 <= time_val <= 1530):
            return
        
        # 鐢熸垚骞跺彂閫佹棩鎶?        report = self._generate_daily_report()
        if report:
            print("\n" + report)
            # TODO: 璋冪敤OpenClaw鍙戦€佹棩鎶?            self.daily_report_sent = True
            print(f"[鏃ユ姤] 鏀剁洏鏃ユ姤宸插彂閫?({now.strftime('%H:%M')})")

    def _generate_daily_report(self):
        """鐢熸垚鏀剁洏鏃ユ姤"""
        if not self.daily_data:
            return None
        
        now = datetime.now() + timedelta(hours=13)  # 鍖椾含鏃堕棿
        date_str = now.strftime('%Y-%m-%d')
        
        lines = [
            f"馃搳銆愭敹鐩樻棩鎶ャ€憑date_str}",
            "鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣",
            ""
        ]
        
        total_cost_value = 0
        total_current_value = 0
        total_day_change = 0
        alert_count = 0
        
        for stock in WATCHLIST:
            code = stock['code']
            data = self.daily_data.get(code)
            if not data:
                continue
            
            price = data['price']
            cost = stock['cost']
            change_pct = data.get('change_pct', 0)
            cost_change_pct = round((price - cost) / cost * 100, 2) if cost > 0 else 0
            
            # 璁＄畻甯傚€硷紙鍋囪鎸佷粨1涓囦唤锛?            position = 10000  # 榛樿鎸佷粨鏁伴噺
            cost_value = cost * position
            current_value = price * position
            
            total_cost_value += cost_value
            total_current_value += current_value
            total_day_change += change_pct
            
            # 棰滆壊鏍囪瘑
            profit_icon = "馃敶" if cost_change_pct >= 0 else "馃煝"
            day_icon = "馃敶" if change_pct >= 0 else "馃煝"
            
            lines.append(f"馃搱 {stock['name']} ({code})")
            lines.append(f"   鎴愭湰: 楼{cost:.3f} 鈫?鏀剁洏: 楼{price:.3f}")
            lines.append(f"   鎸佷粨鐩堜簭: {profit_icon}{cost_change_pct:+.2f}% | 鏃ュ唴娑ㄨ穼: {day_icon}{change_pct:+.2f}%")
            lines.append("")
            
            # 缁熻棰勮娆℃暟
            alert_count += data.get('alert_count', 0)
        
        # 鎬讳綋缁熻
        if total_cost_value > 0:
            total_profit_pct = round((total_current_value - total_cost_value) / total_cost_value * 100, 2)
            avg_day_change = round(total_day_change / len(WATCHLIST), 2)
            profit_icon = "馃敶" if total_profit_pct >= 0 else "馃煝"
            day_icon = "馃敶" if avg_day_change >= 0 else "馃煝"
            
            lines.append("馃搵 浠婃棩姹囨€?)
            lines.append("鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣")
            lines.append(f"馃挵 鎬绘寔浠撶泩浜? {profit_icon}{total_profit_pct:+.2f}%")
            lines.append(f"馃搳 骞冲潎鏃ュ唴娑ㄨ穼: {day_icon}{avg_day_change:+.2f}%")
            lines.append(f"馃敂 棰勮瑙﹀彂娆℃暟: {alert_count}")
            lines.append("")
        
        # 甯傚満鐐硅瘎
        if avg_day_change >= 2:
            comment = "馃殌 浠婃棩甯傚満琛ㄧ幇寮哄娍锛屽鍙釜鑲″ぇ娑?
        elif avg_day_change >= 0.5:
            comment = "馃搱 浠婃棩甯傚満鏁翠綋鍚戝ソ锛岀ǔ姝ヤ笂娑?
        elif avg_day_change > -0.5:
            comment = "鉃★笍 浠婃棩甯傚満闇囪崱鏁寸悊锛屾尝鍔ㄨ緝灏?
        elif avg_day_change > -2:
            comment = "馃搲 浠婃棩甯傚満灏忓箙鍥炶皟锛屾敞鎰忛闄?
        else:
            comment = "馃洃 浠婃棩甯傚満澶у箙涓嬭穼锛岃皑鎱庢搷浣?
        
        lines.append(f"馃挕 {comment}")
        lines.append("")
        lines.append("鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣")
        lines.append("馃搶 鏁版嵁鏉ユ簮: 鏂版氮璐㈢粡/鑵捐璐㈢粡")
        lines.append("鈴?涓嬫鏃ユ姤: 涓嬩竴浜ゆ槗鏃ユ敹鐩樺悗")
        
        return "\n".join(lines)

    def run_forever(self):
        """鎸佺画杩愯"""
        print("="*50)
        print("鑲＄エ鐩戞帶鍚姩 (V2鍙嶇埇铏紭鍖栫増)")
        print(f"鐩戞帶鏍囩殑: {len(WATCHLIST)} 鍙?)
        print(f"UA: {self.user_agent[:50]}...")
        print("="*50)
        
        while True:
            schedule = self.should_run_now()
            if not schedule['run']:
                time.sleep(60)
                continue
            
            # 鎵ц鐩戞帶
            messages = self.run_once()
            
            # 鍙戦€佹秷鎭紙杩欓噷鍙互鎺ュ叆OpenClaw娑堟伅鍙戦€侊級
            for msg in messages:
                print("\n" + msg)
                # TODO: 璋冪敤OpenClaw鍙戦€佹秷鎭?            
            # 妫€鏌ュ苟鍙戦€侀敊璇€氱煡
            error_notifications = self.check_and_notify_errors()
            if error_notifications:
                error_msg = self.format_error_notification(error_notifications)
                if error_msg:
                    print("\n" + error_msg)
                    # TODO: 璋冪敤OpenClaw鍙戦€侀敊璇€氱煡
            
            # 妫€鏌ユ槸鍚﹂渶瑕佸彂閫佹敹鐩樻棩鎶ワ紙15:00-15:30涔嬮棿锛屼笖鏈彂閫佽繃锛?            self._check_and_send_daily_report(schedule['mode'])
            
            # 绛夊緟涓嬫鎵弿锛?-10鍒嗛挓闅忔満锛?            interval = schedule.get('interval', random.randint(180, 600))
            next_time = datetime.now() + timedelta(seconds=interval)
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 涓嬫鎵弿: {next_time.strftime('%H:%M:%S')} (闂撮殧{interval//60}鍒唟interval%60}绉?")
            time.sleep(interval)


if __name__ == "__main__":
    monitor = StockAlert()
    monitor.run_forever()
