Market Data Skill 闆嗘垚妯″潡
浣跨敤宸叉湁鐨?market-data skill 鑾峰彇琛屾儏鏁版嵁
"""

import json
import logging
import subprocess
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """
    闆嗘垚 market-data skill 鐨勬暟鎹幏鍙栧櫒
    """
    
    def __init__(self, skill_path: Optional[str] = None):
        if skill_path is None:
            # 榛樿鐩稿璺緞
            skill_path = Path(__file__).parent.parent.parent / "market-data"
        else:
            skill_path = Path(skill_path)
        
        self.skill_path = skill_path
        self.script_path = skill_path / "scripts" / "quote_cn_pro.py"
        
    def is_available(self) -> bool:
        """妫€鏌?market-data skill 鏄惁鍙敤"""
        return self.script_path.exists()
    
    def get_kline_data(self, code: str, count: int = 60, period: str = "day") -> Optional[pd.DataFrame]:
        """
        鑾峰彇 K 绾挎暟鎹?        
        Args:
            code: 鑲＄エ浠ｇ爜
            count: 鏁版嵁鏉℃暟
            period: 鍛ㄦ湡 (day/week/month/5min)
            
        Returns:
            DataFrame 鍖呭惈 OHLCV 鏁版嵁
        """
        if not self.is_available():
            logger.warning(f"market-data skill 涓嶅彲鐢? {self.script_path}")
            return None
        
        try:
            cmd = [
                "python3", str(self.script_path),
                code,
                "--kline",
                "--count", str(count),
                "--period", period
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.skill_path)
            )
            
            if result.returncode != 0:
                logger.warning(f"鑾峰彇 K 绾挎暟鎹け璐? {result.stderr}")
                return None
            
            # 瑙ｆ瀽杈撳嚭
            return self._parse_kline_output(result.stdout)
            
        except Exception as e:
            logger.error(f"璋冪敤 market-data skill 澶辫触: {e}")
            return None
    
    def _parse_kline_output(self, output: str) -> Optional[pd.DataFrame]:
        """瑙ｆ瀽 K 绾胯緭鍑?""
        lines = output.strip().split('\n')
        data = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('馃搱') or line.startswith('馃摗') or line.startswith('='):
                continue
            
            # 灏濊瘯瑙ｆ瀽 K 绾挎暟鎹
            # 鏍煎紡: 鏃ユ湡 寮€鐩?鏀剁洏 鏈€楂?鏈€浣?鎴愪氦閲?鎴愪氦棰?...
            parts = line.split()
            if len(parts) >= 6:
                try:
                    data.append({
                        'date': parts[0],
                        'open': float(parts[1]),
                        'close': float(parts[2]),
                        'high': float(parts[3]),
                        'low': float(parts[4]),
                        'volume': float(parts[5]),
                    })
                except (ValueError, IndexError):
                    continue
        
        if data:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            return df
        
        return None
    
    def get_daily_summary(self, code: str) -> Optional[Dict[str, Any]]:
        """
        鑾峰彇鏃ョ嚎鎬荤粨
        
        Returns:
            鍖呭惈浠锋牸銆佸潎绾跨瓑鏁版嵁鐨勫瓧鍏?        """
        if not self.is_available():
            return None
        
        try:
            cmd = [
                "python3", str(self.script_path),
                code,
                "--daily"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.skill_path)
            )
            
            if result.returncode != 0:
                return None
            
            return self._parse_daily_output(result.stdout)
            
        except Exception as e:
            logger.error(f"鑾峰彇鏃ョ嚎鏁版嵁澶辫触: {e}")
            return None
    
    def _parse_daily_output(self, output: str) -> Dict[str, Any]:
        """瑙ｆ瀽鏃ョ嚎杈撳嚭"""
        result = {}
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 鎻愬彇褰撳墠浠锋牸
            if '褰撳墠浠锋牸:' in line:
                try:
                    result['price'] = float(line.split(':')[1].split()[0])
                except:
                    pass
            
            # 鎻愬彇娑ㄨ穼骞?            elif '娑ㄨ穼:' in line:
                try:
                    parts = line.split(':')[1].strip()
                    if '+' in parts:
                        result['change_pct'] = float(parts.split('%')[0].replace('+', ''))
                    elif '-' in parts:
                        result['change_pct'] = -float(parts.split('%')[0].replace('-', ''))
                except:
                    pass
            
            # 鎻愬彇鍧囩嚎
            elif 'MA5:' in line:
                try:
                    result['ma5'] = float(line.split(':')[1].strip())
                except:
                    pass
            elif 'MA10:' in line:
                try:
                    result['ma10'] = float(line.split(':')[1].strip())
                except:
                    pass
            elif 'MA20:' in line:
                try:
                    result['ma20'] = float(line.split(':')[1].strip())
                except:
                    pass
        
        return result


def create_data_fetcher(config: Optional[Dict] = None) -> Any:
    """
    宸ュ巶鍑芥暟锛氬垱寤哄悎閫傜殑鏁版嵁鑾峰彇鍣?    
    浼樺厛浣跨敤 market-data skill锛屽鏋滀笉鍙敤鍒欏洖閫€鍒?akshare
    """
    if config is None:
        config = {}
    
    use_market_data = config.get('data', {}).get('use_market_data_skill', True)
    
    if use_market_data:
        skill_path = config.get('data', {}).get('market_data_skill_path', '../market-data')
        fetcher = MarketDataFetcher(skill_path)
        
        if fetcher.is_available():
            logger.info("浣跨敤 market-data skill 鑾峰彇鏁版嵁")
            return fetcher
        else:
            logger.warning(f"market-data skill 涓嶅彲鐢紝鍥為€€鍒?akshare")
    
    # 鍥為€€鍒?akshare
    from scripts.data_fetcher import get_daily_data, get_realtime_quote
    return None  # 浣跨敤 None 琛ㄧず浣跨敤榛樿鐨?akshare 鏂瑰紡
