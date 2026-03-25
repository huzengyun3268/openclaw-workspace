# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings('ignore')
import akshare as ak

# List functions related to index
funcs = [f for f in dir(ak) if 'index' in f.lower() or 'spot' in f.lower() or 'quote' in f.lower()]
for f in funcs[:30]:
    print(f)
