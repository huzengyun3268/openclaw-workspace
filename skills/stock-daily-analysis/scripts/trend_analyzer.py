瓒嬪娍浜ゆ槗鍒嗘瀽鍣?- 鍩轰簬浜ゆ槗鐞嗗康鐨勬妧鏈垎鏋?
鏍稿績鍘熷垯锛?1. 涓ヨ繘绛栫暐 - 涓嶈拷楂橈紝杩芥眰姣忕瑪浜ゆ槗鎴愬姛鐜?2. 瓒嬪娍浜ゆ槗 - MA5>MA10>MA20 澶氬ご鎺掑垪锛岄『鍔胯€屼负
3. 涔扮偣鍋忓ソ - 鍦?MA5/MA10 闄勮繎鍥炶俯涔板叆
"""

import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class TrendStatus(Enum):
    """瓒嬪娍鐘舵€佹灇涓?""
    STRONG_BULL = "寮哄娍澶氬ご"
    BULL = "澶氬ご鎺掑垪"
    WEAK_BULL = "寮卞娍澶氬ご"
    CONSOLIDATION = "鐩樻暣"
    WEAK_BEAR = "寮卞娍绌哄ご"
    BEAR = "绌哄ご鎺掑垪"
    STRONG_BEAR = "寮哄娍绌哄ご"


class VolumeStatus(Enum):
    """閲忚兘鐘舵€佹灇涓?""
    HEAVY_VOLUME_UP = "鏀鹃噺涓婃定"
    HEAVY_VOLUME_DOWN = "鏀鹃噺涓嬭穼"
    SHRINK_VOLUME_UP = "缂╅噺涓婃定"
    SHRINK_VOLUME_DOWN = "缂╅噺鍥炶皟"
    NORMAL = "閲忚兘姝ｅ父"


class BuySignal(Enum):
    """涔板叆淇″彿鏋氫妇"""
    STRONG_BUY = "寮虹儓涔板叆"
    BUY = "涔板叆"
    HOLD = "鎸佹湁"
    WAIT = "瑙傛湜"
    SELL = "鍗栧嚭"
    STRONG_SELL = "寮虹儓鍗栧嚭"


class MACDStatus(Enum):
    """MACD鐘舵€佹灇涓?""
    GOLDEN_CROSS_ZERO = "闆惰酱涓婇噾鍙?
    GOLDEN_CROSS = "閲戝弶"
    BULLISH = "澶氬ご"
    CROSSING_UP = "涓婄┛闆惰酱"
    CROSSING_DOWN = "涓嬬┛闆惰酱"
    BEARISH = "绌哄ご"
    DEATH_CROSS = "姝诲弶"


class RSIStatus(Enum):
    """RSI鐘舵€佹灇涓?""
    OVERBOUGHT = "瓒呬拱"
    STRONG_BUY = "寮哄娍涔板叆"
    NEUTRAL = "涓€?
    WEAK = "寮卞娍"
    OVERSOLD = "瓒呭崠"


@dataclass
class TrendAnalysisResult:
    """瓒嬪娍鍒嗘瀽缁撴灉"""
    code: str
    
    # 瓒嬪娍鍒ゆ柇
    trend_status: TrendStatus = TrendStatus.CONSOLIDATION
    ma_alignment: str = ""
    trend_strength: float = 0.0
    
    # 鍧囩嚎鏁版嵁
    ma5: float = 0.0
    ma10: float = 0.0
    ma20: float = 0.0
    ma60: float = 0.0
    current_price: float = 0.0
    
    # 涔栫鐜?    bias_ma5: float = 0.0
    bias_ma10: float = 0.0
    bias_ma20: float = 0.0
    
    # 閲忚兘鍒嗘瀽
    volume_status: VolumeStatus = VolumeStatus.NORMAL
    volume_ratio_5d: float = 0.0
    volume_trend: str = ""
    
    # 鏀拺鍘嬪姏
    support_ma5: bool = False
    support_ma10: bool = False
    resistance_levels: List[float] = field(default_factory=list)
    support_levels: List[float] = field(default_factory=list)
    
    # MACD 鎸囨爣
    macd_dif: float = 0.0
    macd_dea: float = 0.0
    macd_bar: float = 0.0
    macd_status: MACDStatus = MACDStatus.BULLISH
    macd_signal: str = ""
    
    # RSI 鎸囨爣
    rsi_6: float = 0.0
    rsi_12: float = 0.0
    rsi_24: float = 0.0
    rsi_status: RSIStatus = RSIStatus.NEUTRAL
    rsi_signal: str = ""
    
    # 涔板叆淇″彿
    buy_signal: BuySignal = BuySignal.WAIT
    signal_score: int = 0
    signal_reasons: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """杞崲涓哄瓧鍏?""
        return {
            'code': self.code,
            'trend_status': self.trend_status.value,
            'ma_alignment': self.ma_alignment,
            'trend_strength': self.trend_strength,
            'ma5': self.ma5,
            'ma10': self.ma10,
            'ma20': self.ma20,
            'ma60': self.ma60,
            'current_price': self.current_price,
            'bias_ma5': self.bias_ma5,
            'bias_ma10': self.bias_ma10,
            'bias_ma20': self.bias_ma20,
            'volume_status': self.volume_status.value,
            'volume_ratio_5d': self.volume_ratio_5d,
            'volume_trend': self.volume_trend,
            'support_ma5': self.support_ma5,
            'support_ma10': self.support_ma10,
            'buy_signal': self.buy_signal.value,
            'signal_score': self.signal_score,
            'signal_reasons': self.signal_reasons,
            'risk_factors': self.risk_factors,
            'macd_status': self.macd_status.value,
            'macd_signal': self.macd_signal,
            'rsi_status': self.rsi_status.value,
            'rsi_signal': self.rsi_signal,
        }


class StockTrendAnalyzer:
    """
    鑲＄エ瓒嬪娍鍒嗘瀽鍣?    
    鍩轰簬浜ゆ槗鐞嗗康锛?    1. 瓒嬪娍鍒ゆ柇 - MA5>MA10>MA20 澶氬ご鎺掑垪
    2. 涔栫鐜囨娴?- 涓嶈拷楂橈紝鍋忕 MA5 瓒呰繃 5% 涓嶄拱
    3. 閲忚兘鍒嗘瀽 - 鍋忓ソ缂╅噺鍥炶皟
    4. MACD/RSI 鎸囨爣鍒嗘瀽
    """
    
    BIAS_THRESHOLD = 5.0  # 涔栫鐜囬槇鍊?    VOLUME_SHRINK_RATIO = 0.7
    VOLUME_HEAVY_RATIO = 1.5
    MA_SUPPORT_TOLERANCE = 0.02
    
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    RSI_SHORT = 6
    RSI_MID = 12
    RSI_LONG = 24
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    
    def analyze(self, df: pd.DataFrame, code: str) -> TrendAnalysisResult:
        """
        鍒嗘瀽鑲＄エ瓒嬪娍
        
        Args:
            df: 鍖呭惈 OHLCV 鏁版嵁鐨?DataFrame
            code: 鑲＄エ浠ｇ爜
            
        Returns:
            TrendAnalysisResult 鍒嗘瀽缁撴灉
        """
        result = TrendAnalysisResult(code=code)
        
        if df is None or df.empty or len(df) < 20:
            logger.warning(f"{code} 鏁版嵁涓嶈冻锛屾棤娉曡繘琛岃秼鍔垮垎鏋?)
            result.risk_factors.append("鏁版嵁涓嶈冻锛屾棤娉曞畬鎴愬垎鏋?)
            return result
        
        # 纭繚鏁版嵁鎸夋棩鏈熸帓搴?        df = df.sort_values('date').reset_index(drop=True)
        
        # 璁＄畻鎸囨爣
        df = self._calculate_mas(df)
        df = self._calculate_macd(df)
        df = self._calculate_rsi(df)
        
        # 鑾峰彇鏈€鏂版暟鎹?        latest = df.iloc[-1]
        result.current_price = float(latest['close'])
        result.ma5 = float(latest['MA5'])
        result.ma10 = float(latest['MA10'])
        result.ma20 = float(latest['MA20'])
        result.ma60 = float(latest.get('MA60', 0))
        
        # 鍒嗘瀽鍚勯」
        self._analyze_trend(df, result)
        self._calculate_bias(result)
        self._analyze_volume(df, result)
        self._analyze_support_resistance(df, result)
        self._analyze_macd(df, result)
        self._analyze_rsi(df, result)
        self._generate_signal(result)
        
        return result
    
    def _calculate_mas(self, df: pd.DataFrame) -> pd.DataFrame:
        """璁＄畻鍧囩嚎"""
        df = df.copy()
        df['MA5'] = df['close'].rolling(window=5, min_periods=1).mean()
        df['MA10'] = df['close'].rolling(window=10, min_periods=1).mean()
        df['MA20'] = df['close'].rolling(window=20, min_periods=1).mean()
        if len(df) >= 60:
            df['MA60'] = df['close'].rolling(window=60, min_periods=1).mean()
        else:
            df['MA60'] = df['MA20']
        return df
    
    def _calculate_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """璁＄畻 MACD 鎸囨爣"""
        df = df.copy()
        
        ema_fast = df['close'].ewm(span=self.MACD_FAST, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.MACD_SLOW, adjust=False).mean()
        
        df['MACD_DIF'] = ema_fast - ema_slow
        df['MACD_DEA'] = df['MACD_DIF'].ewm(span=self.MACD_SIGNAL, adjust=False).mean()
        df['MACD_BAR'] = (df['MACD_DIF'] - df['MACD_DEA']) * 2
        
        return df
    
    def _calculate_rsi(self, df: pd.DataFrame) -> pd.DataFrame:
        """璁＄畻 RSI 鎸囨爣"""
        df = df.copy()
        
        for period in [self.RSI_SHORT, self.RSI_MID, self.RSI_LONG]:
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=period, min_periods=1).mean()
            avg_loss = loss.rolling(window=period, min_periods=1).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            df[f'RSI_{period}'] = rsi.fillna(50)
        
        return df
    
    def _analyze_trend(self, df: pd.DataFrame, result: TrendAnalysisResult) -> None:
        """鍒嗘瀽瓒嬪娍鐘舵€?""
        ma5, ma10, ma20 = result.ma5, result.ma10, result.ma20
        
        if ma5 > ma10 > ma20:
            # 妫€鏌ヨ秼鍔垮己搴?            if len(df) >= 5:
                prev = df.iloc[-5]
                prev_spread = (prev['MA5'] - prev['MA20']) / prev['MA20'] * 100 if prev['MA20'] > 0 else 0
                curr_spread = (ma5 - ma20) / ma20 * 100 if ma20 > 0 else 0
                
                if curr_spread > prev_spread and curr_spread > 5:
                    result.trend_status = TrendStatus.STRONG_BULL
                    result.ma_alignment = "寮哄娍澶氬ご鎺掑垪锛屽潎绾垮彂鏁ｄ笂琛?
                    result.trend_strength = 90
                else:
                    result.trend_status = TrendStatus.BULL
                    result.ma_alignment = "澶氬ご鎺掑垪 MA5>MA10>MA20"
                    result.trend_strength = 75
            else:
                result.trend_status = TrendStatus.BULL
                result.ma_alignment = "澶氬ご鎺掑垪 MA5>MA10>MA20"
                result.trend_strength = 75
                
        elif ma5 > ma10 and ma10 <= ma20:
            result.trend_status = TrendStatus.WEAK_BULL
            result.ma_alignment = "寮卞娍澶氬ご锛孧A5>MA10 浣?MA10鈮A20"
            result.trend_strength = 55
            
        elif ma5 < ma10 < ma20:
            if len(df) >= 5:
                prev = df.iloc[-5]
                prev_spread = (prev['MA20'] - prev['MA5']) / prev['MA5'] * 100 if prev['MA5'] > 0 else 0
                curr_spread = (ma20 - ma5) / ma5 * 100 if ma5 > 0 else 0
                
                if curr_spread > prev_spread and curr_spread > 5:
                    result.trend_status = TrendStatus.STRONG_BEAR
                    result.ma_alignment = "寮哄娍绌哄ご鎺掑垪锛屽潎绾垮彂鏁ｄ笅琛?
                    result.trend_strength = 10
                else:
                    result.trend_status = TrendStatus.BEAR
                    result.ma_alignment = "绌哄ご鎺掑垪 MA5<MA10<MA20"
                    result.trend_strength = 25
            else:
                result.trend_status = TrendStatus.BEAR
                result.ma_alignment = "绌哄ご鎺掑垪 MA5<MA10<MA20"
                result.trend_strength = 25
                
        elif ma5 < ma10 and ma10 >= ma20:
            result.trend_status = TrendStatus.WEAK_BEAR
            result.ma_alignment = "寮卞娍绌哄ご锛孧A5<MA10 浣?MA10鈮A20"
            result.trend_strength = 40
            
        else:
            result.trend_status = TrendStatus.CONSOLIDATION
            result.ma_alignment = "鍧囩嚎缂犵粫锛岃秼鍔夸笉鏄?
            result.trend_strength = 50
    
    def _calculate_bias(self, result: TrendAnalysisResult) -> None:
        """璁＄畻涔栫鐜?""
        price = result.current_price
        
        if result.ma5 > 0:
            result.bias_ma5 = (price - result.ma5) / result.ma5 * 100
        if result.ma10 > 0:
            result.bias_ma10 = (price - result.ma10) / result.ma10 * 100
        if result.ma20 > 0:
            result.bias_ma20 = (price - result.ma20) / result.ma20 * 100
    
    def _analyze_volume(self, df: pd.DataFrame, result: TrendAnalysisResult) -> None:
        """鍒嗘瀽閲忚兘"""
        if len(df) < 5:
            return
        
        latest = df.iloc[-1]
        vol_5d_avg = df['volume'].iloc[-6:-1].mean()
        
        if vol_5d_avg > 0:
            result.volume_ratio_5d = float(latest['volume']) / vol_5d_avg
        
        # 鍒ゆ柇浠锋牸鍙樺寲
        if len(df) >= 2:
            prev_close = df.iloc[-2]['close']
            price_change = (latest['close'] - prev_close) / prev_close * 100
            
            # 閲忚兘鐘舵€佸垽鏂?            if result.volume_ratio_5d >= self.VOLUME_HEAVY_RATIO:
                if price_change > 0:
                    result.volume_status = VolumeStatus.HEAVY_VOLUME_UP
                    result.volume_trend = "鏀鹃噺涓婃定锛屽澶村姏閲忓己鍔?
                else:
                    result.volume_status = VolumeStatus.HEAVY_VOLUME_DOWN
                    result.volume_trend = "鏀鹃噺涓嬭穼锛屾敞鎰忛闄?
            elif result.volume_ratio_5d <= self.VOLUME_SHRINK_RATIO:
                if price_change > 0:
                    result.volume_status = VolumeStatus.SHRINK_VOLUME_UP
                    result.volume_trend = "缂╅噺涓婃定锛屼笂鏀诲姩鑳戒笉瓒?
                else:
                    result.volume_status = VolumeStatus.SHRINK_VOLUME_DOWN
                    result.volume_trend = "缂╅噺鍥炶皟锛屾礂鐩樼壒寰佹槑鏄?
            else:
                result.volume_status = VolumeStatus.NORMAL
                result.volume_trend = "閲忚兘姝ｅ父"
    
    def _analyze_support_resistance(self, df: pd.DataFrame, result: TrendAnalysisResult) -> None:
        """鍒嗘瀽鏀拺鍘嬪姏浣?""
        price = result.current_price
        
        # 妫€鏌?MA5 鏀拺
        if result.ma5 > 0:
            ma5_distance = abs(price - result.ma5) / result.ma5
            if ma5_distance <= self.MA_SUPPORT_TOLERANCE and price >= result.ma5:
                result.support_ma5 = True
                result.support_levels.append(result.ma5)
        
        # 妫€鏌?MA10 鏀拺
        if result.ma10 > 0:
            ma10_distance = abs(price - result.ma10) / result.ma10
            if ma10_distance <= self.MA_SUPPORT_TOLERANCE and price >= result.ma10:
                result.support_ma10 = True
                if result.ma10 not in result.support_levels:
                    result.support_levels.append(result.ma10)
        
        # MA20 浣滀负閲嶈鏀拺
        if result.ma20 > 0 and price >= result.ma20:
            result.support_levels.append(result.ma20)
        
        # 杩戞湡楂樼偣浣滀负鍘嬪姏
        if len(df) >= 20:
            recent_high = df['high'].iloc[-20:].max()
            if recent_high > price:
                result.resistance_levels.append(recent_high)
    
    def _analyze_macd(self, df: pd.DataFrame, result: TrendAnalysisResult) -> None:
        """鍒嗘瀽 MACD 鎸囨爣"""
        if len(df) < self.MACD_SLOW:
            result.macd_signal = "鏁版嵁涓嶈冻"
            return
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        result.macd_dif = float(latest['MACD_DIF'])
        result.macd_dea = float(latest['MACD_DEA'])
        result.macd_bar = float(latest['MACD_BAR'])
        
        # 鍒ゆ柇閲戝弶姝诲弶
        prev_dif_dea = prev['MACD_DIF'] - prev['MACD_DEA']
        curr_dif_dea = result.macd_dif - result.macd_dea
        
        is_golden_cross = prev_dif_dea <= 0 and curr_dif_dea > 0
        is_death_cross = prev_dif_dea >= 0 and curr_dif_dea < 0
        is_crossing_up = prev['MACD_DIF'] <= 0 and result.macd_dif > 0
        is_crossing_down = prev['MACD_DIF'] >= 0 and result.macd_dif < 0
        
        if is_golden_cross and result.macd_dif > 0:
            result.macd_status = MACDStatus.GOLDEN_CROSS_ZERO
            result.macd_signal = "猸?闆惰酱涓婇噾鍙夛紝寮虹儓涔板叆淇″彿锛?
        elif is_crossing_up:
            result.macd_status = MACDStatus.CROSSING_UP
            result.macd_signal = "鈿?DIF涓婄┛闆惰酱锛岃秼鍔胯浆寮?
        elif is_golden_cross:
            result.macd_status = MACDStatus.GOLDEN_CROSS
            result.macd_signal = "鉁?閲戝弶锛岃秼鍔垮悜涓?
        elif is_death_cross:
            result.macd_status = MACDStatus.DEATH_CROSS
            result.macd_signal = "鉂?姝诲弶锛岃秼鍔垮悜涓?
        elif is_crossing_down:
            result.macd_status = MACDStatus.CROSSING_DOWN
            result.macd_signal = "鈿狅笍 DIF涓嬬┛闆惰酱锛岃秼鍔胯浆寮?
        elif result.macd_dif > 0 and result.macd_dea > 0:
            result.macd_status = MACDStatus.BULLISH
            result.macd_signal = "鉁?澶氬ご鎺掑垪锛屾寔缁笂娑?
        elif result.macd_dif < 0 and result.macd_dea < 0:
            result.macd_status = MACDStatus.BEARISH
            result.macd_signal = "鈿?绌哄ご鎺掑垪锛屾寔缁笅璺?
        else:
            result.macd_status = MACDStatus.BULLISH
            result.macd_signal = "MACD 涓€у尯鍩?
    
    def _analyze_rsi(self, df: pd.DataFrame, result: TrendAnalysisResult) -> None:
        """鍒嗘瀽 RSI 鎸囨爣"""
        if len(df) < self.RSI_LONG:
            result.rsi_signal = "鏁版嵁涓嶈冻"
            return
        
        latest = df.iloc[-1]
        
        result.rsi_6 = float(latest[f'RSI_{self.RSI_SHORT}'])
        result.rsi_12 = float(latest[f'RSI_{self.RSI_MID}'])
        result.rsi_24 = float(latest[f'RSI_{self.RSI_LONG}'])
        
        rsi_mid = result.rsi_12
        
        if rsi_mid > self.RSI_OVERBOUGHT:
            result.rsi_status = RSIStatus.OVERBOUGHT
            result.rsi_signal = f"鈿狅笍 RSI瓒呬拱({rsi_mid:.1f}>70)锛岀煭鏈熷洖璋冮闄╅珮"
        elif rsi_mid > 60:
            result.rsi_status = RSIStatus.STRONG_BUY
            result.rsi_signal = f"鉁?RSI寮哄娍({rsi_mid:.1f})锛屽澶村姏閲忓厖瓒?
        elif rsi_mid >= 40:
            result.rsi_status = RSIStatus.NEUTRAL
            result.rsi_signal = f"RSI涓€?{rsi_mid:.1f})锛岄渿鑽℃暣鐞嗕腑"
        elif rsi_mid >= self.RSI_OVERSOLD:
            result.rsi_status = RSIStatus.WEAK
            result.rsi_signal = f"鈿?RSI寮卞娍({rsi_mid:.1f})锛屽叧娉ㄥ弽寮?
        else:
            result.rsi_status = RSIStatus.OVERSOLD
            result.rsi_signal = f"猸?RSI瓒呭崠({rsi_mid:.1f}<30)锛屽弽寮规満浼氬ぇ"
    
    def _generate_signal(self, result: TrendAnalysisResult) -> None:
        """鐢熸垚涔板叆淇″彿鍜岀患鍚堣瘎鍒?""
        score = 0
        reasons = []
        risks = []
        
        # 瓒嬪娍璇勫垎锛?0鍒嗭級
        trend_scores = {
            TrendStatus.STRONG_BULL: 30,
            TrendStatus.BULL: 26,
            TrendStatus.WEAK_BULL: 18,
            TrendStatus.CONSOLIDATION: 12,
            TrendStatus.WEAK_BEAR: 8,
            TrendStatus.BEAR: 4,
            TrendStatus.STRONG_BEAR: 0,
        }
        trend_score = trend_scores.get(result.trend_status, 12)
        score += trend_score
        
        if result.trend_status in [TrendStatus.STRONG_BULL, TrendStatus.BULL]:
            reasons.append(f"鉁?{result.trend_status.value}锛岄『鍔垮仛澶?)
        elif result.trend_status in [TrendStatus.BEAR, TrendStatus.STRONG_BEAR]:
            risks.append(f"鈿狅笍 {result.trend_status.value}锛屼笉瀹滃仛澶?)
        
        # 涔栫鐜囪瘎鍒嗭紙20鍒嗭級
        bias = result.bias_ma5
        if bias < 0:
            if bias > -3:
                score += 20
                reasons.append(f"鉁?浠锋牸鐣ヤ綆浜嶮A5({bias:.1f}%)锛屽洖韪╀拱鐐?)
            elif bias > -5:
                score += 16
                reasons.append(f"鉁?浠锋牸鍥炶俯MA5({bias:.1f}%)锛岃瀵熸敮鎾?)
            else:
                score += 8
                risks.append(f"鈿狅笍 涔栫鐜囪繃澶?{bias:.1f}%)锛屽彲鑳界牬浣?)
        elif bias < 2:
            score += 18
            reasons.append(f"鉁?浠锋牸璐磋繎MA5({bias:.1f}%)锛屼粙鍏ュソ鏃舵満")
        elif bias < self.BIAS_THRESHOLD:
            score += 14
            reasons.append(f"鈿?浠锋牸鐣ラ珮浜嶮A5({bias:.1f}%)锛屽彲灏忎粨浠嬪叆")
        else:
            score += 4
            risks.append(f"鉂?涔栫鐜囪繃楂?{bias:.1f}%>5%)锛屼弗绂佽拷楂橈紒")
        
        # 閲忚兘璇勫垎锛?5鍒嗭級
        volume_scores = {
            VolumeStatus.SHRINK_VOLUME_DOWN: 15,
            VolumeStatus.HEAVY_VOLUME_UP: 12,
            VolumeStatus.NORMAL: 10,
            VolumeStatus.SHRINK_VOLUME_UP: 6,
            VolumeStatus.HEAVY_VOLUME_DOWN: 0,
        }
        vol_score = volume_scores.get(result.volume_status, 8)
        score += vol_score
        
        if result.volume_status == VolumeStatus.SHRINK_VOLUME_DOWN:
            reasons.append("鉁?缂╅噺鍥炶皟锛屼富鍔涙礂鐩?)
        elif result.volume_status == VolumeStatus.HEAVY_VOLUME_DOWN:
            risks.append("鈿狅笍 鏀鹃噺涓嬭穼锛屾敞鎰忛闄?)
        
        # 鏀拺璇勫垎锛?0鍒嗭級
        if result.support_ma5:
            score += 5
            reasons.append("鉁?MA5鏀拺鏈夋晥")
        if result.support_ma10:
            score += 5
            reasons.append("鉁?MA10鏀拺鏈夋晥")
        
        # MACD 璇勫垎锛?5鍒嗭級
        macd_scores = {
            MACDStatus.GOLDEN_CROSS_ZERO: 15,
            MACDStatus.GOLDEN_CROSS: 12,
            MACDStatus.CROSSING_UP: 10,
            MACDStatus.BULLISH: 8,
            MACDStatus.BEARISH: 2,
            MACDStatus.CROSSING_DOWN: 0,
            MACDStatus.DEATH_CROSS: 0,
        }
        macd_score = macd_scores.get(result.macd_status, 5)
        score += macd_score
        
        if result.macd_status in [MACDStatus.GOLDEN_CROSS_ZERO, MACDStatus.GOLDEN_CROSS]:
            reasons.append(f"鉁?{result.macd_signal}")
        elif result.macd_status in [MACDStatus.DEATH_CROSS, MACDStatus.CROSSING_DOWN]:
            risks.append(f"鈿狅笍 {result.macd_signal}")
        else:
            reasons.append(result.macd_signal)
        
        # RSI 璇勫垎锛?0鍒嗭級
        rsi_scores = {
            RSIStatus.OVERSOLD: 10,
            RSIStatus.STRONG_BUY: 8,
            RSIStatus.NEUTRAL: 5,
            RSIStatus.WEAK: 3,
            RSIStatus.OVERBOUGHT: 0,
        }
        rsi_score = rsi_scores.get(result.rsi_status, 5)
        score += rsi_score
        
        if result.rsi_status in [RSIStatus.OVERSOLD, RSIStatus.STRONG_BUY]:
            reasons.append(f"鉁?{result.rsi_signal}")
        elif result.rsi_status == RSIStatus.OVERBOUGHT:
            risks.append(f"鈿狅笍 {result.rsi_signal}")
        else:
            reasons.append(result.rsi_signal)
        
        # 缁煎悎鍒ゆ柇
        result.signal_score = score
        result.signal_reasons = reasons
        result.risk_factors = risks
        
        if score >= 75 and result.trend_status in [TrendStatus.STRONG_BULL, TrendStatus.BULL]:
            result.buy_signal = BuySignal.STRONG_BUY
        elif score >= 60 and result.trend_status in [TrendStatus.STRONG_BULL, TrendStatus.BULL, TrendStatus.WEAK_BULL]:
            result.buy_signal = BuySignal.BUY
        elif score >= 45:
            result.buy_signal = BuySignal.HOLD
        elif score >= 30:
            result.buy_signal = BuySignal.WAIT
        elif result.trend_status in [TrendStatus.BEAR, TrendStatus.STRONG_BEAR]:
            result.buy_signal = BuySignal.STRONG_SELL
        else:
            result.buy_signal = BuySignal.SELL


def analyze_stock(df: pd.DataFrame, code: str) -> TrendAnalysisResult:
    """渚挎嵎鍑芥暟锛氬垎鏋愬崟鍙偂绁?""
    analyzer = StockTrendAnalyzer()
    return analyzer.analyze(df, code)
