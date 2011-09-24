#!env python

CONFIG = {}

CONFIG['metadoc_en'] = "/doc/en/metadoc.xml"
CONFIG['metadoc_ja'] = "/doc/ja/metadoc.xml"

CONFIG['BASE_PATH'] =  "/usr/local/jpdoc/cvs/gentoo"
CONFIG['BASE_PATH'] =  "/home/kazunori/repos/gentoojp/gentoo-docs/xml/htdocs/"
CONFIG['HANDBOOK_DIR'] = ('handbook', 'security')

CONFIG['NON_LIST_FILE'] = ('metadoc','metadoc-index', 'metadoc-list', 'metadoc-overview', 'doc-languages', 'inserts')

CONFIG['GENTOO_URL_BASE'] = 'http://www.gentoo.org'
CONFIG['CVS_URL_BASE'] = 'http://sources.gentoo.org/cgi-bin/viewvc.cgi/gentoo/xml/htdocs'
CONFIG['DIFF_DIF'] = u'/var/www/projects.gentoo.gr.jp/htdocs/docs/diff'
CONFIG['DIFF_DIR'] = u'/tmp/'

CONFIG['BASE_TAMPLATE'] = "./template/trans_status_base.xml"
CONFIG['CHAPTER_TEMPLATE'] = "./template/trans_status_chapter.xml"
CONFIG['RECORD_TEMPLATE'] = "./template/trans_status_record.xml"
CONFIG['RECORD_NOT_TRANSLATE_TEMPLATE'] = "./template/trans_status_record_not_translate.xml"
CONFIG['RECORD_LATEST_TEMPLATE'] = "./template/trans_status_record_latest.xml"
