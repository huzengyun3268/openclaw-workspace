"""
A 鑲″競鍦烘棩鎶ヨ剼鏈?鑾峰彇澶х洏鎸囨暟銆佺儹闂ㄦ澘鍧楀拰榫欏ご鑲℃暟鎹?鏁版嵁鏉ユ簮锛氫笢鏂硅储瀵岀綉
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class AStockDailyReport:
    """A 鑲″競鍦烘棩鎶ョ敓鎴愬櫒"""
    
    # 涓滄柟璐㈠瘜 API 鍩虹 URL
    BASE_URL = "http://push2.eastmoney.com/api/qt"
    
    # 澶х洏鎸囨暟浠ｇ爜
    INDICES = {
        "涓婅瘉鎸囨暟": "1.000001",
        "娣辫瘉鎴愭寚": "0.399001",
        "鍒涗笟鏉挎寚": "0.399006",
    }
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.session = requests.Session()
        
    def _get(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """鍙戦€?GET 璇锋眰"""
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"璇锋眰澶辫触锛歿e}")
            return None
    
    def get_index_data(self) -> List[Dict]:
        """鑾峰彇澶х洏鎸囨暟鏁版嵁"""
        results = []
        for name, code in self.INDICES.items():
            try:
                url = f"{self.BASE_URL}/stock/get"
                params = {
                    "secid": code,
                    "fields": "f43,f44,f45,f46,f58,f107"
                }
                data = self._get(url, params)
                if data and data.get('data'):
                    d = data['data']
                    current = d.get('f46', 0) / 100
                    open_p = d.get('f44', 0) / 100
                    pct = d.get('f107', 0)
                    if pct == 0 and open_p > 0:
                        pct = ((current - open_p) / open_p * 100)
                    results.append({
                        "name": name,
                        "current": current,
                        "pct": pct
                    })
            except Exception as e:
                print(f"鑾峰彇{name}澶辫触锛歿e}")
        return results
    
    def get_hot_sectors(self, top_n: int = 10) -> List[Dict]:
        """鑾峰彇鐑棬鏉垮潡鎺掕"""
        try:
            url = f"{self.BASE_URL}/clist/get"
            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": "f3",
                "fs": "m:90+t:3",
                "fields": "f12,f14,f2,f3,f4"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                sectors = []
                for block in data['data']['diff']:
                    sectors.append({
                        "code": block.get('f12', ''),
                        "name": block.get('f14', ''),
                        "price": block.get('f2', 0),
                        "pct": block.get('f3', 0),
                        "change": block.get('f4', 0)
                    })
                return sectors
        except Exception as e:
            print(f"鑾峰彇鏉垮潡澶辫触锛歿e}")
        return []
    
    def get_sector_leaders(self, sector_code: str, top_n: int = 3) -> List[Dict]:
        """鑾峰彇鏉垮潡榫欏ご鑲?""
        try:
            url = f"{self.BASE_URL}/clist/get"
            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": "f3",
                "fs": f"b:{sector_code}",
                "fields": "f12,f14,f2,f3,f4"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                stocks = []
                for stock in data['data']['diff']:
                    stocks.append({
                        "code": stock.get('f12', ''),
                        "name": stock.get('f14', ''),
                        "pct": stock.get('f3', 0)
                    })
                return stocks
        except Exception as e:
            print(f"鑾峰彇{sector_code}榫欏ご鑲″け璐ワ細{e}")
        return []
    
    def get_all_time_high_stocks(self, top_n: int = 20) -> List[Dict]:
        """鑾峰彇鍒涘巻鍙叉柊楂樼殑鑲＄エ"""
        try:
            url = f"{self.BASE_URL}/clist/get"
            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": "f109",  # 鎸夊巻鍙叉柊楂樻帓搴?                "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
                "fields": "f12,f14,f2,f3,f109"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                stocks = []
                for stock in data['data']['diff']:
                    stocks.append({
                        "code": stock.get('f12', ''),
                        "name": stock.get('f14', ''),
                        "price": stock.get('f2', 0),
                        "pct": stock.get('f3', 0),
                        "high_days": stock.get('f109', 0)
                    })
                return stocks
        except Exception as e:
            print(f"鑾峰彇鍘嗗彶鏂伴珮鑲＄エ澶辫触锛歿e}")
        return []
    
    def get_continuous_high_stocks(self, days: int = 20, top_n: int = 20) -> List[Dict]:
        """鑾峰彇杩炵画鍒涙柊楂樼殑鑲＄エ锛圢 鏃ユ柊楂橈級"""
        try:
            url = f"{self.BASE_URL}/clist/get"
            # 鏍规嵁澶╂暟閫夋嫨鎺掑簭瀛楁
            fid = "f109" if days == 20 else "f193"  # f109=20 鏃ユ柊楂橈紝f193=60 鏃ユ柊楂?            params = {
                "pn": 1,
                "pz": top_n,
                "po": 1,
                "np": 1,
                "ut": "bd1d9ddb04089700cf9c27f6f7426281",
                "fltt": 2,
                "invt": 2,
                "fid": fid,
                "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23",
                "fields": "f12,f14,f2,f3,f109,f193"
            }
            data = self._get(url, params)
            if data and data.get('data') and data['data'].get('diff'):
                stocks = []
                for stock in data['data']['diff']:
                    high_20 = stock.get('f109', 0)
                    high_60 = stock.get('f193', 0)
                    # 鍙樉绀虹鍚堝ぉ鏁拌姹傜殑
                    if (days == 20 and high_20 > 0) or (days == 60 and high_60 > 0):
                        stocks.append({
                            "code": stock.get('f12', ''),
                            "name": stock.get('f14', ''),
                            "price": stock.get('f2', 0),
                            "pct": stock.get('f3', 0),
                            "high_20": high_20,
                            "high_60": high_60
                        })
                return stocks
        except Exception as e:
            print(f"鑾峰彇{days}鏃ユ柊楂樿偂绁ㄥけ璐ワ細{e}")
        return []
    
    def generate_report(self) -> str:
        """鐢熸垚瀹屾暣鐨勫競鍦烘棩鎶?""
        lines = []
        lines.append("=" * 50)
        lines.append("馃搱 A 鑲″競鍦烘棩鎶?)
        lines.append(f"馃搮 {datetime.now().strftime('%Y骞?m鏈?d鏃?%H:%M')} (Asia/Shanghai)")
        lines.append("=" * 50)
        lines.append("")
        
        # 1. 澶х洏鎸囨暟
        lines.append("銆愬ぇ鐩樻寚鏁般€?)
        indices = self.get_index_data()
        for idx in indices:
            lines.append(f"  {idx['name']}: {idx['current']:.2f} 鐐?({idx['pct']:+.2f}%)")
        if not indices:
            lines.append("  鏁版嵁鑾峰彇涓?..")
        lines.append("")
        
        # 2. 鐑棬鏉垮潡
        lines.append("銆愷煍?浠婃棩鏈€鐑澘鍧?Top 10銆?)
        sectors = self.get_hot_sectors(10)
        for i, sec in enumerate(sectors, 1):
            emoji = "馃敟" if i <= 3 else "馃搱"
            lines.append(f"  {emoji} {i}. {sec['name']}: {sec['price']:.2f} ({sec['pct']:+.2f}%)")
        if not sectors:
            lines.append("  鏁版嵁鑾峰彇涓?..")
        lines.append("")
        
        # 3. 鏉垮潡榫欏ご鑲?        lines.append("銆愷煆?鏉垮潡榫欏ご鑲°€?)
        top_sectors = sectors[:3] if len(sectors) >= 3 else sectors
        for sec in top_sectors:
            lines.append(f"\n  {sec['name']}:")
            leaders = self.get_sector_leaders(sec['code'], 3)
            for stock in leaders:
                flag = "馃殌" if stock['pct'] >= 15 else ""
                lines.append(f"    鈥?{stock['name']}({stock['code']}): {stock['pct']:+.2f}%{flag}")
        lines.append("")
        
        # 4. 甯傚満绠€璇?        lines.append("銆愬競鍦虹畝璇勩€?)
        if indices and sectors:
            sh = indices[0] if len(indices) > 0 else None
            if sh and sh['pct'] > 0:
                lines.append("  浠婃棩甯傚満鍛堢幇缁撴瀯鎬у垎鍖栫壒寰?)
            else:
                lines.append("  浠婃棩甯傚満鏁翠綋璋冩暣锛岀粨鏋勬€ф満浼氫负涓?)
            
            if sectors:
                top_sector = sectors[0]
                lines.append(f"  {top_sector['name']}棰嗘定锛屾定骞厈top_sector['pct']:+.2f}%")
                lines.append("  绉戞妧鎴愰暱鏉垮潡琛ㄧ幇娲昏穬")
        lines.append("")
        
        # 5. 鍒涘巻鍙叉柊楂樿偂绁?Top20
        lines.append("銆愷煄?鍒涘巻鍙叉柊楂樿偂绁?Top20銆?)
        ath_stocks = self.get_all_time_high_stocks(20)
        if ath_stocks:
            lines.append(f"  {'鑲＄エ':<12} {'浠ｇ爜':<10} {'鐜颁环':<10} {'娑ㄥ箙':<10}")
            lines.append("  " + "-" * 42)
            for stock in ath_stocks[:20]:
                lines.append(f"  {stock['name']:<12} {stock['code']:<10} {stock['price']:<10.2f} {stock['pct']:+.2f}%")
        else:
            lines.append("  鏆傛棤鏁版嵁鎴栦粖鏃ユ棤鍒涘巻鍙叉柊楂樿偂绁?)
        lines.append("")
        
        # 6. 杩炵画鍒涙柊楂樿偂绁?        lines.append("銆愷煋?杩炵画鍒涙柊楂樿偂绁ㄣ€?)
        high_20 = self.get_continuous_high_stocks(20, 15)
        high_60 = self.get_continuous_high_stocks(60, 15)
        
        lines.append("  銆?0 鏃ユ柊楂樸€?)
        if high_20:
            for stock in high_20[:10]:
                lines.append(f"    {stock['name']}({stock['code']}): {stock['price']:.2f} ({stock['pct']:+.2f}%)")
        else:
            lines.append("    鏆傛棤鏁版嵁")
        
        lines.append("  銆?0 鏃ユ柊楂樸€?)
        if high_60:
            for stock in high_60[:10]:
                lines.append(f"    {stock['name']}({stock['code']}): {stock['price']:.2f} ({stock['pct']:+.2f}%)")
        else:
            lines.append("    鏆傛棤鏁版嵁")
        lines.append("")
        
        lines.append("=" * 50)
        lines.append("馃挕 鏁版嵁鏉ユ簮锛氫笢鏂硅储瀵岀綉 | 浠呬緵鍙傝€冿紝涓嶆瀯鎴愭姇璧勫缓璁?)
        lines.append("鈿狅笍 椋庨櫓鎻愮ず锛氳偂甯傛湁椋庨櫓锛屾姇璧勯渶璋ㄦ厧銆傛湰鎶ュ憡浠呬緵鍙傝€冿紝涓嶆瀯鎴愪换浣曟姇璧勫缓璁€?)
        lines.append("=" * 50)
        
        return "\n".join(lines)


def main():
    """涓诲嚱鏁?""
    report = AStockDailyReport()
    print(report.generate_report())


if __name__ == "__main__":
    main()
