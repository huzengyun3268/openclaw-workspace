description: LLM椹卞姩鐨勬瘡鏃ヨ偂绁ㄥ垎鏋愮郴缁熴€傛敮鎸丄鑲?娓偂/缇庤偂鑷€夎偂鏅鸿兘鍒嗘瀽锛岀敓鎴愬喅绛栦华琛ㄧ洏鍜屽ぇ鐩樺鐩樻姤鍛娿€傛彁渚涙妧鏈潰鍒嗘瀽锛堝潎绾裤€丮ACD銆丷SI銆佷箹绂荤巼锛夈€佽秼鍔垮垽鏂€佷拱鍏ヤ俊鍙疯瘎鍒嗐€傚彲涓巑arket-data skill闆嗘垚鑾峰彇鏇寸ǔ瀹氱殑ETF鏁版嵁銆傝Е鍙戣瘝锛氳偂绁ㄥ垎鏋愩€佸垎鏋愯偂绁ㄣ€佹瘡鏃ュ垎鏋愩€佹妧鏈潰鍒嗘瀽銆?---

# Daily Stock Analysis for OpenClaw

鍩轰簬 LLM 鐨?A/H/缇庤偂鏅鸿兘鍒嗘瀽 Skill锛屾彁渚涙妧鏈潰鍒嗘瀽鍜?AI 鍐崇瓥寤鸿銆?
## 鍔熻兘鐗规€?
1. **澶氬競鍦烘敮鎸?* - A鑲°€佹腐鑲°€佺編鑲?2. **鎶€鏈潰鍒嗘瀽** - MA5/10/20銆丮ACD銆丷SI銆佷箹绂荤巼
3. **瓒嬪娍浜ゆ槗** - 澶氬ご鎺掑垪鍒ゆ柇銆佷拱鍏ヤ俊鍙疯瘎鍒?4. **AI 鍐崇瓥** - DeepSeek/Gemini/OpenAI 娣卞害鍒嗘瀽
5. **鏁版嵁婧愰泦鎴?* - 鍙€?market-data skill

## 蹇€熶娇鐢?
```python
from scripts.analyzer import analyze_stock, analyze_stocks

# 鍗曞彧鍒嗘瀽
result = analyze_stock('600519')
print(result['ai_analysis']['operation_advice'])

# 鎵归噺鍒嗘瀽
results = analyze_stocks(['600362', '601318', '159892'])
```

## 閰嶇疆

1. 澶嶅埗閰嶇疆妯℃澘锛?```bash
cp config.example.json config.json
```

2. 濉叆 DeepSeek API Key锛?```json
{
  "ai": {
    "provider": "openai",
    "api_key": "sk-your-deepseek-key",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat"
  }
}
```

3. (鍙€? 鍚敤 market-data skill 鏁版嵁婧愶細
```json
{
  "data": {
    "use_market_data_skill": true,
    "market_data_skill_path": "../market-data"
  }
}
```

## 杩斿洖鏁版嵁

```python
{
    'code': '600519',
    'name': '璐靛窞鑼呭彴',
    'technical_indicators': {
        'trend_status': '寮哄娍澶氬ご',
        'ma5': 1500.0, 'ma10': 1480.0, 'ma20': 1450.0,
        'bias_ma5': 2.5,
        'macd_status': '閲戝弶',
        'rsi_status': '寮哄娍涔板叆',
        'buy_signal': '涔板叆',
        'signal_score': 75
    },
    'ai_analysis': {
        'sentiment_score': 75,
        'operation_advice': '涔板叆',
        'confidence_level': '楂?,
        'target_price': '1550',
        'stop_loss': '1420'
    }
}
```

## 椤圭洰淇℃伅

- **寮€婧愬崗璁?*: MIT
- **椤圭洰鍦板潃**: https://github.com/yourusername/stock-daily-analysis
- **鍘熼」鐩?*: https://github.com/ZhuLinsen/daily_stock_analysis

---

鈿狅笍 **鍏嶈矗澹版槑**: 鏈」鐩粎渚涘涔犵爺绌讹紝涓嶆瀯鎴愭姇璧勫缓璁€傝偂甯傛湁椋庨櫓锛屾姇璧勯渶璋ㄦ厧銆?
