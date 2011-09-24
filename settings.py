#!env python
# encoding: utf-8
CONFIG = {}

CONFIG['metadoc_en'] = "/doc/en/metadoc.xml"
CONFIG['metadoc_ja'] = "/doc/ja/metadoc.xml"

CONFIG['BASE_PATH'] =  "/usr/local/jpdoc/cvs/gentoo"
CONFIG['HANDBOOK_DIR'] = ('handbook', 'security')

CONFIG['NON_LIST_FILE'] = ('metadoc','metadoc-index', 'metadoc-list', 'metadoc-overview', 'doc-languages', 'inserts')

CONFIG['GENTOO_URL_BASE'] = 'http://www.gentoo.org'
CONFIG['CVS_URL_BASE'] = 'http://sources.gentoo.org/cgi-bin/viewvc.cgi/gentoo/xml/htdocs'
CONFIG['DIFF_DIF'] = '/var/www/projects.gentoo.gr.jp/htdocs/docs/diff'
CONFIG['DIFF_DIR'] = '/tmp/'

CONFIG['BASE_TAMPLATE'] = "./template/trans_status_base.xml"
CONFIG['CHAPTER_TEMPLATE'] = "./template/trans_status_chapter.xml"
CONFIG['RECORD_TEMPLATE'] = "./template/trans_status_record.xml"
CONFIG['RECORD_NOT_TRANSLATE_TEMPLATE'] = "./template/trans_status_record_not_translate.xml"
CONFIG['RECORD_LATEST_TEMPLATE'] = "./template/trans_status_record_latest.xml"

CONFIG['COVERS'] = ('handbook-alpha', 'handbook-amd64', 'handbook-arm', 'handbook-hppa',
                    'handbook-ia64', 'handbook-mips', 'handbook-ppc', 'handbook-ppc64',
                    'handbook-sparc', 'handbook-x86', 'security-handbook')

CONFIG['handbook-alpha'] = ('Handbook-alpha' , u'ハンドブック alpha')
CONFIG['handbook-amd64'] = ('Handbook-amd64' , u'ハンドブック amd64')
CONFIG['handbook-arm'] = ('Handbook-arm' , u'ハンドブック arm')
CONFIG['handbook-hppa'] = ('Handbook-hppa' , u'ハンドブック hppa')
CONFIG['handbook-ia64'] = ('Handbook-ia64' , u'ハンドブック ia64')
CONFIG['handbook-mips'] = ('Handbook-mips' , u'ハンドブック mipsn')
CONFIG['handbook-ppc'] = ('Handbook-ppc' , u'ハンドブック ppc')
CONFIG['handbook-ppc64'] = ('Handbook-ppc64' , u'ハンドブック ppc64')
CONFIG['handbook-sparc'] = ('Handbook-sparc' , u'ハンドブック sparc')
CONFIG['handbook-x86'] = ('Handbook-x64' , u'ハンドブック x86')
CONFIG['security-handbook']  = ('Security Handbook', u'セキュリティハンドブック')
