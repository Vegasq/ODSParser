#!/usr/bin/python3
#
# Copyright (C) 2012 Nikolay Yakovlev
# niko.yakovlev@yandex.ru
# vegasq@gmail.com
# 14.07.2012

import zipfile
import xml.etree.ElementTree as etree
import os

class ODSParser:
    '''ODS2Array converter'''
    
    '''For result storing'''
    result = []
    
    '''XML attribs'''
    repeat = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated'
    
    '''Default ODS file'''
    ods = 'gg_text_value.ods'
    
    def __init__(self, filename = False):
        '''Make you life simpler'''
        if (filename != False):
            self.ods = filename
        self.open()
        self.row_parser()
        #parser._tostring()
    
    def open(self):
        '''Extract XML from ods'''
        z = zipfile.ZipFile(self.ods)
        z.extract('content.xml')
        tree = etree.parse('content.xml')
        self.root = tree.getroot() 
        
    def row_parser(self):
        '''
        Parse XML
        Row > Cell
        
        + columns-repeat fix
        '''
        for child in self.root[3]:
            for row in child[0]:
                single_row = {}
                elem_num = 0
                #print("---ROW------------------------------")
                for cell_elem in row:
                    #print("---CELL----------------------------")
                    # build text
                    txt = ""
                    for i in cell_elem:
                        if i.text:
                            txt = txt + i.text
                    single_row[elem_num] = txt

                    # append repeated calls
                    if(self.repeat in cell_elem.attrib and int(cell_elem.attrib[self.repeat]) < 100):
                        counter = int(cell_elem.attrib[self.repeat])
                        while counter > 1:
                            elem_num += 1
                            single_row[elem_num] = txt
                            counter = counter - 1
                    elem_num += 1
                self.result.append(single_row)
    
    def _tostring(self):
        for line in self.result:
            print(line)
            
    def get_result(self):
        os.remove('content.xml')
        return self.result
