#!/usr/bin/env python

from simple_doc import SimpleDoc
from handbook import Handbook
from metadoc import MetaDoc
from settings import *

def list_check(sd):
    if sd.meta_info_error:
        return False

    if sd.meta_info['file_id'] in CONFIG['NON_LIST_FILE']:
        return False

    return True
    


def main():
    md = MetaDoc()
    
    sd_all = [SimpleDoc(info) for info in md.get_meta_info(scope = 'simple')]

    sd_list = [sd for sd in sd_all if list_check(sd)]
    sd_error_list = [sd for sd in sd_all if not list_check(sd)]

    for sd in sd_list:
        try:
            if sd.is_translated:
                print sd.meta_info['file_id'], '/', sd.en_title, '/', sd.ja_title.encode('utf-8') 
            else:
                print sd.meta_info['file_id'], '/', sd.en_title, '/', 'NOT_TRANSLATED'
        except Exception, errormsg:
            print errormsg, sd.meta_info['file_id']

    print '---'
    for sd in sd_error_list:
        print "SD_WARNING", sd.meta_info['file_id']
        


if __name__ == '__main__':
    main()
