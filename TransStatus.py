#!/usr/bin/env python
# coding: utf-8

import codecs
from xml.sax.saxutils import escape
from datetime import date
from string import Template
from types import *
from metadoc import MetaDoc
from simple_doc import SimpleDoc
from handbook import Handbook
from util import *
from settings import *


class TransStatus(object):
    def __init__(self):
        self.base_template = Template(open(CONFIG['BASE_TAMPLATE'], 'r').read().decode('utf-8'))
        self.chapter_template = Template(open(CONFIG['CHAPTER_TEMPLATE'], 'r').read().decode('utf-8'))

        self.md = MetaDoc()
        self.categories = {}

        # Simple Documents
        sd_all = [info for info in self.md.get_meta_info(scope = 'simple')]
        sd_all = guess_categories(sd_all)
        sd_all = [SimpleDoc(info) for info in sd_all]
        sd_list = [sd for sd in sd_all if self.list_check(sd)]
        sd_error_list = [sd for sd in sd_all if not self.list_check(sd)]

        for sd in sd_list:
            self.add_doc(sd)
        
        hb_all = [info for info in self.md.get_meta_info(scope = 'handbook')]
        hb_all = guess_categories_coverpage(hb_all)
        hb_all = [Handbook(info) for info in hb_all]
        
        for hb in hb_all:
            self.add_doc(hb)

    def add_doc(self, doc):
        for (k, v) in doc.meta_info['ja_memberof'].items():
            if self.categories.has_key(k):
                self.categories[k]['member'].append(doc)
            else:
                parent = self.md.get_parent_category_title(lang='ja', c_id=k)
                self.categories.update({k: {'member': [], 'title': v, 'parent': parent}})
                self.categories[k]['member'].append(doc)

    def list_check(self, sd):
        if sd.meta_info_error:
            return False

        if sd.meta_info['file_id'] in CONFIG['NON_LIST_FILE']:
            return False

        if not sd.meta_info['en_memberof']:
            return False

        return True

    def dump(self):
        chapters = []
        for category in sorted(self.categories.items()):
            records = []
            for record in self.record(category[0]):
                records.append(record)

            if len(records) > 0:
                c_title = u"%s -> %s" % (category[1]['parent'], category[1]['title'])
                chapters.append(self.chapter_template.substitute(chapter = c_title, records = u"".join(records)))
        
        d = u"%s" % date.today().strftime('%d %b %Y')
        print self.base_template.substitute(date = d, chapters = u"".join(chapters)).encode('utf-8')


    def record(self, category_id):
        docs = self.categories[category_id]['member']
        docs.sort(cmp=lambda x,y: cmp(x.en_title, y.en_title))
        for doc in docs:
            attrs = {
                    'en_url': escape(doc_url(doc, lang='en')),
                    'en_cvs': escape(doc_url(doc, lang='en', cvs=True)),
                    'en_cvs_rev': doc.en_cvs_rev,
                    'en_title': doc.en_title,
                    }
            if doc.is_translated:
                if doc.en_cvs_rev == doc.ja_org_rev:
                    template = Template(open(CONFIG['RECORD_LATEST_TEMPLATE'], 'r').read().decode('utf-8'))
                else:
                    template = Template(open(CONFIG['RECORD_TEMPLATE'], 'r').read().decode('utf-8'))
                    
                doc_diff_url = docdiff_url(doc)
                
                if doc_diff_url == None:
                    doc_diff_url = ""
                else:
                    doc_diff_url = CONFIG['DIFF_URL'] + doc_diff_url


                try:
                    translator = doc.translator
                except:
                    translator = ""
                attrs.update({
                    'ja_url': escape(doc_url(doc, lang='ja')),
                    'ja_cvs': escape(doc_url(doc, lang='ja', cvs=True)),
                    'ja_cvs_rev': doc.ja_org_rev,
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
