$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

$outputDir = "E:\胡氏宗谱改正版\"

$files = @(
    @{src="$outputDir\南岙胡宗谱序.p65"; name="南岙胡宗谱序"},
    @{src="$outputDir\南岙胡胡氏宗谱谱丁简介.p65"; name="南岙胡胡氏宗谱谱丁简介"},
    @{src="$outputDir\总谱世系.p65"; name="总谱世系"}
)

foreach ($f in $files) {
    $name = $f.name
    $src = $f.src
    Write-Host "Opening: $name"
    
    try {
        $doc = $word.Documents.Open($src, $false, $true, $false)
        Start-Sleep -Seconds 3
        
        # Get text
        $text = $doc.Content.Text
        Write-Host "  Got text: $($text.Length) chars"
        
        # Save as txt
        $txtPath = $outputDir + $name + "-w.txt"
        $doc.SaveAs([ref]$txtPath, [ref]2)
        Write-Host "  Saved: $txtPath"
        
        $doc.Close($false)
    } catch {
        Write-Host "  ERROR: $($_.Exception.Message)"
    }
}

$word.Quit()
Write-Host "Done"
