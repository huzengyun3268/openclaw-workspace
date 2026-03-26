AI 鍒嗘瀽妯″潡 - 璋冪敤 Gemini/OpenAI 杩涜娣卞害鍒嗘瀽
"""

import json
import logging
from typing import Dict, Any, Optional

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI 鍒嗘瀽鍣?- 鏀寔 Gemini 鍜?OpenAI"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get('provider', 'gemini')
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'gemini-3-flash-preview')
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 4096)
        
        if self.provider == 'openai' and HAS_OPENAI:
            base_url = config.get('base_url', 'https://api.openai.com/v1')
            self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        else:
            self.client = None
    
    def analyze(self, code: str, name: str, technical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        浣跨敤 AI 杩涜娣卞害鍒嗘瀽
        
        Args:
            code: 鑲＄エ浠ｇ爜
            name: 鑲＄エ鍚嶇О
            technical_data: 鎶€鏈寚鏍囨暟鎹?            
        Returns:
            AI 鍒嗘瀽缁撴灉
        """
        if not self.api_key:
            logger.warning("鏈厤缃?API Key锛岃烦杩?AI 鍒嗘瀽")
            return self._default_analysis()
        
        try:
            if self.provider == 'gemini':
                return self._analyze_with_gemini(code, name, technical_data)
            else:
                return self._analyze_with_openai(code, name, technical_data)
        except Exception as e:
            logger.error(f"AI 鍒嗘瀽澶辫触: {e}")
            return self._default_analysis()
    
    def _analyze_with_gemini(self, code: str, name: str, tech: Dict[str, Any]) -> Dict[str, Any]:
        """浣跨敤 Gemini API"""
        import requests
        import os
        
        prompt = self._build_prompt(code, name, tech)
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens
            }
        }
        
        # 浠ｇ悊璁剧疆
        proxies = {}
        proxy_url = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
        if proxy_url:
            proxies = {'https': proxy_url, 'http': proxy_url}
        
        response = requests.post(url, headers=headers, params=params, json=data, timeout=30, proxies=proxies)
        response.raise_for_status()
        
        result = response.json()
        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        return self._parse_ai_response(text, tech)
    
    def _analyze_with_openai(self, code: str, name: str, tech: Dict[str, Any]) -> Dict[str, Any]:
        """浣跨敤 OpenAI API"""
        if not HAS_OPENAI or not self.client:
            return self._default_analysis()
        
        prompt = self._build_prompt(code, name, tech)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        text = response.choices[0].message.content
        return self._parse_ai_response(text, tech)
    
    def _build_prompt(self, code: str, name: str, tech: Dict[str, Any]) -> str:
        """鏋勫缓 AI 鎻愮ず璇?""
        
        return f"""浣犳槸涓€浣嶄笓涓氱殑鑲＄エ鍒嗘瀽甯堬紝璇锋牴鎹互涓嬫妧鏈寚鏍囩粰鍑烘姇璧勫缓璁€?
鑲＄エ: {name} ({code})

鎶€鏈寚鏍囨暟鎹?
- 褰撳墠浠锋牸: {tech.get('current_price', 'N/A')}
- MA5: {tech.get('ma5', 'N/A'):.2f} (涔栫鐜? {tech.get('bias_ma5', 0):+.2f}%)
- MA10: {tech.get('ma10', 'N/A'):.2f} (涔栫鐜? {tech.get('bias_ma10', 0):+.2f}%)
- MA20: {tech.get('ma20', 'N/A'):.2f}
- 瓒嬪娍鐘舵€? {tech.get('trend_status', 'N/A')}
- MACD: {tech.get('macd_status', 'N/A')} - {tech.get('macd_signal', '')}
- RSI: {tech.get('rsi_status', 'N/A')} - {tech.get('rsi_signal', '')}
- 閲忚兘: {tech.get('volume_status', 'N/A')} - {tech.get('volume_trend', '')}
- 鎶€鏈潰璇勫垎: {tech.get('signal_score', 0)}/100
- 涔板叆淇″彿: {tech.get('buy_signal', 'N/A')}
- 涔板叆鐞嗙敱: {', '.join(tech.get('signal_reasons', []))}
- 椋庨櫓鍥犵礌: {', '.join(tech.get('risk_factors', []))}

璇疯緭鍑轰互涓?JSON 鏍煎紡鐨勫垎鏋愮粨鏋?
{{
    "sentiment_score": 0-100,
    "trend_prediction": "涓婃定/涓嬭穼/闇囪崱",
    "operation_advice": "涔板叆/鎸佹湁/瑙傛湜/鍗栧嚭",
    "confidence_level": "楂?涓?浣?,
    "analysis_summary": "涓€鍙ヨ瘽鏍稿績缁撹",
    "buy_reason": "鍏蜂綋涔板叆鐞嗙敱",
    "risk_warning": "椋庨櫓鎻愮ず",
    "target_price": "鐩爣浠?,
    "stop_loss": "姝㈡崯浠?
}}

鍙緭鍑?JSON锛屼笉瑕佸叾浠栧唴瀹广€?""
    
    def _parse_ai_response(self, text: str, tech: Dict[str, Any]) -> Dict[str, Any]:
        """瑙ｆ瀽 AI 鍝嶅簲"""
        try:
            # 灏濊瘯鎻愬彇 JSON
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    'sentiment_score': result.get('sentiment_score', tech.get('signal_score', 50)),
                    'trend_prediction': result.get('trend_prediction', tech.get('trend_status', '闇囪崱')),
                    'operation_advice': result.get('operation_advice', tech.get('buy_signal', '瑙傛湜')),
                    'confidence_level': result.get('confidence_level', '涓?),
                    'analysis_summary': result.get('analysis_summary', ''),
                    'buy_reason': result.get('buy_reason', ''),
                    'risk_warning': result.get('risk_warning', ''),
                    'target_price': result.get('target_price', ''),
                    'stop_loss': result.get('stop_loss', '')
                }
        except Exception as e:
            logger.warning(f"瑙ｆ瀽 AI 鍝嶅簲澶辫触: {e}")
        
        # 鍥為€€鍒板熀浜庢妧鏈潰鐨勯粯璁ゅ垎鏋?        return self._default_analysis_from_tech(tech)
    
    def _default_analysis_from_tech(self, tech: Dict[str, Any]) -> Dict[str, Any]:
        """鍩轰簬鎶€鏈潰鐨勯粯璁ゅ垎鏋?""
        score = tech.get('signal_score', 50)
        buy_signal = tech.get('buy_signal', '瑙傛湜')
        
        return {
            'sentiment_score': score,
            'trend_prediction': tech.get('trend_status', '闇囪崱'),
            'operation_advice': buy_signal,
            'confidence_level': '楂? if score >= 70 else '涓? if score >= 50 else '浣?,
            'analysis_summary': ' | '.join(tech.get('signal_reasons', []))[:100],
            'buy_reason': ', '.join(tech.get('signal_reasons', [])),
            'risk_warning': ' | '.join(tech.get('risk_factors', [])),
            'target_price': '',
            'stop_loss': ''
        }
    
    def _default_analysis(self) -> Dict[str, Any]:
        """榛樿鍒嗘瀽缁撴灉"""
        return {
            'sentiment_score': 50,
            'trend_prediction': '闇囪崱',
            'operation_advice': '瑙傛湜',
            'confidence_level': '浣?,
            'analysis_summary': 'AI 鍒嗘瀽鏈惎鐢?,
            'buy_reason': '',
            'risk_warning': '',
            'target_price': '',
            'stop_loss': ''
        }
