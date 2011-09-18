#!env python

from simple_doc import SimpleDoc
from handbook import Handbook
from metadoc import MetaDoc

m = MetaDoc()

for info in [i for i in  m.get_meta_info(scope = 'handbook')]:
  doc = Handbook(info)
  if doc.has_child():
      for c in doc.childs:
          print "%s -> %s" % (c.meta_info['parent'], c.meta_info['file_en_path'])
