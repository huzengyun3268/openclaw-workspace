---
name: whisper-local
description: 本地 Whisper 语音转文字（完全免费，离线可用）。当用户发送语音消息时使用此技能将语音转换为文字。无需 API Key，不花任何费用。支持中文、英文等语言自动识别。
homepage: https://github.com/openai/whisper
metadata:
  region: CN
  language: zh
  author: local
---

# Whisper 本地语音识别

使用本地 Whisper AI 模型将语音转换为文字，完全免费、离线可用。

## 适用场景
- 微信用户发送语音消息
- 语音消息转文字
- 开车时语音输入

## 核心脚本
- 路径: `C:/tools/whisper-skill/scripts/transcribe.js`
- 模型: whisper base（支持中英文）
- 依赖: Python 3.14 + openai-whisper + ffmpeg

## 使用方式

当收到语音消息（audio file）时，运行以下命令转写：

```bash
node C:/tools/whisper-skill/scripts/transcribe.js "<音频文件路径>" <语言>
```

语言参数可选（默认中文）:
- `zh` - 中文
- `en` - 英文
- `auto` - 自动检测语言

## 输出格式
JSON格式:
```json
{
  "text": "转写出的文字内容",
  "language": "zh",
  "duration": 12.5
}
```

## 示例

```bash
node C:/tools/whisper-skill/scripts/transcribe.js "C:/temp/voice_msg.silk" zh
```

## 环境要求
- Python: `C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe`
- FFmpeg: `C:\tools\ffmpeg\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe`
- Whisper模型: `C:\tools\whisper_models`
- Node.js: 内置
