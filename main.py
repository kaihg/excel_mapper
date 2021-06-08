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
range = sheet['B2': 'I{0}'.format(size)]

last_product = None
taste_list = []

# unmerge all
while len(sheet.merged_cells.ranges) > 0 :
    for merged in sheet.merged_cells.ranges:
        # print(merged.coord)
        sheet.unmerge_cells(merged.coord)
wb.save('test.xlsx')

def finish_taste_session():
    global last_product, taste_list, merged_products
    if not last_product:
        return None

    count_sum = sum([item[1] for item in taste_list])
    str_list = [item[0] for item in taste_list]
    content = "/".join(str_list)

    merged = "{0}*{2}({1})".format(last_product, content, count_sum)

    last_product = None
    taste_list = []

    merged_products.append(merged)
    return merged


merged_products = []
others = []
useless_rows = []
row_idx = 1
for orderNum, cartNum, receiver, address, phone, name, package, detail in range:
    row_idx += 1
    if name.value is not None and detail.value is not None:
        # 有口味產品 第一個選擇
        merged = finish_taste_session()
        if merged:
            tail = others[-1]
            tail.value = merged
            
        taste_list.append(mapper.map(detail.value))
        last_product = name.value
        others.append(detail)
    elif name.value is None and detail.value is not None:
        # 有口味產品 其他選擇
        taste_list.append(mapper.map(detail.value))
        useless_rows.append(row_idx)
        # sheet.delete_rows(row_idx, 1)
    elif name.value is not None and package.value is not None and detail.value is None:
        # 其他一般產品
        merged = finish_taste_session()
        if merged:
            tail = others[-1]
            tail.value = merged

        pack, count = package.value.split("*")
        merged = f"{name.value}({pack.strip()})*{count.strip()}"
        # merged_products.append(merged)

        # others.append(", ".join(
        #     [str(orderNum.value), receiver.value, address.value, '"'+str(phone.value)+'"']))
        detail.value = merged
    else:
        # 特殊空白欄，砍掉
        useless_rows.append(row_idx)
        pass

merged = finish_taste_session()
if merged:
    tail = others[-1]
    tail.value = merged

for idx in reversed(useless_rows):
    # print(sheet[f'G{idx}'].value, idx)
    sheet.delete_rows(idx, 1)
# remove useless columns
sheet.delete_cols(7, 2)
sheet.delete_cols(10, 2)



wb.save('output.xlsx')

# with open('merge_product.csv', 'w', encoding='utf-8') as ff:
#     ff.write('\ufeff')
#     for info, detail in zip(others, merged_products):
#         ff.write(info)
#         ff.write(", ")
#         ff.write(detail)
#         ff.write('\n')
