#!/usr/bin/env python

import xml.etree.ElementTree as etree
from settings import *
import commands
import tempfile
import urllib
import os
import os.path
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/metadoc.log',
                    filemode='w')

def doc_url(doc, lang = 'en', cvs=False,  diff = False):

    if lang == 'ja':
        f_path = doc.meta_info['file_ja_path']
    else:
        f_path = doc.meta_info['file_en_path']

    if diff:
        return CONFIG['CVS_URL_BASE'] + f_path + '?r1=%s&r2=%s' % (doc.ja_org_rev, doc.en_cvs_rev)

    if cvs:
        return CONFIG['CVS_URL_BASE'] + f_path
    else:
        return CONFIG['GENTOO_URL_BASE'] + f_path


def docdiff_url(doc):
    file_path = doc.meta_info['file_ja_path']
    
    cvs_url = "http://sources.gentoo.org/cgi-bin/viewcvs.cgi/*checkout*/xml/htdocs" + file_path + "?rev=%s&hideattic=0&root=gentoo&content-type=text/plain" 

    old_file = tempfile.mkstemp()
    new_file = tempfile.mkstemp()

    urllib.urlretrieve(cvs_url % (doc.ja_org_rev,) , old_file[1])
    urllib.urlretrieve(cvs_url % (doc.en_cvs_rev,) , old_file[1])

    docdiff_command = '/usr/bin/docdiff --utf8 --html %s %s' % (old_file[1], new_file[1])
    diff_html = commands.getoutput(docdiff_command)

    diff_html_path = None

    try:
        diff_html_path = CONFIG['DIFF_DIR'] + doc.meta_info['file_id'] + '.' + doc.ja_org_rev + '_' + doc.en_cvs_rev + '.html'
        html = open(diff_html_path, 'w')
        html.write(diff_html)
        html.close()
    except:
        logging.warning('docdiff_url: warning')
        logging.warning(doc.__str__())
        logging.warning(doc.meta_info['file_id'])

    os.remove(old_file[1])
    os.remove(new_file[1])

    return os.path.basename(diff_html_path)



def guess_categories(info_list):
    for info in info_list:
        try:
            tree = etree.parse(CONFIG['BASE_PATH'] + info['file_en_path'])
            included_docs = tree.findall('.//include')
            order = 0
            if included_docs.__len__() > 0:
                for d in included_docs:
                    d_path = d.get('href')
                    for i in info_list:
                        if d_path == os.path.basename(i['file_en_path']): # searching meta-info by including path
                            i['en_memberof'].update(info['en_memberof'])
                            i['ja_memberof'].update(info['ja_memberof'])
                            i['order'] = order
                            order = order +1 
        except:
            pass
    
    return info_list


def guess_categories_coverpage(hb_list):
    for info in hb_list:
        if info['file_id'] in CONFIG['COVERS']:
            f_id = info['file_id']
            info['en_memberof'].update({f_id: CONFIG[f_id][0]})
            info['ja_memberof'].update({f_id: CONFIG[f_id][1]})

    hb_list = guess_categories(hb_list)
    # sort by index
    for info in hb_list:
        if not 'order' in info:
            info['order'] = -1
    hb_list.sort(cmp=lambda x,y: cmp(x['order'], y['order']))
    return hb_list
