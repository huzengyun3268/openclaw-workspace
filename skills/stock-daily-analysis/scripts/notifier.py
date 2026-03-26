閫氱煡/杈撳嚭澶勭悊妯″潡
璐熻矗鏍煎紡鍖栧垎鏋愭姤鍛婂苟杈撳嚭缁撴灉
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AnalysisReport:
    """鍒嗘瀽鎶ュ憡鏁版嵁缁撴瀯"""
    code: str
    name: str
    sentiment_score: int
    trend_prediction: str
    operation_advice: str
    decision_type: str
    confidence_level: str
    technical_summary: Dict[str, Any]
    ai_analysis: Optional[str] = None
    risk_warning: str = ""
    buy_reason: str = ""
    support_levels: List[float] = None
    resistance_levels: List[float] = None
    
    def __post_init__(self):
        if self.support_levels is None:
            self.support_levels = []
        if self.resistance_levels is None:
            self.resistance_levels = []


def format_analysis_report(report: AnalysisReport) -> str:
    """
    鏍煎紡鍖栧垎鏋愭姤鍛婁负鏂囨湰
    
    Args:
        report: 鍒嗘瀽鎶ュ憡鏁版嵁
        
    Returns:
        鏍煎紡鍖栧悗鐨勬姤鍛婃枃鏈?    """
    lines = [
        f"{'='*50}",
        f"馃搳 {report.name} ({report.code}) 鍒嗘瀽鎶ュ憡",
        f"{'='*50}",
        "",
        f"銆愭牳蹇冪粨璁恒€?,
        f"  鎿嶄綔寤鸿: {report.operation_advice}",
        f"  瓒嬪娍棰勬祴: {report.trend_prediction}",
        f"  鎯呯华璇勫垎: {report.sentiment_score}/100",
        f"  缃俊搴? {report.confidence_level}",
        "",
        f"銆愭妧鏈潰鍒嗘瀽銆?,
    ]
    
    # 鎶€鏈寚鏍?    tech = report.technical_summary
    if 'current_price' in tech:
        lines.append(f"  褰撳墠浠锋牸: {tech.get('current_price', 'N/A')}")
    
    if 'ma5' in tech:
        lines.append(f"  MA5: {tech.get('ma5', 'N/A'):.2f} (涔栫鐜? {tech.get('bias_ma5', 0):+.2f}%)")
    if 'ma10' in tech:
        lines.append(f"  MA10: {tech.get('ma10', 'N/A'):.2f} (涔栫鐜? {tech.get('bias_ma10', 0):+.2f}%)")
    if 'ma20' in tech:
        lines.append(f"  MA20: {tech.get('ma20', 'N/A'):.2f}")
    
    if 'trend_status' in tech:
        lines.append(f"  瓒嬪娍鐘舵€? {tech.get('trend_status', 'N/A')}")
    
    if 'volume_status' in tech:
        lines.append(f"  閲忚兘鐘舵€? {tech.get('volume_status', 'N/A')}")
    
    if 'macd_status' in tech:
        lines.append(f"  MACD: {tech.get('macd_status', 'N/A')}")
    
    if 'rsi_status' in tech:
        lines.append(f"  RSI: {tech.get('rsi_status', 'N/A')}")
    
    lines.append("")
    
    # 鏀拺鍘嬪姏浣?    if report.support_levels:
        lines.append(f"銆愭敮鎾戜綅銆?)
        for level in report.support_levels[:3]:
            lines.append(f"  - {level:.2f}")
        lines.append("")
    
    if report.resistance_levels:
        lines.append(f"銆愬帇鍔涗綅銆?)
        for level in report.resistance_levels[:3]:
            lines.append(f"  - {level:.2f}")
        lines.append("")
    
    # 涔板叆鐞嗙敱
    if report.buy_reason:
        lines.append(f"銆愪拱鍏ョ悊鐢便€?)
        lines.append(f"  {report.buy_reason}")
        lines.append("")
    
    # 椋庨櫓璀﹀憡
    if report.risk_warning:
        lines.append(f"銆愰闄╂彁绀恒€?)
        lines.append(f"  {report.risk_warning}")
        lines.append("")
    
    # AI 鍒嗘瀽
    if report.ai_analysis:
        lines.append(f"銆怉I 鍒嗘瀽銆?)
        lines.append(f"  {report.ai_analysis}")
        lines.append("")
    
    lines.append(f"{'='*50}")
    
    return "\n".join(lines)


def format_dashboard_report(reports: List[AnalysisReport]) -> str:
    """
    鏍煎紡鍖栧喅绛栦华琛ㄧ洏鎶ュ憡锛堝鑲＄エ姹囨€伙級
    
    Args:
        reports: 鍒嗘瀽鎶ュ憡鍒楄〃
        
    Returns:
        鏍煎紡鍖栫殑浠〃鐩樻姤鍛?    """
    if not reports:
        return "鏆傛棤鍒嗘瀽鎶ュ憡"
    
    # 缁熻
    buy_count = sum(1 for r in reports if r.decision_type == 'buy')
    hold_count = sum(1 for r in reports if r.decision_type == 'hold')
    sell_count = sum(1 for r in reports if r.decision_type == 'sell')
    
    lines = [
        f"{'='*60}",
        f"馃搳 鑲＄エ鍒嗘瀽鍐崇瓥浠〃鐩?,
        f"{'='*60}",
        "",
        f"鍒嗘瀽鑲＄エ鏁? {len(reports)} 鍙?,
        f"馃煝 涔板叆: {buy_count}  馃煛 瑙傛湜: {hold_count}  馃敶 鍗栧嚭: {sell_count}",
        "",
        f"{'='*60}",
    ]
    
    for report in reports:
        emoji = "馃煝" if report.decision_type == 'buy' else "馃煛" if report.decision_type == 'hold' else "馃敶"
        lines.append(f"{emoji} {report.name} ({report.code})")
        lines.append(f"   寤鸿: {report.operation_advice} | 璇勫垎: {report.sentiment_score}/100")
        lines.append(f"   瓒嬪娍: {report.trend_prediction}")
        
        # 娣诲姞鍏抽敭鎶€鏈寚鏍?        tech = report.technical_summary
        key_info = []
        
        if 'bias_ma5' in tech:
            key_info.append(f"涔栫鐜? {tech['bias_ma5']:+.1f}%")
        if 'macd_status' in tech:
            key_info.append(f"MACD: {tech['macd_status']}")
        
        if key_info:
            lines.append(f"   鍏抽敭鎸囨爣: {' | '.join(key_info)}")
        
        lines.append("")
    
    lines.append(f"{'='*60}")
    
    return "\n".join(lines)


def create_report_from_result(result: Dict[str, Any]) -> AnalysisReport:
    """
    浠庡垎鏋愮粨鏋滃瓧鍏稿垱寤烘姤鍛婂璞?    
    Args:
        result: 鍒嗘瀽缁撴灉瀛楀吀
        
    Returns:
        AnalysisReport 瀵硅薄
    """
    technical = result.get('technical_indicators', {})
    ai_result = result.get('ai_analysis', {})
    
    # 纭畾鍐崇瓥绫诲瀷
    advice = ai_result.get('operation_advice', '瑙傛湜')
    if advice in ['涔板叆', '鍔犱粨', '寮虹儓涔板叆']:
        decision_type = 'buy'
    elif advice in ['鍗栧嚭', '鍑忎粨', '寮虹儓鍗栧嚭']:
        decision_type = 'sell'
    else:
        decision_type = 'hold'
    
    return AnalysisReport(
        code=result.get('code', ''),
        name=result.get('name', ''),
        sentiment_score=ai_result.get('sentiment_score', 50),
        trend_prediction=ai_result.get('trend_prediction', '闇囪崱'),
        operation_advice=advice,
        decision_type=decision_type,
        confidence_level=ai_result.get('confidence_level', '涓?),
        technical_summary=technical,
        ai_analysis=ai_result.get('analysis_summary', ''),
        risk_warning=ai_result.get('risk_warning', ''),
        buy_reason=ai_result.get('buy_reason', ''),
        support_levels=technical.get('support_levels', []),
        resistance_levels=technical.get('resistance_levels', []),
    )


def print_report(report: AnalysisReport) -> None:
    """鎵撳嵃鍒嗘瀽鎶ュ憡鍒版帶鍒跺彴"""
    print(format_analysis_report(report))


def print_dashboard(reports: List[AnalysisReport]) -> None:
    """鎵撳嵃鍐崇瓥浠〃鐩樺埌鎺у埗鍙?""
    print(format_dashboard_report(reports))
