# -*- coding: utf-8 -*-
"""
Created on Sun May 30 23:32:30 2021

@author: kk
"""

class BaseMapper():
    
    def __init__(self):
        pass
    
    def map(self, taste):
        product, subNum = taste.split("/")
        sub, num = subNum.split('*')
        
        simple_word = self.simpleDictMap(sub)
                
        return (f'{simple_word}{num}', int(num))
    
    def simpleDictMap(self,sub):
        live = {
                '經典紐澳良': '紐',
                '泰式酸甜':'泰',
                '日式照燒':'日',
                '台式鹽酥':'鹽',
                '鮮嫩原味':'原',
                '脆皮油雞腿':'油',
                '功夫醉雞腿':'醉',
                '軟嫩牛腱':'腱',
                '香Q牛筋':'筋',
                '檸檬原汁冰磚隨手包':'檸',
                '金桔檸檬冰磚隨手包':'桔',
                }
        return live.get(sub, 'NoItem')
        
def getMapper(platform):
    return BaseMapper()
