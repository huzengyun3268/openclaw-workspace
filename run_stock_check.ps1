chcp 65001 > $null
cd C:\Users\Administrator\.openclaw\workspace
$env:PYTHONIOENCODING = "utf-8"
python stock_check_report.py
