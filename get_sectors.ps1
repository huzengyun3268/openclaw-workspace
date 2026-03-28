param([string]$endDate="20260327")
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

function Get-Mom {
    param($c, $d)
    try {
        $u = "https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58&secid=$c&klt=101&fqt=1&end=$endDate&lmt=$d"
        $r = Invoke-RestMethod $u -TimeoutSec 5
        if ($r.data.klines) {
            $kl = $r.data.klines
            $s = [double](($kl[0] -split ',')[1])
            $e = [double](($kl[-1] -split ',')[1])
            $mom = [math]::Round(($e-$s)/$s*100,2)
            $v5 = @()
            for ($i=[Math]::Max(0,$kl.Count-5); $i -lt $kl.Count; $i++) { $v5 += [double](($kl[$i] -split ',')[6]) }
            $avgV = ($v5 | Measure-Object -Average).Average
            $lv = [double](($kl[-1] -split ',')[6])
            $vr = if($avgV-gt 0){[math]::Round($lv/$avgV,2)}else{0}
            $t5 = 0
            if($kl.Count -ge 5){
                $f5=[double](($kl[$kl.Count-5] -split ',')[1])
                $l5=[double](($kl[-1] -split ',')[1])
                $t5=[math]::Round(($l5-$f5)/$f5*100,2)
            }
            Write-Output "$c|$mom|$vr|$t5"
        }
    } catch {}
}

# 板块动量 - 东方财富行业板块
# 电气设备:0.801780, 计算机:0.801760, 通信:0.801770, 机械设备:0.801730
# 医药:0.801140, 食品饮料:0.801110, 军工:0.801790, 电子:0.801060
# 汽车:0.801070, 房地产:0.801170, 化工:0.801030, 银行:1.881005
# 证券:0.801050, 白酒:0.801080, 农业:0.801010
$secList = @(
'0.801780','0.801760','0.801770','0.801730','0.801140',
'0.801110','0.801790','0.801060','0.801070','0.801170',
'0.801030','1.881005','0.801050','0.801080','0.801010'
)

foreach ($s in $secList) {
    Get-Mom $s 20
}
