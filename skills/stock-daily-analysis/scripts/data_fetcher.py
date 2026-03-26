鏁版嵁鑾峰彇妯″潡 - 鍩轰簬 akshare 鐨勫甯傚満鏁版嵁鑾峰彇
鏀寔 A鑲°€佹腐鑲°€佺編鑲¤鎯呰幏鍙?"""

import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import pandas as pd
import akshare as ak

logger = logging.getLogger(__name__)


@dataclass
class StockQuote:
    """缁熶竴瀹炴椂琛屾儏鏁版嵁缁撴瀯"""
    code: str
    name: str = ""
    price: float = 0.0
    change_pct: float = 0.0
    change_amount: float = 0.0
    volume: int = 0
    amount: float = 0.0
    open_price: float = 0.0
    high: float = 0.0
    low: float = 0.0
    pre_close: float = 0.0
    volume_ratio: Optional[float] = None
    turnover_rate: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    total_mv: Optional[float] = None
    circ_mv: Optional[float] = None


@dataclass
class ChipDistribution:
    """绛圭爜鍒嗗竷鏁版嵁"""
    profit_ratio: float = 0.0  # 鑾峰埄姣斾緥
    avg_cost: float = 0.0  # 骞冲潎鎴愭湰
    concentration_90: float = 0.0  # 90%绛圭爜闆嗕腑搴?    concentration_70: float = 0.0  # 70%绛圭爜闆嗕腑搴?

def _is_us_code(stock_code: str) -> bool:
    """鍒ゆ柇鏄惁涓虹編鑲′唬鐮侊紙1-5涓ぇ鍐欏瓧姣嶏級"""
    code = stock_code.strip().upper()
    return bool(re.match(r'^[A-Z]{1,5}(\.[A-Z])?$', code))


def _is_hk_code(stock_code: str) -> bool:
    """鍒ゆ柇鏄惁涓烘腐鑲′唬鐮侊紙5浣嶆暟瀛楋級"""
    code = stock_code.lower()
    if code.startswith('hk'):
        numeric_part = code[2:]
        return numeric_part.isdigit() and 1 <= len(numeric_part) <= 5
    return code.isdigit() and len(code) == 5


def _is_etf_code(stock_code: str) -> bool:
    """鍒ゆ柇鏄惁涓?ETF 浠ｇ爜"""
    etf_prefixes = ('51', '52', '56', '58', '15', '16', '18')
    return stock_code.startswith(etf_prefixes) and len(stock_code) == 6


def normalize_code(stock_code: str) -> tuple:
    """
    鏍囧噯鍖栬偂绁ㄤ唬鐮?    
    Returns:
        tuple: (market, code)
        - market: 'a', 'hk', 'us'
        - code: 鏍囧噯鍖栧悗鐨勪唬鐮?    """
    code = stock_code.strip()
    
    if _is_us_code(code):
        return 'us', code.upper()
    
    if _is_hk_code(code):
        # 鍘婚櫎 hk 鍓嶇紑锛岃繑鍥?浣嶆暟瀛?        if code.lower().startswith('hk'):
            code = code[2:]
        return 'hk', code.zfill(5)
    
    # A鑲￠粯璁ゅ鐞?    return 'a', code


def get_daily_data(stock_code: str, days: int = 60) -> Optional[pd.DataFrame]:
    """
    鑾峰彇鑲＄エ鏃ョ嚎鏁版嵁
    
    Args:
        stock_code: 鑲＄エ浠ｇ爜
        days: 鑾峰彇澶╂暟
        
    Returns:
        DataFrame 鍖呭惈 OHLCV 鏁版嵁锛屽け璐ヨ繑鍥?None
    """
    market, code = normalize_code(stock_code)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days * 2)
    
    try:
        if market == 'us':
            return _fetch_us_data(code, start_date, end_date)
        elif market == 'hk':
            return _fetch_hk_data(code, start_date, end_date)
        else:
            return _fetch_a_stock_data(code, start_date, end_date)
    except Exception as e:
        logger.error(f"鑾峰彇 {stock_code} 鏁版嵁澶辫触: {e}")
        return None


def _fetch_a_stock_data(stock_code: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """鑾峰彇 A 鑲℃暟鎹?""
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    if _is_etf_code(stock_code):
        df = ak.fund_etf_hist_em(
            symbol=stock_code,
            period="daily",
            start_date=start_str,
            end_date=end_str,
            adjust="qfq"
        )
    else:
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_str,
            end_date=end_str,
            adjust="qfq"
        )
    
    return _standardize_columns(df)


def _fetch_hk_data(stock_code: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """鑾峰彇娓偂鏁版嵁"""
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    df = ak.stock_hk_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_str,
        end_date=end_str,
        adjust="qfq"
    )
    
    return _standardize_columns(df)


def _fetch_us_data(stock_code: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """鑾峰彇缇庤偂鏁版嵁"""
    df = ak.stock_us_daily(symbol=stock_code, adjust="qfq")
    
    if df is None or df.empty:
        return pd.DataFrame()
    
    # 鎸夋棩鏈熻繃婊?    df['date'] = pd.to_datetime(df['date'])
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # 鏍囧噯鍖栧垪鍚?    df = df.rename(columns={
        'date': '鏃ユ湡',
        'open': '寮€鐩?,
        'high': '鏈€楂?,
        'low': '鏈€浣?,
        'close': '鏀剁洏',
        'volume': '鎴愪氦閲?
    })
    
    # 璁＄畻娑ㄨ穼骞呭拰鎴愪氦棰?    if '鏀剁洏' in df.columns:
        df['娑ㄨ穼骞?] = df['鏀剁洏'].pct_change() * 100
        df['娑ㄨ穼骞?] = df['娑ㄨ穼骞?].fillna(0)
    
    if '鎴愪氦閲? in df.columns and '鏀剁洏' in df.columns:
        df['鎴愪氦棰?] = df['鎴愪氦閲?] * df['鏀剁洏']
    
    return _standardize_columns(df)


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """鏍囧噯鍖?DataFrame 鍒楀悕"""
    if df is None or df.empty:
        return pd.DataFrame()
    
    column_mapping = {
        '鏃ユ湡': 'date',
        '寮€鐩?: 'open',
        '鏀剁洏': 'close',
        '鏈€楂?: 'high',
        '鏈€浣?: 'low',
        '鎴愪氦閲?: 'volume',
        '鎴愪氦棰?: 'amount',
        '娑ㄨ穼骞?: 'pct_chg',
    }
    
    df = df.rename(columns=column_mapping)
    
    # 纭繚鏃ユ湡鏍煎紡姝ｇ‘
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # 鏁板€艰浆鎹?    for col in ['open', 'high', 'low', 'close', 'volume', 'amount', 'pct_chg']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 鍘婚櫎绌哄€艰
    df = df.dropna(subset=['close', 'volume'])
    
    # 鎸夋棩鏈熸帓搴?    df = df.sort_values('date', ascending=True).reset_index(drop=True)
    
    return df


def get_realtime_quote(stock_code: str) -> Optional[StockQuote]:
    """
    鑾峰彇瀹炴椂琛屾儏
    
    Args:
        stock_code: 鑲＄エ浠ｇ爜
        
    Returns:
        StockQuote 瀵硅薄锛屽け璐ヨ繑鍥?None
    """
    market, code = normalize_code(stock_code)
    
    try:
        if market == 'us':
            return None  # 缇庤偂鏆備笉鏀寔瀹炴椂琛屾儏
        elif market == 'hk':
            return _get_hk_realtime_quote(code)
        else:
            return _get_a_stock_realtime_quote(code)
    except Exception as e:
        logger.warning(f"鑾峰彇瀹炴椂琛屾儏澶辫触 {stock_code}: {e}")
        return None


def _get_a_stock_realtime_quote(stock_code: str) -> Optional[StockQuote]:
    """鑾峰彇 A 鑲″疄鏃惰鎯?""
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df['浠ｇ爜'] == stock_code]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        
        return StockQuote(
            code=stock_code,
            name=str(row.get('鍚嶇О', '')),
            price=float(row.get('鏈€鏂颁环', 0)) if pd.notna(row.get('鏈€鏂颁环')) else 0,
            change_pct=float(row.get('娑ㄨ穼骞?, 0)) if pd.notna(row.get('娑ㄨ穼骞?)) else 0,
            change_amount=float(row.get('娑ㄨ穼棰?, 0)) if pd.notna(row.get('娑ㄨ穼棰?)) else 0,
            volume=int(row.get('鎴愪氦閲?, 0)) if pd.notna(row.get('鎴愪氦閲?)) else 0,
            amount=float(row.get('鎴愪氦棰?, 0)) if pd.notna(row.get('鎴愪氦棰?)) else 0,
            open_price=float(row.get('浠婂紑', 0)) if pd.notna(row.get('浠婂紑')) else 0,
            high=float(row.get('鏈€楂?, 0)) if pd.notna(row.get('鏈€楂?)) else 0,
            low=float(row.get('鏈€浣?, 0)) if pd.notna(row.get('鏈€浣?)) else 0,
            volume_ratio=float(row.get('閲忔瘮', 0)) if pd.notna(row.get('閲忔瘮')) else None,
            turnover_rate=float(row.get('鎹㈡墜鐜?, 0)) if pd.notna(row.get('鎹㈡墜鐜?)) else None,
            pe_ratio=float(row.get('甯傜泩鐜?鍔ㄦ€?, 0)) if pd.notna(row.get('甯傜泩鐜?鍔ㄦ€?)) else None,
            pb_ratio=float(row.get('甯傚噣鐜?, 0)) if pd.notna(row.get('甯傚噣鐜?)) else None,
            total_mv=float(row.get('鎬诲競鍊?, 0)) if pd.notna(row.get('鎬诲競鍊?)) else None,
            circ_mv=float(row.get('娴侀€氬競鍊?, 0)) if pd.notna(row.get('娴侀€氬競鍊?)) else None,
        )
    except Exception as e:
        logger.warning(f"鑾峰彇 A 鑲″疄鏃惰鎯呭け璐? {e}")
        return None


def _get_hk_realtime_quote(stock_code: str) -> Optional[StockQuote]:
    """鑾峰彇娓偂瀹炴椂琛屾儏"""
    try:
        df = ak.stock_hk_spot_em()
        row = df[df['浠ｇ爜'] == stock_code]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        
        return StockQuote(
            code=stock_code,
            name=str(row.get('鍚嶇О', '')),
            price=float(row.get('鏈€鏂颁环', 0)) if pd.notna(row.get('鏈€鏂颁环')) else 0,
            change_pct=float(row.get('娑ㄨ穼骞?, 0)) if pd.notna(row.get('娑ㄨ穼骞?)) else 0,
            change_amount=float(row.get('娑ㄨ穼棰?, 0)) if pd.notna(row.get('娑ㄨ穼棰?)) else 0,
            volume=int(row.get('鎴愪氦閲?, 0)) if pd.notna(row.get('鎴愪氦閲?)) else 0,
            amount=float(row.get('鎴愪氦棰?, 0)) if pd.notna(row.get('鎴愪氦棰?)) else 0,
            volume_ratio=float(row.get('閲忔瘮', 0)) if pd.notna(row.get('閲忔瘮')) else None,
            turnover_rate=float(row.get('鎹㈡墜鐜?, 0)) if pd.notna(row.get('鎹㈡墜鐜?)) else None,
            pe_ratio=float(row.get('甯傜泩鐜?, 0)) if pd.notna(row.get('甯傜泩鐜?)) else None,
            pb_ratio=float(row.get('甯傚噣鐜?, 0)) if pd.notna(row.get('甯傚噣鐜?)) else None,
        )
    except Exception as e:
        logger.warning(f"鑾峰彇娓偂瀹炴椂琛屾儏澶辫触: {e}")
        return None


def get_chip_distribution(stock_code: str) -> Optional[ChipDistribution]:
    """
    鑾峰彇绛圭爜鍒嗗竷鏁版嵁锛堜粎 A 鑲★級
    
    Args:
        stock_code: 鑲＄エ浠ｇ爜
        
    Returns:
        ChipDistribution 瀵硅薄锛屽け璐ヨ繑鍥?None
    """
    market, code = normalize_code(stock_code)
    
    if market != 'a' or _is_etf_code(code):
        return None
    
    try:
        df = ak.stock_cyq_em(symbol=code)
        
        if df is None or df.empty:
            return None
        
        latest = df.iloc[-1]
        
        return ChipDistribution(
            profit_ratio=float(latest.get('鑾峰埄姣斾緥', 0)) if pd.notna(latest.get('鑾峰埄姣斾緥')) else 0,
            avg_cost=float(latest.get('骞冲潎鎴愭湰', 0)) if pd.notna(latest.get('骞冲潎鎴愭湰')) else 0,
            concentration_90=float(latest.get('90%闆嗕腑搴?, 0)) if pd.notna(latest.get('90%闆嗕腑搴?)) else 0,
            concentration_70=float(latest.get('70%闆嗕腑搴?, 0)) if pd.notna(latest.get('70%闆嗕腑搴?)) else 0,
        )
    except Exception as e:
        logger.warning(f"鑾峰彇绛圭爜鍒嗗竷澶辫触 {stock_code}: {e}")
        return None


def get_stock_name(stock_code: str) -> str:
    """鑾峰彇鑲＄エ鍚嶇О"""
    quote = get_realtime_quote(stock_code)
    if quote and quote.name:
        return quote.name
    
    # 榛樿杩斿洖浠ｇ爜
    return stock_code
