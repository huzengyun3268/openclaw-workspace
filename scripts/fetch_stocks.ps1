$headers = @{
    'User-Agent' = 'Mozilla/5.0'
    'Referer' = 'https://finance.sina.com.cn'
}
$codes = "sh600352,sz300033,bj831330,sh601168,sh600893,bj920046,bj430046,sh688295,sh600089,sh600114,sz301638"
try {
    $r = Invoke-WebRequest -Uri "https://hq.sinajs.cn/list=$codes" -Headers $headers -TimeoutSec 10
    $text = [System.Text.Encoding]::GetEncoding('GBK').GetString($r.Content)
    Write-Output $text
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
}
