[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$stocks = @{
    '600352' = 'zhejiang longsheng'
    '300033' = 'tonghuashun'
    '831330' = 'pushidaohang'
    '000988' = 'huagongkeji'
    '688295' = 'zhongfushenying'
    '600487' = 'hengtongguangdian'
    '300499' = 'gaolangufen'
    '601168' = 'xibukuangye'
    '600893' = 'hangfadongli'
    '920046' = 'yinengdianli'
    '430046' = 'shengrunrun'
    '600114' = 'dongmugufen'
    '301638' = 'nanwangshuzi'
    '600089' = 'tebiangongdian'
}

$names_cn = @{
    '600352' = '浙江龙盛'
    '300033' = '同花顺'
    '831330' = '普适导航'
    '000988' = '华工科技'
    '688295' = '中复神鹰'
    '600487' = '亨通光电'
    '300499' = '高澜股份'
    '601168' = '西部矿业'
    '600893' = '航发动力'
    '920046' = '亿能电力'
    '430046' = '圣博润'
    '600114' = '东睦股份'
    '301638' = '南网数字'
    '600089' = '特变电工'
}

$results = @()

foreach ($code in $stocks.Keys) {
    try {
        if ($code.StartsWith('6') -or $code.StartsWith('9')) {
            $secid = "1.$code"
        } else {
            $secid = "0.$code"
        }
        $url = "https://push2.eastmoney.com/api/qt/stock/get?secid=$secid&fields=f43,f44,f45,f46,f47,f58,f60,f169,f170,f171"
        $data = Invoke-RestMethod -Uri $url -TimeoutSec 5
        if ($data.data) {
            $d = $data.data
            $price = [math]::Round($d.f43 / 100, 2)
            $pct = [math]::Round($d.f170 / 100, 2)
            $open = [math]::Round($d.f46 / 100, 2)
            $high = [math]::Round($d.f44 / 100, 2)
            $low = [math]::Round($d.f45 / 100, 2)
            $results += [PSCustomObject]@{
                code = $code
                name_cn = $names_cn[$code]
                price = $price
                pct_chg = $pct
                open = $open
                high = $high
                low = $low
            }
        }
    } catch {
        $results += [PSCustomObject]@{
            code = $code
            name_cn = $names_cn[$code]
            price = "ERR"
            pct_chg = "ERR"
            open = "-"
            high = "-"
            low = "-"
        }
    }
}

$results | Format-Table -AutoSize | Out-String -Width 200
