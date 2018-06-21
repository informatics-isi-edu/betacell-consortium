# This script will query a catalog and dump out the annotations for a table. These are then output into a new
# script that can recreate those annotations.

import argparse
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint

parser = argparse.ArgumentParser(description='Generate a table configuration from an existing table.')
parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                    help='Catalog server name')
parser.add_argument('table', help='schema:table_name)')

args = parser.parse_args()

server = args.server
schema_name = args.table.split(':')[0]
table_name = args.table.split(':')[1]

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]

header = '''from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

server = '{}'
schema_name = '{}'
table_name = '{}'

'''.format(server, schema_name, table_name)

footer = '''
credential = get_credential(server)
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
        
table.table_display = table_display

table.apply(catalog)
'''



visible_columns = table.visible_columns
visible_foreign_keys = table.visible_foreign_keys
table_display = table.table_display
table_annotations = table.annotations
table_acls = table.acls
table_acl_bindings = table.acl_bindings

column_annotations = {}
column_acls = {}
column_acl_bindings = {}
for i in table.column_definitions:
    column_annotations[i.name] = i.annotations
    column_acls[i.name] = i.acls
    column_acl_bindings[i.name] = i.acl_bindings

print(header)
print('visible_columns = \\')
pprint.pprint(visible_columns, indent=4, width=80, depth=None, compact=False)
print('\n\n')
print('visible_foreign_keys = \\')
pprint.pprint(visible_foreign_keys, indent=4, width=80, depth=None, compact=False)
print('\n')
print('table_display = \\')
pprint.pprint(table_display, indent=4, width=80, depth=None, compact=False)

print('table_annotations = \\')
pprint.pprint(table_annotations, indent=4, width=80, depth=None, compact=False)
print('table_acls = \\')
pprint.pprint(table_acls, indent=4, width=80, depth=None, compact=False)
print('table_acl_bindings = \\')
pprint.pprint(table_acl_bindings, indent=4, width=80, depth=None, compact=False)

print('column_annotations = \\')
pprint.pprint(column_annotations, indent=1, width=80, depth=None, compact=False)
print('column_acls = \\')
pprint.pprint(column_acls, indent=1, width=80, depth=None, compact=False)
print('column_acl_bindings = \\')
pprint.pprint(column_acl_bindings, indent=1, width=80, depth=None, compact=False)

print(footer)
