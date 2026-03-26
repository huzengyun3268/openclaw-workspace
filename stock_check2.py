import akshare as ak
import warnings
warnings.filterwarnings('ignore')

# Individual stock real-time quotes
stocks = [
    ('600352', '浙江龙盛'),
    ('300033', '同花顺'),
    ('688295', '中复神鹰'),
    ('600487', '亨通光电'),
    ('300499', '高澜股份'),
    ('601168', '西部矿业'),
    ('600893', '航发动力'),
    ('600089', '特变电工'),
    ('600114', '东睦股份'),
    ('301638', '南网数字'),
]

results = []
for code, name in stocks:
    try:
        df = ak.stock_zh_a_spot()
        row = df[df['代码'] == code]
        if not row.empty:
            price = row['最新价'].values[0]
            chg_pct = row['涨跌幅'].values[0]
            results.append(f"{name}({code}): {price} ({chg_pct:+.2f}%)")
    except Exception as e:
        results.append(f"{name}({code}): 获取失败 {e}")

for r in results:
    print(r)
