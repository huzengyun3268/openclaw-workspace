$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open("C:\Users\Administrator\.openclaw\workspace\temp_tender.doc")
    $text = $doc.Content.Text
    $doc.Close($false)
    $word.Quit()
    Write-Output $text
} catch {
    Write-Output "ERROR: $_"
    $word.Quit()
}
