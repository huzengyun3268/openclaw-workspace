import sys
sys.stdout.reconfigure(encoding='utf-8')
try:
    import akshare as ak
    print('akshare version:', ak.__version__)
    # Try to get quotes
    df = ak.stock_zh_a_spot_em()
    print(df.columns.tolist())
    for code in ['831330', '430046']:
        row = df[df['代码'] == code]
        if not row.empty:
            print(row[['代码', '名称', '最新价', '涨跌幅']].to_string())
except Exception as e:
    print('ERROR:', e)
