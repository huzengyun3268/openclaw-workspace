$paths = @(
    "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe",
    "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe",
    "C:\Users\Administrator\AppData\Local\Programs\Python\Python310\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "C:\Program Files\Python312\python.exe",
    "C:\Program Files\Python311\python.exe",
    "C:\Users\Administrator\anaconda3\python.exe",
    "C:\Users\Administrator\miniconda3\python.exe",
    "C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe"
)
foreach ($p in $paths) {
    if (Test-Path $p) { Write-Host "FOUND: $p" }
}
Write-Host "DONE"
