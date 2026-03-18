# 每日热点扫描 - 使用浏览器获取全网热点
$date = Get-Date -Format "yyyy-MM-dd"
$outputDir = "C:\Users\Administrator\.openclaw\workspace\memory"
$outputFile = "$outputDir\hotspots_$date.md"

# 调用OpenClaw浏览器获取热点
$hotspotData = @{}

# 百度热搜
try {
    $baiduHtml = Invoke-WebRequest -Uri "https://top.baidu.com/board?tab=realtime" -UseBasicParsing -TimeoutSec 15
    if ($baiduHtml.Content -match '<div class="hero-title">([^<]+)</div>') {
        $hotspotData["百度"] = $matches[1]
    }
} catch {
    $hotspotData["百度"] = "获取失败"
}

$report = @"
# 📊 每日热点选题清单 - $date

> 生成时间: $(Get-Date -Format 'HH:mm')

---

## 🔵 百度热搜
*(top.baidu.com)*

## 🟢 微博热搜  
*(weibo.com)*

## 🔴 抖音热点
*(douyin.com)*

## 📕 小红书热点
*(xiaohongshu.com)*

---

*每天早上8点自动生成 | 通过飞书发送*
"@

$report | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "热点报告已生成: $outputFile"

# 标记今天已生成
"$outputDir\last_hotspots_date.txt" | ForEach-Object { $date | Out-File -FilePath $_ -Encoding UTF8 }
