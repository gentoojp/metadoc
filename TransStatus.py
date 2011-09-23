#!/usr/bin/env python
# coding: utf-8

import codecs
from xml.sax.saxutils import escape
from datetime import date
from string import Template
from metadoc import MetaDoc
from simple_doc import SimpleDoc
from handbook import Handbook
from util import *
from settings import *


class TransStatus(object):
    def __init__(self):
        self.base_template = Template(open(CONFIG['BASE_TAMPLATE'], 'r').read().decode('utf-8'))
        self.chapter_template = Template(open(CONFIG['CHAPTER_TEMPLATE'], 'r').read().decode('utf-8'))
        md = MetaDoc()
        self.categories = { category.get('id'): { 'member':[], 'title': category.text } for category in md.get_categories(lang='ja') }

        sd_all = [SimpleDoc(info) for info in md.get_meta_info(scope = 'simple')]

        sd_list = [sd for sd in sd_all if self.list_check(sd)]
        sd_error_list = [sd for sd in sd_all if not self.list_check(sd)]

        for sd in sd_list:
            try:
                for category in sd.meta_info['en_memberof'].keys():
                    self.add_doc(category, sd)
            except:
                pass

        hb_all = [Handbook(info) for info in md.get_meta_info(scope = 'handbook')]
        
        for hb in hb_all:
            try:
                for category in hb.meta_info['en_memberof'].keys():
                    self.add_doc(category, hb)
            except:
                pass

    def add_doc(self, category_id, doc):
        self.categories[category_id]['member'].append(doc)

    def list_check(self, sd):
        if sd.meta_info_error:
            return False

        if sd.meta_info['file_id'] in CONFIG['NON_LIST_FILE']:
            return False

        return True

    def dump(self):
        chapters = []
        for category in sorted(self.categories.items()):
            #print "----"
            #print category[0]
            records = []
            for record in self.record(category[0]):
                 records.append(record)
            
            chapters.append(self.chapter_template.substitute(chapter = category[1]['title'], records = u"".join(records)))

        
        d = u"%s" % date.today().strftime('%d %b %Y')
        print self.base_template.substitute(date = d, chapters = u"".join(chapters)).encode('utf-8')


    def record(self, category_id):
        docs = self.categories[category_id]['member']
        for doc in docs:
            attrs = {
                    'en_url': escape(doc_url(doc, lang='en')),
                    'en_cvs': escape(doc_url(doc, lang='en', cvs=True)),
                    'en_cvs_rev': doc.en_cvs_rev,
                    'en_title': doc.en_title,
                    }
            if doc.is_translated:
                if doc.en_cvs_rev == doc.ja_cvs_rev:
                    template = Template(open(CONFIG['RECORD_LATEST_TEMPLATE'], 'r').read().decode('utf-8'))
                else:
                    template = Template(open(CONFIG['RECORD_TEMPLATE'], 'r').read().decode('utf-8'))
                    
                doc_diff_url = docdiff_url(doc)
                
                if doc_diff_url == None:
                    doc_diff_url = ""

                try:
                    translator = doc.translator
                except:
                    translator = ""
                attrs.update({
                    'ja_url': escape(doc_url(doc, lang='ja')),
                    'ja_cvs': escape(doc_url(doc, lang='ja', cvs=True)),
                    'ja_cvs_rev': doc.ja_cvs_rev,
                    'diff_url': escape(doc_url(doc, diff=True)),
                    'doc_diff_url': escape(doc_diff_url),
                    'translator': escape(translator)
                    })
            else:
                template = Template(open(CONFIG['RECORD_NOT_TRANSLATE_TEMPLATE'], 'r').read().decode('utf-8'))

            yield template.substitute(attrs)

if __name__ == "__main__":
    t = TransStatus()
    t.dump()

# vim: set ts=4 sw=4 tw=0 :
