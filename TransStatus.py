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
        md = MetaDoc()
        self.categories = {}

        for category in md.get_categories(lang='ja'):
            self.__add_category(category.get('id'), category.text, category.get('parent'))
        self.__add_category('Handbook', 'Handbook', None)

        # Simple Documents
        sd_all = [SimpleDoc(info) for info in md.get_meta_info(scope = 'simple')]
        sd_list = [sd for sd in sd_all if self.list_check(sd)]
        sd_error_list = [sd for sd in sd_all if not self.list_check(sd)]

        for sd in sd_list:
            self.__add_doc(sd)

        # Handbooks
        hb_all = [Handbook(info) for info in md.get_meta_info(scope = 'handbook')]
        for hb in hb_all:
            self.__add_doc(hb)
    
    def __add_category(self, category_id, title, parent):
        self.categories[category_id] = { 'member': [], 'title': title, 'parent': parent }

    def __add_doc(self, doc):
        if doc.meta_info['en_memberof']:
            if doc.meta_info.has_key('parent') and doc.meta_info['parent']:
                if not doc.meta_info['parent'] in self.categories and doc.meta_info['parent'] in CONFIG:
                    self.__add_category(doc.meta_info['parent'], CONFIG[doc.meta_info['parent']][1], 'Handbook')
                self.categories[doc.meta_info['parent']]['member'].append(doc)
            else:
                for category_id in doc.meta_info['en_memberof'].keys():
                    if not category_id in self.categories and category_id in CONFIG:
                        # for Handbook
                        self.__add_category(category_id, CONFIG[category_id][1], 'Handbook')
                    self.categories[category_id]['member'].append(doc)

        if type(doc) is Handbook and doc.has_child():
             for child_doc in doc.childs:
                 self.__add_doc(child_doc)


    def list_check(self, sd):
        if sd.meta_info_error:
            return False

        if sd.meta_info['file_id'] in CONFIG['NON_LIST_FILE']:
            return False

        return True

    def dump(self):
        chapters = []
        for category in sorted(self.categories.items()):
            if category[1]['parent']:
                records = []
                for record in self.record(category[0]):
                     records.append(record)
                c_title = u"%s -> %s" % (self.categories[category[1]['parent']]['title'], category[1]['title'])
                chapters.append(self.chapter_template.substitute(chapter = c_title, records = u"".join(records)))
        
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
                doc_diff_url = None#docdiff_url(doc)
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
