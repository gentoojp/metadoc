from xml.etree.ElementTree import ElementTree

CONFIG = {}

#CONFIG['metadoc_en'] = "doc/en/metadoc.xml"
#CONFIG['metadoc_ja'] = "doc/ja/metadoc.xml"

CONFIG['metadoc_en'] = "metadoc.en.xml"
CONFIG['metadoc_ja'] = "metadoc.ja.xml"

CONFIG['BASE_PATH'] = "./"
CONFIG['HANDBOOK_DIR'] = ('handbook', 'security')

        
class MetaDoc():
    def __init__(self):
        en_metadoc_tree = ElementTree()
        en_metadoc_tree.parse(CONFIG['BASE_PATH'] + CONFIG['metadoc_en'])

        ja_metadoc_tree = ElementTree()
        ja_metadoc_tree.parse(CONFIG['BASE_PATH'] + CONFIG['metadoc_ja'])

        self.metadoc_tree = {'en' : en_metadoc_tree, 'ja' : ja_metadoc_tree}


    def get_files(self, **kwargs):
        lang = kwargs['lang'] if kwargs.has_key('lang') else 'en'
        tree = self.metadoc_tree[lang]
         
        if kwargs.has_key('f_id'):
            return tree.find("files/file[@id='" + kwargs['f_id'] + "']")

        if kwargs.has_key('scope') and kwargs['scope'] == 'handbook':
            return [f for f in tree.findall('files/file') if f.text.split('/')[3] in CONFIG['HANDBOOK_DIR']]
        elif kwargs.has_key('scope') and kwargs['scope'] == 'simple':
            return [f for f in tree.findall('files/file') if f.text.split('/')[3] not in CONFIG['HANDBOOK_DIR']]
        else:
            return tree.findall('files/file')

    def get_categories(self, **kwargs):
        lang = kwargs['lang'] if kwargs.has_key('lang') else 'en'
        tree = self.metadoc_tree[lang]
        if kwargs.has_key('c_id'):
            return tree.find("categories/cat[@id='" + kwargs['c_id'] + "']")
        else:
            return tree.findall('categories/cat')

            
    def get_docs(self, **kwargs):
        lang = kwargs['lang'] if kwargs.has_key('lang') else 'en'
        tree = self.metadoc_tree[lang]
        if kwargs.has_key('fileid'):
            return tree.find("docs/doc[@fileid='" + kwargs['fileid'] + "']")
        else:
            return tree.findall('docs/doc')
        

    def get_meta_info(self, scope = None):
        files = self.get_files(lang = 'en', scope = scope)
        for f in files:
            meta_info = {}
            meta_info['file_en_path'] = f.text
            meta_info['file_id'] = f.get('id')
            meta_info['f'] = f

            en_doc = self.get_docs(fileid = f.get('id'))
            try:
                en_member_cat = [(m.text, self.get_categories(lang = 'en', c_id = m.text).text) for m in en_doc.getiterator('memberof')]
                meta_info['en_memberof'] = dict(en_member_cat)

                ja_doc = self.get_docs(lang = 'ja', fileid = f.get('id'))
                ja_member_cat = [(m.text, self.get_categories(lang = 'ja', c_id = m.text).text) for m in ja_doc.getiterator('memberof')]
                meta_info['ja_memberof'] = dict(ja_member_cat)
            except:
                meta_info['en_memberof'] = None

            file_ja_path = meta_info['file_en_path'].replace('/en/', '/ja/')
            if file_ja_path == self.get_files(lang = 'ja', f_id = f.get('id')).text:
                meta_info['file_ja_path'] = file_ja_path
            else:
                meta_info['file_ja_path'] = meta_info['file_en_path']

            yield meta_info
    
if __name__ == '__main__':
    print "MetaDoc"
