#!/usr/bin/env python
# encoding: utf-8

import re
import os.path
import codecs
from settings import *
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/metadoc.log',
                    filemode='w')


class SimpleDoc(object):
    def __init__(self, info):
        self.meta_info = info

        if os.path.exists(CONFIG['BASE_PATH'] + self.meta_info['file_en_path']):
            self.meta_info_error = False
        else:
            self.meta_info_error = True

        if (os.path.exists(CONFIG['BASE_PATH'] + self.meta_info['file_ja_path'])) and (self.meta_info['file_en_path'] != self.meta_info['file_ja_path']):
            self.is_translated = True
        else:
            self.is_translated = False

        self.__set_docinfo()
        
    def __set_docinfo(self):

        try:
            doc_en_file = open(CONFIG['BASE_PATH'] + self.meta_info['file_en_path'], 'r')
            s = doc_en_file.read()
            doc_en_file.close()

            Regex_version = re.compile(r"""<version>(.*?)</version>""", re.IGNORECASE)
            Regex_cvs_rev = re.compile(r""".*\$Header.*xml\,v\s([0-9\.]*?)\s.*\$""")
            Regex_title   = re.compile(r"""<title>(.*?)</title>""", re.IGNORECASE)

            self.en_ver = Regex_version.search(s).group(1).strip() if Regex_version.search(s) is not None else None
            self.en_cvs_rev =  Regex_cvs_rev.search(s).group(1).strip() if Regex_cvs_rev.search(s) is not None else None
            self.en_title = Regex_title.search(s).group(1).strip() if Regex_title.search(s) is not None else None

            if self.en_cvs_rev is None:
                self.en_cvs_rev = self.__read_rev('en')

            if self.is_translated:
                doc_ja_file = codecs.open(CONFIG['BASE_PATH'] + self.meta_info['file_ja_path'], 'r', 'utf-8')
                s = doc_ja_file.read()
                doc_ja_file.close()

                self.ja_ver = Regex_version.search(s).group(1).strip() if Regex_version.search(s) is not None else None
                self.ja_cvs_rev =  Regex_cvs_rev.search(s).group(1).strip() if Regex_cvs_rev.search(s) is not None else None

                if self.ja_cvs_rev is None:
                    self.ja_cvs_rev = self.__read_rev('ja')
                
                self.ja_title = Regex_title.search(s).group(1).strip() if Regex_title.search(s) is not None else None

                Regex_org_rev = re.compile(r"""<!--.*Original revision:(.*)-->""")
                self.ja_org_rev = Regex_org_rev.search(s).group(1).strip() if Regex_org_rev.search(s) is not None else None

                Regex_translator_block = re.compile(u"(<author title=\"翻訳\">.*</author>)", re.DOTALL)

                if Regex_translator_block.search(s) is not None:  # for handbook part file
                    tb = Regex_translator_block.search(s).group(1)
                    Regex_translator_name =  re.compile(r'<mail link=\".*\">(.*?)</mail>', re.MULTILINE)
                    tn_list = Regex_translator_name.findall(tb)
                    self.translator = ','.join(tn_list)
                else:
                    self.translator = ''
                
        except Exception, errormsg:
            logging.warning('SimpleDoc.__set_doc_info()')
            logging.warning(self.meta_info['file_id'] + ' ' + errormsg.__str__())
            self.ERROR = errormsg

    def __read_rev(self, lang):
        file_path = self.meta_info['file_' + lang + '_path'] # /doc/en/hoge.xml
        file_name = os.path.basename(file_path) #hoge.xml
        dir_path = os.path.dirname(file_path) #/doc/en
        
        cvs_entries = open(CONFIG['BASE_PATH'] + dir_path + '/CVS/Entries', 'r') # BASE_PATH/doc/en/CVS/Entries

        cvs_rev = None
        for l in cvs_entries:
            if l.startswith('/' + file_name):
                cvs_rev = l.split('/')[2]

        return cvs_rev
            
            
        
        
        
