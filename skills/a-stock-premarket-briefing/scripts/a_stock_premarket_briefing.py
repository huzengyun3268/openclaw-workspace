"""
A 鑲＄洏鍓嶇畝鎶ヨ剼鏈?浜ゆ槗鏃ュ紑鐩樺墠鍒嗘瀽甯傚満鏂伴椈銆佸畯瑙備簨浠讹紝鐢熸垚鎶曡祫鍙傝€冩姤鍛?
鏁版嵁鏉ユ簮锛歮ulti-search-engine + summarize
鏈€浣充娇鐢ㄦ椂鏈猴細浜ゆ槗鏃?8:00-9:15
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import subprocess
import sys


class AStockPremarketBriefing:
    """A 鑲＄洏鍓嶇畝鎶ョ敓鎴愬櫒"""
    
    # 鎼滅储鍏抽敭璇嶅垪琛?    SEARCH_QUERIES = [
        "A 鑲?鏈€鏂版秷鎭?浠婃棩",
        "缇庤仈鍌?鏈€鏂拌璇?鍔犳伅",
        "璇佺洃浼?鏂版斂 鍙戝竷",
        "鍖楀悜璧勯噾 浠婃棩 娴佸叆",
        "缇庤偂 鏄ㄥ 娑ㄨ穼 绉戞妧鑲?,
        "涓鑲?鏈€鏂?琛屾儏",
        "A 鑲?鐩樺墠 鍒嗘瀽",
        "绉戝垱鏉?鏈€鏂?鏀跨瓥",
        "鏂拌兘婧?鐢垫睜 鏈€鏂?娑堟伅",
        "AI 浜哄伐鏅鸿兘 鏈€鏂?杩涘睍",
    ]
    
    # 浼樺厛鏉ユ簮鍩熷悕
    PREFERRED_SOURCES = [
        "csrc.gov.cn",      # 璇佺洃浼?        "sse.com.cn",       # 涓婁氦鎵€
        "szse.cn",          # 娣变氦鎵€
        "xinhuanet.com",    # 鏂板崕绀?        "people.com.cn",    # 浜烘皯缃?        "caixin.com",       # 璐㈡柊
        "yicai.com",        # 涓€璐?        "stcn.com",         # 璇佸埜鏃舵姤
        "eastmoney.com",    # 涓滄柟璐㈠瘜
        "10jqka.com.cn",    # 鍚岃姳椤?    ]
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.news_items = []
        self.analysis = {}
        
    def is_trading_day(self) -> bool:
        """鍒ゆ柇鏄惁涓轰氦鏄撴棩锛堝伐浣滄棩涓旈潪鑺傚亣鏃ワ級"""
        today = datetime.now()
        # 绠€鍗曞垽鏂細鍛ㄦ湯涓嶆槸浜ゆ槗鏃?        if today.weekday() >= 5:  # 5=鍛ㄥ叚锛?=鍛ㄦ棩
            return False
        # TODO: 娣诲姞涓浗娉曞畾鑺傚亣鏃ュ垽鏂?        return True
    
    def get_search_urls(self) -> List[str]:
        """鐢熸垚鎼滅储寮曟搸 URL 鍒楄〃锛堣繃鍘?12 灏忔椂锛?""
        urls = []
        # Google 鏃堕棿杩囨护锛氳繃鍘?12 灏忔椂
        for query in self.SEARCH_QUERIES:
            encoded_query = requests.utils.quote(query)
            # Google 杩囧幓 12 灏忔椂
            urls.append(f"https://www.google.com/search?q={encoded_query}&tbs=qdr:h")
            # Bing 杩囧幓 24 灏忔椂锛堜綔涓鸿ˉ鍏咃級
            urls.append(f"https://cn.bing.com/search?q={encoded_query}")
        return urls
    
    def search_news(self) -> List[Dict]:
        """
        浣跨敤 multi-search-engine 鎼滅储鏂伴椈
        瀹為檯鎵ц闇€瑕佽皟鐢?web_fetch 宸ュ叿
        """
        print("馃攳 姝ｅ湪鎼滅储甯傚満鏂伴椈...")
        print("   鎻愮ず锛氭姝ラ闇€瑕佽皟鐢?multi-search-engine 鎶€鑳?)
        print("   鎼滅储鍏抽敭璇嶏細", ", ".join(self.SEARCH_QUERIES[:5]))
        
        # 杩欓噷杩斿洖鎼滅储鎸囦护锛屽疄闄呮悳绱㈢敱 AI 鎵ц
        search_instructions = []
        for query in self.SEARCH_QUERIES:
            search_instructions.append({
                "query": query,
                "engine": "bing_cn",  # 榛樿浣跨敤 Bing CN
                "time_filter": "past_12h"
            })
        
        return search_instructions
    
    def extract_with_summarize(self, urls: List[str]) -> List[Dict]:
        """
        浣跨敤 summarize 鎻愬彇 URL 鍐呭
        """
        print("馃搫 姝ｅ湪鎻愬彇缃戦〉鍐呭...")
        extracted = []
        
        for url in urls[:10]:  # 闄愬埗鎻愬彇鏁伴噺
            try:
                # 璋冪敤 summarize CLI
                result = subprocess.run(
                    ["summarize", url, "--extract-only", "--json"],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    extracted.append({
                        "url": url,
                        "title": data.get("title", ""),
                        "content": data.get("content", "")
                    })
            except Exception as e:
                print(f"   鎻愬彇澶辫触 {url}: {e}")
        
        return extracted
    
    def analyze_market(self, news_data: List[Dict]) -> Dict:
        """
        浣跨敤 summarize 鍒嗘瀽甯傚満
        """
        print("馃 姝ｅ湪鍒嗘瀽甯傚満...")
        
        # 鏋勫缓鍒嗘瀽鎻愮ず
        analysis_prompt = """
璇峰垎鏋愪互涓?A 鑲″競鍦虹浉鍏虫柊闂伙紝鐢熸垚鐩樺墠绠€鎶ワ細

銆愬垎鏋愯姹傘€?1. 浠婃棩涓荤嚎鍙欎簨锛? 鏉★級- 鏍稿績鎶曡祫閫昏緫
2. A 鑲″競鍦哄亸鍚戯紙澶?绌?闇囪崱锛? 缃俊搴?
3. 褰撳墠鏈€寮烘澘鍧楅娴嬶紙3 涓級
4. 鍙瀵?A 鑲℃爣鐨勬竻鍗曪紙5 涓級

銆愯緭鍑烘牸寮忋€?姣忔潯缁撹鍚庡繀椤婚檮鏉ユ簮閾炬帴銆?
銆愭柊闂绘暟鎹€?"""
        for item in news_data[:10]:
            analysis_prompt += f"- {item.get('title', '')}: {item.get('url', '')}\n"
        
        print("   鎻愮ず锛氭姝ラ闇€瑕佽皟鐢?summarize 杩涜 AI 鍒嗘瀽")
        return {"prompt": analysis_prompt}
    
    def generate_report(self) -> str:
        """鐢熸垚瀹屾暣鐨勭洏鍓嶇畝鎶?""
        lines = []
        lines.append("=" * 50)
        lines.append("馃搱 A 鑲＄洏鍓嶇畝鎶?)
        lines.append(f"馃搮 {datetime.now().strftime('%Y骞?m鏈?d鏃?%H:%M')} (Asia/Shanghai)")
        lines.append("=" * 50)
        lines.append("")
        
        # 妫€鏌ユ槸鍚︿负浜ゆ槗鏃?        if not self.is_trading_day():
            lines.append("鈿狅笍 浠婃棩涓洪潪浜ゆ槗鏃ワ紙鍛ㄦ湯鎴栬妭鍋囨棩锛?)
            lines.append("   鐩樺墠绠€鎶ヤ粎鍦ㄤ氦鏄撴棩鐢熸垚")
            lines.append("")
            lines.append("=" * 50)
            return "\n".join(lines)
        
        # 1. 鎼滅储鎸囦护
        lines.append("銆愷煍?鎼滅储鎸囦护銆?)
        lines.append("璇锋墽琛屼互涓嬫悳绱㈡煡璇紙杩囧幓 12 灏忔椂锛夛細")
        search_instructions = self.search_news()
        for i, inst in enumerate(search_instructions[:5], 1):
            lines.append(f"  {i}. {inst['query']} ({inst['engine']})")
        lines.append("")
        
        # 2. 鍒嗘瀽鎻愮ず
        lines.append("銆愷煠?鍒嗘瀽鎻愮ず銆?)
        lines.append("浣跨敤 summarize 瀵规悳绱㈢粨鏋滆繘琛屽垎鏋愶紝鐢熸垚锛?)
        lines.append("  1. 浠婃棩涓荤嚎鍙欎簨锛? 鏉★級")
        lines.append("  2. 甯傚満鍋忓悜鍒ゆ柇锛堝/绌?闇囪崱 + 缃俊搴?锛?)
        lines.append("  3. 鏈€寮烘澘鍧楅娴嬶紙3 涓級")
        lines.append("  4. 鍙瀵熸爣鐨勬竻鍗曪紙5 涓級")
        lines.append("")
        
        lines.append("=" * 50)
        lines.append("馃挕 浣跨敤璇存槑锛?)
        lines.append("   1. 鎵ц鎼滅储鎸囦护鑾峰彇鏂伴椈")
        lines.append("   2. 浣跨敤 summarize 鍒嗘瀽鏂伴椈鍐呭")
        lines.append("   3. 鐢熸垚瀹屾暣鎶ュ憡")
        lines.append("鈿狅笍 椋庨櫓鎻愮ず锛氱洏鍓嶅垎鏋愪粎渚涘弬鑰冿紝涓嶆瀯鎴愭姇璧勫缓璁?)
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def generate_full_briefing(self) -> str:
        """
        鐢熸垚瀹屾暣绠€鎶ワ紙闇€瑕?AI 閰嶅悎鎵ц鎼滅储鍜屽垎鏋愶級
        杩欐槸涓€涓寚瀵兼€ф柟娉曪紝瀹為檯鎵ц闇€瑕?AI 璋冪敤宸ュ叿
        """
        briefing = {
            "date": datetime.now().isoformat(),
            "is_trading_day": self.is_trading_day(),
            "search_queries": self.SEARCH_QUERIES,
            "preferred_sources": self.PREFERRED_SOURCES,
            "analysis_framework": {
                "main_narratives": 3,
                "market_bias": "bullish/bearish/neutral",
                "confidence_pct": "0-100",
                "top_sectors": 3,
                "watchlist_stocks": 5
            }
        }
        return json.dumps(briefing, ensure_ascii=False, indent=2)


def main():
    """涓诲嚱鏁?""
    briefing = AStockPremarketBriefing()
    
    # 妫€鏌ユ槸鍚︿负浜ゆ槗鏃?    if not briefing.is_trading_day():
        print("鈿狅笍 浠婃棩涓洪潪浜ゆ槗鏃ワ紝鐩樺墠绠€鎶ヤ粎鍦ㄤ氦鏄撴棩鐢熸垚")
        return
    
    # 鐢熸垚绠€鎶ユ鏋?    print(briefing.generate_report())
    print("\n瀹屾暣绠€鎶ユ鏋讹紙JSON锛夛細")
    print(briefing.generate_full_briefing())


if __name__ == "__main__":
    main()
