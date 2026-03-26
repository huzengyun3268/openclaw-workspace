鑲＄エ姣忔棩鍒嗘瀽 - 涓诲叆鍙ｆā鍧?
鏁村悎鏁版嵁鑾峰彇銆佹妧鏈垎鏋愬拰鎶ュ憡鐢熸垚
鎻愪緵绠€鍗曠殑璋冪敤鎺ュ彛
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

# 璁剧疆鏃ュ織
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 瀵煎叆妯″潡
from scripts.data_fetcher import get_daily_data, get_realtime_quote, get_stock_name
from scripts.trend_analyzer import StockTrendAnalyzer
from scripts.ai_analyzer import AIAnalyzer
from scripts.notifier import AnalysisReport, format_analysis_report, format_dashboard_report


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """鍔犺浇閰嶇疆鏂囦欢"""
    if config_path is None:
        skill_dir = Path(__file__).parent.parent
        config_path = skill_dir / "config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"鍔犺浇閰嶇疆鏂囦欢澶辫触: {e}锛屼娇鐢ㄩ粯璁ら厤缃?)
        return {
            "data": {"days": 60, "realtime_enabled": True},
            "analysis": {"bias_threshold": 5.0}
        }


def analyze_stock(code: str, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    鍒嗘瀽鍗曞彧鑲＄エ
    
    Args:
        code: 鑲＄エ浠ｇ爜 (濡?'600519', 'AAPL', '00700')
        config: 閰嶇疆瀛楀吀锛屽彲閫?        
    Returns:
        鍖呭惈鎶€鏈垎鏋愮粨鏋滅殑瀛楀吀
    """
    if config is None:
        config = load_config()
    
    logger.info(f"寮€濮嬪垎鏋愯偂绁? {code}")
    
    # 鑾峰彇鑲＄エ鍚嶇О
    name = get_stock_name(code)
    
    # 鑾峰彇鍘嗗彶鏁版嵁
    days = config.get('data', {}).get('days', 60)
    df = get_daily_data(code, days=days)
    
    if df is None or df.empty:
        logger.error(f"鏃犳硶鑾峰彇 {code} 鐨勬暟鎹?)
        return {
            'code': code,
            'name': name,
            'error': '鏁版嵁鑾峰彇澶辫触',
            'technical_indicators': {},
            'ai_analysis': {'operation_advice': '鏁版嵁涓嶈冻', 'sentiment_score': 0}
        }
    
    # 鎶€鏈垎鏋?    analyzer = StockTrendAnalyzer()
    trend_result = analyzer.analyze(df, code)
    
    # 鑾峰彇瀹炴椂琛屾儏
    quote = get_realtime_quote(code)
    if quote:
        name = quote.name or name
    
    # AI 娣卞害鍒嗘瀽
    ai_config = config.get('ai', {})
    ai_analyzer = AIAnalyzer(ai_config)
    ai_result = ai_analyzer.analyze(code, name, trend_result.to_dict())
    
    # 鏁村悎缁撴灉
    result = {
        'code': code,
        'name': name,
        'technical_indicators': trend_result.to_dict(),
        'ai_analysis': ai_result
    }
    
    logger.info(f"{code} 鍒嗘瀽瀹屾垚锛岃瘎鍒? {ai_result.get('sentiment_score', trend_result.signal_score)}")
    return result


def analyze_stocks(codes: List[str], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    鍒嗘瀽澶氬彧鑲＄エ
    
    Args:
        codes: 鑲＄エ浠ｇ爜鍒楄〃
        config: 閰嶇疆瀛楀吀锛屽彲閫?        
    Returns:
        鍒嗘瀽缁撴灉鍒楄〃
    """
    results = []
    for code in codes:
        try:
            result = analyze_stock(code, config)
            results.append(result)
        except Exception as e:
            logger.error(f"鍒嗘瀽 {code} 鏃跺嚭閿? {e}")
            results.append({
                'code': code,
                'name': code,
                'error': str(e),
                'ai_analysis': {'operation_advice': '鍒嗘瀽澶辫触', 'sentiment_score': 0}
            })
    
    return results


def print_analysis(codes: List[str]) -> None:
    """
    鍒嗘瀽鑲＄エ骞舵墦鍗版姤鍛?    
    Args:
        codes: 鑲＄エ浠ｇ爜鍒楄〃
    """
    results = analyze_stocks(codes)
    
    # 杞崲涓烘姤鍛婃牸寮忓苟鎵撳嵃
    reports = []
    for result in results:
        if 'error' not in result:
            from scripts.notifier import create_report_from_result
            report = create_report_from_result(result)
            reports.append(report)
    
    if reports:
        print("\n" + format_dashboard_report(reports))
        
        # 鎵撳嵃姣忎釜鑲＄エ鐨勮缁嗘姤鍛?        for report in reports:
            print("\n" + format_analysis_report(report))
    else:
        print("娌℃湁鍙樉绀虹殑鎶ュ憡")


# 渚挎嵎鍑芥暟
if __name__ == "__main__":
    # 娴嬭瘯
    print("=== 鑲＄エ姣忔棩鍒嗘瀽绯荤粺 ===\n")
    print("姝ｅ湪娴嬭瘯鍒嗘瀽鑼呭彴 (600519)...\n")
    print_analysis(['600519'])
