#!/usr/bin/python3
#
# Copyright (C) 2012-2013 Nikolay Yakovlev
# niko.yakovlev@yandex.ru
# vegasq@gmail.com
# 11.03.2013

import zipfile
import xml.etree.ElementTree as etree
import os

import re

class ODSParser:
    '''ODS2Array converter'''

    '''For result storing'''
    result = {}

    '''XML attribs'''
    repeat = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated'
    table_name = '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name'

    '''Default ODS file'''
    ods = 'gg_text_value.ods'
    content = 'content.xml'

    remove_patterns = [
        r'<text:[^>]*>',
        r'</text:[^>]*>',
        r'<dc:date>.*?</dc:date>',
        r'<office:annotation.*?:annotation>'
    ]

    def __init__(self, filename = False):
        '''Make you life simpler'''
        if (filename != False):
            self.ods = filename
        self.open()
        self.row_parser()
        os.remove(self.content)

    def clean(self, xml):
        for pattern in self.remove_patterns:
            rmtag = re.compile(pattern)
            xml = re.sub(rmtag, '', xml)
        return xml

    def open(self):
        '''Extract XML from ods'''
        z = zipfile.ZipFile(self.ods)
        z.extract(self.content)

        content = open(self.content,'r')
        lines = content.read()
        content.close()

        lines = self.clean(lines)

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
        +  multitabs added
        '''
        for child in self.root[3]:
            ''' For each list in table '''
            for table_list in child:
                table_name = table_list.attrib.get(self.table_name)
                for row in table_list:
                    single_row = {}
                    elem_num = 0
                    #print("---ROW------------------------------")
                    for cell_elem in row:
                        #print("---CELL----------------------------")
                        text = cell_elem.text
                        if type(text) is str:
                            text = text.strip()
                            single_row[elem_num] = text

                        # append repeated cells
                        if(self.repeat in cell_elem.attrib and int(cell_elem.attrib[self.repeat]) < 100):
                            counter = int(cell_elem.attrib[self.repeat])
                            while counter > 1:
                                elem_num += 1
                                single_row[elem_num] = text
                                counter = counter - 1
                        elem_num += 1
                    try:
                        self.result[table_name].append(single_row)
                    except KeyError:
                        self.result[table_name] = []
                        self.result[table_name].append(single_row)

    def get_result(self):
        return self.result


