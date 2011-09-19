#!/usr/bin/env python

from settings import *
import commands


def doc_url(doc, lang = 'en', cvs=False,  diff = False):

    if lang = 'ja':
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
    pass
    
