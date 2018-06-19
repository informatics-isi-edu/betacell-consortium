from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import re

server = 'pbcconsortium.isrd.isi.edu'
schema_name = 'isa'
table_name = 'replicate'



filename= 'table_config.py'

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]

header = '''
'from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re
server = {} \
schema_name = {}
table_name = {}
'''.format(server, schema_name, table_name)

footer = '''
'credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]

if len(visible_columns) > 0:
    for k, v in visible_columns.items():
        table.visible_columns[k] = v

if len(visible_foreign_keys) > 0:
    for k, v in visible_foreign_keys.items():
        table.visible_foreign_keys[k] = v

table.apply(catalog)
'''


visible_columns = table.visible_columns
visible_foreign_keys = table.visible_foreign_keys
table_display = table.table_display
acls = table.acls
acl_bindings = table.acl_bindings

with open('foo', 'w') as f:
     f.write(header)
     f.write('visible_columns = \\\nl')
     pprint.pprint(visible_columns, stream=f, indent=1, width=80, depth=None, compact=False)
     f.write('\n\n')
     f.write('visible_foreign_keys = \\\n')
     pprint.pprint(visible_columns, stream=f, indent=1, width=80, depth=None, compact=False)
     f.write('\n\n')
     f.write('table_display = \\\n')
     pprint.pprint(visible_columns, stream=f, indent=1, width=80, depth=None, compact=False)
     f.write(footer)
f.closed



