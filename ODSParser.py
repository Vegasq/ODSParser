#!/usr/bin/python3
#
# Copyright (C) 2012 Nikolay Yakovlev
# niko.yakovlev@yandex.ru
# vegasq@gmail.com
# 16.07.2012

import zipfile
import xml.etree.ElementTree as etree
import os

import re

class ODSParser:
    '''ODS2Array converter'''
    
    '''For result storing'''
    result = []
    
    '''XML attribs'''
    repeat = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated'

    '''Default ODS file'''
    ods = 'gg_text_value.ods'
    content = 'content.xml'
    
    def __init__(self, filename = False):
        '''Make you life simpler'''
        if (filename != False):
            self.ods = filename
        self.open()
        self.row_parser()
    
    def open(self):
        '''Extract XML from ods'''
        z = zipfile.ZipFile(self.ods)
        z.extract(self.content)

        content = open(self.content,'r')
        lines = content.read()
        content.close()

        rmtag1 = re.compile(r'<text:[^>]*>')
        rmtag2 = re.compile(r'</text:[^>]*>')
       
        lines = re.sub(rmtag1,'',lines)
        lines = re.sub(rmtag2,'',lines)

        content = open(self.content,'w')
        content.write(lines)
        content.close()

        tree = etree.parse(self.content)
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
                    text = cell_elem.text
                    if type(text) is str:
                        text = text.strip()
                        single_row[elem_num] = text

                    # append repeated calls
                    if(self.repeat in cell_elem.attrib and int(cell_elem.attrib[self.repeat]) < 100):
                        counter = int(cell_elem.attrib[self.repeat])
                        while counter > 1:
                            elem_num += 1
                            single_row[elem_num] = text
                            counter = counter - 1
                    elem_num += 1
                self.result.append(single_row)
    
    def _tostring(self):
        for line in self.result:
            print(line)
            
    def get_result(self):
        #os.remove('content.xml')
        return self.result

