param([string]$endDate="20260327")
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'SilentlyContinue'

function Get-Idx {
    param($c, $n)
    try {
        $u = "https://push2.eastmoney.com/api/qt/stock/get?fields=f43,f169,f170,f47,f48&secid=$c"
        $r = Invoke-RestMethod $u -TimeoutSec 5
        if ($r.data) {
            $p = [math]::Round($r.data.f43/100,2)
            $ch = [math]::Round($r.data.f169/100,2)
            $pct = [math]::Round($r.data.f170/100,2)
            $h = [math]::Round($r.data.f48/100,2)
            $l = [math]::Round($r.data.f47/100,2)
            Write-Output "$n|$p|$ch|$pct|$h|$l"
        }
    } catch {}
}

function Get-Mom {
    param($c, $n, $d)
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
            Write-Output "$n|$mom|$vr|$($kl.Count)|$t5"
        }
    } catch {}
}

Get-Idx '1.000001' 'ShangZong'
Get-Idx '0.399001' 'ShenZhong'
Get-Idx '0.399006' 'ChuangYe'
Get-Idx '1.000300' 'Hushen300'
Get-Idx '1.000905' 'Zhongzheng500'
Get-Idx '1.000852' 'Zhongzheng1000'
Get-Idx '0.399005' 'ZhongXiaoBan'
Get-Idx '1.000016' 'ShangZheng50'

Get-Mom '1.000001' 'ShangZong' 20
Get-Mom '0.399006' 'ChuangYe' 20
Get-Mom '1.000300' 'Hushen300' 20
Get-Mom '1.000905' 'Zhongzheng500' 20
Get-Mom '1.000852' 'Zhongzheng1000' 20

Get-Mom '1.000001' 'ShangZong' 60
Get-Mom '0.399006' 'ChuangYe' 60
Get-Mom '1.000300' 'Hushen300' 60
Get-Mom '1.000905' 'Zhongzheng500' 60
Get-Mom '1.000852' 'Zhongzheng1000' 60

Get-Mom '1.881005' 'YinHang' 20
Get-Mom '1.801780' 'DianQi' 20
Get-Mom '1.801760' 'JiSuanJi' 20
Get-Mom '1.801770' 'TongXin' 20
Get-Mom '1.801730' 'JiXie' 20
Get-Mom '1.801140' 'YiYao' 20
Get-Mom '1.801110' 'ShiPin' 20
Get-Mom '1.801790' 'GuoFang' 20
Get-Mom '1.801060' 'DianZi' 20
Get-Mom '1.801070' 'QiChe' 20
Get-Mom '1.801010' 'NongLin' 20
Get-Mom '1.801170' 'FangDiChan' 20
Get-Mom '1.801030' 'HuaGong' 20
Get-Mom '1.801020' 'CaiKuang' 20
Get-Mom '1.801180' 'JianZhu' 20

