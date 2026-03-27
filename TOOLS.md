# TOOLS.md - Local Notes

## SMTP邮件配置
- 邮箱: 66096170@qq.com
- 授权码: qsluszirhwibbhcb
- SMTP: smtp.qq.com:587 (SSL)
- 脚本: C:\Users\Administrator\Desktop\sendmail3.ps1

## 摄像头

## SSH

## TTS

## 扬声器/房间

## 设备昵称

---

## 股票交易注意事项
- A股T+1制度：当天买的股票当天不能卖，需下一个交易日才能卖出
- 提醒用户时必须同时说明T+1规则

## 股票数据规则
- **只做A股**：老胡只交易沪深A股，港股/外股数据只作参考
- **前缀规则**：查询A股必须明确指定 sh/sz/bj 前缀，不能让API自动匹配
  - 沪市主板：sh + 6位数代码（如 sh600019）
  - 深市主板：sz + 6位数代码（如 sz000001）
  - 北交所：bj + 6位数代码（如 bj920046）
- **腾讯API会自动匹配港股**：如不指定前缀会拿到港股而非A股
- 发送邮件时使用 PowerShell System.Net.Mail，需用 [System.Reflection.Assembly]::LoadWithPartialName("System.Net.Mail")
- 文件编码：中文txt文件用GB2312读取，再用UTF8保存
