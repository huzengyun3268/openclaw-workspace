# -*- coding: utf-8 -*-
content = open(r'C:\Users\Administrator\.openclaw\workspace\stock_check2.py', 'r', encoding='utf-8').read()
content = content.replace('print(f"{name}({code}): 行情获取失败")', 'print(name + "(" + code + "): 行情获取失败")')
open(r'C:\Users\Administrator\.openclaw\workspace\stock_check2.py', 'w', encoding='utf-8').write(content)
print('done')
