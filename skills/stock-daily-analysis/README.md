> 鍩轰簬 LLM 鐨勮偂绁ㄦ櫤鑳藉垎鏋?Skill锛屼负 OpenClaw 鎻愪緵 A鑲?娓偂/缇庤偂 鎶€鏈潰鍒嗘瀽鍜?AI 鍐崇瓥寤鸿銆?
## 馃幆 椤圭洰瀹氫綅

鏈」鐩槸 [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) 鐨?**OpenClaw Skill 閫傞厤鐗?*銆?
涓庡師鐗堢浉姣旓紝鏈」鐩殑鐗圭偣锛?- 鉁?**OpenClaw 鍘熺敓闆嗘垚** - 鐩存帴浣滀负 Skill 璋冪敤
- 鉁?**妯″潡鍖栬璁?* - 鍙嫭绔嬩娇鐢ㄦ垨涓?market-data skill 閰嶅悎
- 鉁?**绠€鍖栦緷璧?* - 鏍稿績鍔熻兘闆堕厤缃嵆鍙繍琛?- 鉁?**寮€婧愬弸濂?* - MIT 鍗忚锛屾杩庤础鐚?
## 馃殌 蹇€熷紑濮?
### 瀹夎

```bash
cd ~/workspace/skills/
git clone https://github.com/yourusername/stock-daily-analysis.git

# 瀹夎渚濊禆
pip3 install akshare pandas numpy requests
```

### 閰嶇疆

```bash
cp config.example.json config.json
# 缂栬緫 config.json 濉叆浣犵殑 API Key
```

### 浣跨敤

```python
from scripts.analyzer import analyze_stock, analyze_stocks

# 鍒嗘瀽鍗曞彧鑲＄エ
result = analyze_stock('600519')
print(result['ai_analysis']['operation_advice'])  # 涔板叆/鎸佹湁/瑙傛湜

# 鍒嗘瀽澶氬彧鑲＄エ
results = analyze_stocks(['600519', 'AAPL', '00700'])
```

## 馃搳 鍔熻兘鐗规€?
| 鍔熻兘 | 鐘舵€?| 璇存槑 |
|------|------|------|
| A鑲″垎鏋?| 鉁?| 鏀寔涓偂銆丒TF |
| 娓偂鍒嗘瀽 | 鉁?| 鏀寔娓偂閫氭爣鐨?|
| 缇庤偂鍒嗘瀽 | 鉁?| 鍩虹琛屾儏鑾峰彇 |
| 鎶€鏈潰鍒嗘瀽 | 鉁?| MA/MACD/RSI/涔栫鐜?|
| AI 鍐崇瓥寤鸿 | 鉁?| DeepSeek/Gemini |
| 甯傚満鏁版嵁婧愰泦鎴?| 鉁?| 鍙€?[market-data skill](https://github.com/chjm-ai/openclaw-market-data) |

## 馃彈锔?椤圭洰缁撴瀯

```
stock-daily-analysis/
鈹溾攢鈹€ SKILL.md                 # OpenClaw Skill 瀹氫箟
鈹溾攢鈹€ README.md                # 椤圭洰鏂囨。
鈹溾攢鈹€ LICENSE                  # MIT 璁稿彲璇?鈹溾攢鈹€ config.example.json      # 閰嶇疆绀轰緥
鈹溾攢鈹€ config.json              # 鐢ㄦ埛閰嶇疆 (gitignore)
鈹溾攢鈹€ requirements.txt         # Python 渚濊禆
鈹斺攢鈹€ scripts/
    鈹溾攢鈹€ analyzer.py          # 涓诲叆鍙?    鈹溾攢鈹€ data_fetcher.py      # akshare 鏁版嵁鑾峰彇
    鈹溾攢鈹€ market_data_bridge.py # market-data skill 妗ユ帴
    鈹溾攢鈹€ trend_analyzer.py    # 鎶€鏈垎鏋愬紩鎿?    鈹溾攢鈹€ ai_analyzer.py       # AI 鍒嗘瀽妯″潡
    鈹斺攢鈹€ notifier.py          # 鎶ュ憡杈撳嚭
```

## 馃敡 閰嶇疆璇存槑

### AI 妯″瀷閰嶇疆

**DeepSeek (鎺ㄨ崘锛屽浗鍐呭彲鐢?**
```json
{
  "ai": {
    "provider": "openai",
    "api_key": "sk-your-deepseek-key",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat"
  }
}
```

**Gemini (鍏嶈垂锛岄渶浠ｇ悊)**
```json
{
  "ai": {
    "provider": "gemini",
    "api_key": "your-gemini-key",
    "model": "gemini-3-flash-preview"
  }
}
```

### 鏁版嵁婧愰厤缃?
**鏂规1锛氫娇鐢?akshare (榛樿)**
```json
{
  "data": {
    "use_market_data_skill": false
  }
}
```

**鏂规2锛氫娇鐢?market-data skill (鎺ㄨ崘鐢ㄤ簬 ETF)**
```json
{
  "data": {
    "use_market_data_skill": true,
    "market_data_skill_path": "../market-data"
  }
}
```

## 馃 涓?market-data skill 闆嗘垚

濡傛灉浣犵殑 OpenClaw 宸插畨瑁?[market-data skill](https://github.com/chjm-ai/openclaw-market-data)锛屾湰椤圭洰鍙嚜鍔ㄨ皟鐢ㄥ叾鏁版嵁婧愶細

```bash
workspace/skills/
鈹溾攢鈹€ market-data/          # 宸插畨瑁?鈹斺攢鈹€ stock-daily-analysis/ # 鏈」鐩?```

閰嶇疆 `use_market_data_skill: true` 鍚庯紝ETF 鏁版嵁灏嗛€氳繃 market-data skill 鑾峰彇锛岀ǔ瀹氭€ф洿濂姐€?
### 瀹夎 market-data skill

```bash
cd ~/workspace/skills/
git clone https://github.com/chjm-ai/openclaw-market-data.git market-data
```

### 鍚敤闆嗘垚

```json
{
  "data": {
    "use_market_data_skill": true,
    "market_data_skill_path": "../market-data"
  }
}
```

## 馃搱 杩斿洖鏁版嵁鏍煎紡

```python
{
    'code': '600519',
    'name': '璐靛窞鑼呭彴',
    'technical_indicators': {
        'trend_status': '寮哄娍澶氬ご',
        'ma5': 1500.0,
        'ma10': 1480.0,
        'ma20': 1450.0,
        'bias_ma5': 2.5,
        'macd_status': '閲戝弶',
        'rsi_status': '寮哄娍涔板叆',
        'buy_signal': '涔板叆',
        'signal_score': 75,
        'signal_reasons': [...],
        'risk_factors': [...]
    },
    'ai_analysis': {
        'sentiment_score': 75,
        'trend_prediction': '寮哄娍澶氬ご',
        'operation_advice': '涔板叆',
        'confidence_level': '楂?,
        'analysis_summary': '澶氬ご鎺掑垪 | MACD閲戝弶 | 閲忚兘閰嶅悎',
        'target_price': '1550',
        'stop_loss': '1420'
    }
}
```

## 馃洜锔?寮€鍙戣鍒?
- [ ] 鏀寔鏇村鏁版嵁婧?(Tushare, Baostock)
- [ ] 娣诲姞鏉垮潡鍒嗘瀽鍔熻兘
- [ ] 鏀寔鑷畾涔夌瓥鐣ュ洖娴?- [ ] WebUI 绠＄悊鐣岄潰
- [ ] 鏀寔鏇村鎺ㄩ€佹笭閬?
## 馃 璐＄尞鎸囧崡

娆㈣繋鎻愪氦 Issue 鍜?PR锛?
1. Fork 鏈」鐩?2. 鍒涘缓鐗规€у垎鏀?(`git checkout -b feature/AmazingFeature`)
3. 鎻愪氦鏇存敼 (`git commit -m 'Add some AmazingFeature'`)
4. 鎺ㄩ€佸垎鏀?(`git push origin feature/AmazingFeature`)
5. 鍒涘缓 Pull Request

## 鈿狅笍 鍏嶈矗澹版槑

鏈」鐩粎渚涘涔犵爺绌朵娇鐢紝涓嶆瀯鎴愪换浣曟姇璧勫缓璁€傝偂甯傛湁椋庨櫓锛屾姇璧勯渶璋ㄦ厧銆?
## 馃搫 璁稿彲璇?
MIT License - 璇﹁ [LICENSE](LICENSE) 鏂囦欢

## 馃檹 鑷磋阿

- 鏁版嵁鏉ユ簮锛歔akshare](https://github.com/akfamily/akshare)
- 鐏垫劅鏉ユ簮锛歔ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis)
- 骞冲彴鏀寔锛歔OpenClaw](https://openclaw.ai)

---

**Made with 鉂わ笍 for OpenClaw**
