# -*- coding: utf-8 -*-
"""
Created on Sun May 30 23:17:33 2021

@author: kk
"""

import openpyxl
import detailMapper

file_name = 'input.xlsx'
default_sheet_name = 'Worksheet'

mapper = detailMapper.getMapper('live')

wb = openpyxl.load_workbook(file_name)
sheet = wb[default_sheet_name]

size = len(list(sheet.columns)[1])
print(size)
range = sheet['G2': 'I{0}'.format(size)]

last_product = None
taste_list = []

def finish_taste_session():
    global last_product, taste_list, merged_products
    if not last_product:
        return
    
    count_sum = sum([item[1] for item in taste_list])
    str_list = [item[0] for item in taste_list]
    content = "/".join(str_list)
    
    
    merged = "{0}*{2}({1})".format(last_product, content,count_sum)
    
    last_product = None
    taste_list = []
    
    merged_products.append(merged)
    return merged

merged_products = []
for name, package, detail in range:
    print(name.value)
    if name.value is not None and detail.value is not None:
        # 有口味產品 第一個選擇
        finish_taste_session()
        
        last_product = name.value
        taste_list.append(mapper.map(detail.value))
    elif name.value == None and detail.value is not None:
        # 有口味產品 其他選擇
        taste_list.append(mapper.map(detail.value))
    elif name.value is not None and package.value is not None and detail.value is None:
        # 其他一般產品
        finish_taste_session()        
        pack, count = package.value.split("*")
        merged = f"{name.value}({pack.strip()})*{count.strip()}"
        merged_products.append(merged)
    else:
        # 特殊空白欄，先不做事
        pass
        
finish_taste_session()

with open('merge_product.csv', 'w') as ff:
    for p in merged_products:
        ff.write(p)
        ff.write('\n')

