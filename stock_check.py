import akshare as ak
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

codes = ['600352', '300033', '831330', '000988', '688295', '600487', '300499', '601168', '600893', '920046', '430046', '600114', '301638', '600089']

df = ak.stock_zh_a_spot_em()
target = df[df['代码'].isin(codes)][['代码', '名称', '最新价', '涨跌幅', '今开', '最高', '最低']]
print(target.to_string())
