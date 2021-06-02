# -*- coding: utf-8 -*-
"""
Created on Sun May 30 23:32:30 2021

@author: kk
"""

import csv


class BaseMapper():

    def __init__(self):
        with open('map_table.csv', 'r', encoding='utf-8',newline='') as table:
            rows = csv.DictReader(table)
            self.default_dict = {}
            for row in rows:
                key = row['full_name'].strip()
                value = row['simple_name'].strip()
                self.default_dict[key] = value
        print(self.default_dict)
        pass

    def map(self, taste):
        product, subNum = taste.split("/")
        sub, num = subNum.split('*')

        simple_word = self.simpleDictMap(sub)

        return (f'{simple_word}{num}', int(num))

    def simpleDictMap(self, sub):

        live = {
            '脆皮油雞腿': '油',
            '功夫醉雞腿': '醉',
            '軟嫩牛腱': '腱',
            '香Q牛筋': '筋',
            '檸檬原汁冰磚隨手包': '檸',
            '金桔檸檬冰磚隨手包': '桔',
        }
        simple_name = self.default_dict.get(sub, live.get(sub, 'NoItem'))
        return simple_name


def getMapper(platform):
    return BaseMapper()
