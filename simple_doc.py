import re
import os.path
import codecs
from settings import *

class SimpleDoc():
    def __init__(self, info):
        self.meta_info = info

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
            
            if self.is_translated:
                doc_ja_file = codecs.open(CONFIG['BASE_PATH'] + self.meta_info['file_ja_path'], 'r', 'utf-8')
                s = doc_ja_file.read()
                doc_ja_file.close()

                Regex_org_rev = re.compile(r"""<!--.*Original revision:(.*)-->""")

                self.ja_ver = Regex_version.search(s).group(1).strip() if Regex_version.search(s) is not None else None
                self.ja_cvs_rev =  Regex_cvs_rev.search(s).group(1).strip() if Regex_cvs_rev.search(s) is not None else None
                self.ja_title = Regex_title.search(s).group(1).strip() if Regex_title.search(s) is not None else None
                self.ja_org_rev = Regex_org_rev.search(s).group(1).strip() if Regex_org_rev.search(s) is not None else None
        except:
            self.ERROR = False
