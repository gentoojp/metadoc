#!/usr/bin/env python

from settings import *
import commands
import tempfile
import urllib
import os

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

    docciff_command = '/usr/bin/docdiff --utf8 --html %s %s' % (old_file[1], new_file[1])
    diff_html = commands.getoutput(docdiff_command)

    html = open(CONFIG['DIFF_DIR'] + '/' + doc.meta_info['file_id'] + '.' + doc.ja_org_rev + '_' + doc.en_cvs_rev + '.html', 'w')
    html.write(diff_html)
    html.close()


    os.remove(old_file[1])
    os.remove(new_file[1])
