# -*- coding: utf-8 -*-
import akshare as ak
import inspect

funcs = [f for f in dir(ak) if not f.startswith('_')]
print("Total:", len(funcs))
stock_funcs = [f for f in funcs if 'stock' in f.lower()]
print("Stock funcs:", stock_funcs[:30])
