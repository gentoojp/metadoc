#!/usr/bin/env python
# encoding: utf-8

import xml.etree.ElementTree as etree
import os.path
from simple_doc import SimpleDoc
from settings import *
 
class Handbook(SimpleDoc):
    def __init__(self, info):
        super(Handbook, self).__init__(info)
        self.childs = []
        self.__set_docinfo()

    def __set_docinfo(self):
        if not self.meta_info['en_memberof']:
            self.meta_info['en_memberof'] = {'Handbook': 'Handbook'}
        else:
            self.meta_info['en_memberof']['Handbook'] = 'Handbook'
        # Parse inculde document
        try:
            tree = etree.parse(CONFIG['BASE_PATH'] + self.meta_info['file_en_path'])
            include_doc = tree.findall('.//include')
            self.childs = []
            for i in include_doc:
                meta_info = {}
                meta_info['file_en_path'] = os.path.dirname(self.meta_info['file_en_path']) + '/' + i.get('href')
                meta_info['file_id'] = i.get('href').replace('.xml', '')
                meta_info['parent'] = self.meta_info['file_id']
                meta_info['en_memberof'] = 'Handbook'
                meta_info['ja_memberof'] = 'Handbook'
                file_ja_path = meta_info['file_en_path'].replace('/en/', '/ja/')
                if file_ja_path == os.path.exists(CONFIG['BASE_PATH'] + file_ja_path):
                    meta_info['file_ja_path'] = file_ja_path
                else:
                    meta_info['file_ja_path'] = meta_info['file_en_path']
                self.childs.append(Handbook(meta_info))
        except:
            pass

    def has_child(self):
        if len(self.childs) > 0:
            return True
        else:
            return False

