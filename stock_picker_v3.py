# Smart Stock Picker - T+1 Strategy
import akshare as ak
import sys
import io

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 50)
print("Smart Stock Picker - T+1")
print("=" * 50)

print("\nLoading data...")
try:
    df = ak.stock_zh_a_spot_em()
    print(f"Got {len(df)} stocks")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Filter
print("\nFiltering...")
df_sel = df[
    (df['涨跌幅'] > 1) & 
    (df['涨跌幅'] < 7) & 
    (df['换手率'] > 3) & 
    (df['量比'] > 1.5)
].sort_values('涨跌幅', ascending=False)

print(f"Found: {len(df_sel)} stocks")

print("\n" + "=" * 50)
print("TOP 5 RECOMMENDED STOCKS")
print("=" * 50)

count = 0
for i, row in df_sel.head(15).iterrows():
    name = str(row.get('名称', ''))
    if 'ST' in name or '*ST' in name:
        continue
    code = row.get('代码', '')
    price = row.get('最新价', 0)
    change = row.get('涨跌幅', 0)
    turnover = row.get('换手率', 0)
    
    print(f"\n{count+1}. {name} ({code})")
    print(f"   Price: {price}, Change: {change}%, Turnover: {turnover}%")
    
    if change < 3:
        print("   -> Stable type (RECOMMENDED)")
    elif change < 5:
        print("   -> Balanced")
    else:
        print("   -> High risk")
    
    count += 1
    if count >= 5:
        break

print("\n" + "=" * 50)
