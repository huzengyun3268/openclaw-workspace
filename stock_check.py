import akshare as ak
import pandas as pd

codes = ['600352', '300033', '000988', '688295', '600487', '300499', '601168', '600893', '920046', '600089', '600114', '301638']
names = {'600352':'浙江龙盛','300033':'同花顺','000988':'华工科技','688295':'中复神鹰','600487':'亨通光电','300499':'高澜股份','601168':'西部矿业','600893':'航发动力','920046':'亿能电力','600089':'特变电工','600114':'东睦股份','301638':'南网数字'}

try:
    df = ak.stock_zh_a_spot_em()
    df = df[df['代码'].isin(codes)]
    for _, row in df.iterrows():
        code = row['代码']
        if code in names:
            chg = row['涨跌幅']
            price = row['最新价']
            vol = row['成交额']/1e8
            print(f"{names[code]}({code}): 现价={price}, 涨跌%={chg}%, 成交额={vol:.2f}亿")
except Exception as e:
    print(f'Error: {e}')
