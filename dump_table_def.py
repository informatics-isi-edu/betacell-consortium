# This script will query a catalog and dump out the definetions for a table. These are then output into a new
# script that can recreate the table.

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

def dump_table(table):
        tab = {
            'display' : table.display,
            'table_display' : table.table_display,
            'comment': table.comment
        }
        return tab

def dump_foreign_keys(table):
    fks =  [
        {
            'foreign_key_columns': [ c['column_name'] for c in i.foreign_key_columns],
            'pk_schema': i.referenced_columns[0]['schema_name'],
            'pk_table': i.referenced_columns[0]['table_name'],
            'pk_columns': [ c['column_name'] for c in i.referenced_columns],
            'constraint_names': i.names,
            'annotations': i.annotations,
            'acls': i.acls, 'acl_bindings' : i.acl_bindings,
            'on_update' : i.on_update, 'on_delete': i.on_delete,
            'comment': i.comment
        } for i in table.foreign_keys
    ]
    return fks

def dump_keys(table):
    keys = [
        {
            'key_columns': i.unique_columns,
            'names': i.names,
            'annotations': i.annotations,
            'comment': i.comment
        } for i in table.keys
    ]
    return keys

def dump_columns(table):
    cols = [
        {
            'name' : i.name,
            'type' : { 'typename': i.type.typename, 'is_array': i.type.is_array},
            'nullok': i.nullok,
            'annotations' : i.annotations,
            'comment' : i.comment
        }
    for i in table.column_definitions
    ]
    return cols

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]
provide_system = False
system_columns = ['RID','RCB','RMB','RCT','RMT']

print('column_defs = [')
for i in dump_columns(table):
    if i['name'] in system_columns:
        provide_system=True
        continue
    print('''    em.Column.define(
    '{}',{},
    nullok={},
    annotations={}
    comment={}),'''.format(i['name'],i['type'],i['nullok'],i['annotations'],
               "'" + i['comment'] + "'" if i['comment'] != None else None))

print('key_defs = [')
for i in dump_keys(table):
    print("""    em.Key.define(
        {},
        constraint_names={},
        annotation={},
        comment={}),""".format(i['key_columns'],i['names'],i['annotations'],

                               "'" + i['comment'] + "'" if i['comment'] != None else None))
print(']')

print('\nfkey_defs = [')
for i in dump_foreign_keys(table):
    print("""    em.ForeignKey.define(
        {},
        '{}', '{}', {},
        constraint_names={},
        annotations={},
        acls={},
        acl_bindings={},
        on_update='{}', on_delete='{}',
        comment={}),""".format(i['foreign_key_columns'], i['pk_schema'], i['pk_table'],i['pk_columns'],
   i['constraint_names'], i['annotations'], i['acls'],i['acl_bindings'],i['on_update'], i['on_delete'], i['comment']))
print(']')

print('table_annotations =')
pprint.pprint(table.annotations, indent=4)

print('''
table_def = em.Table.define(
  {},
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment={},
  acls=acls,
  acl_bindings=acl_bindings,
  annotations=table_annotations,
  provide_system={}
)'''.format(table.name, table.comment, provide_system))

print('''
server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.create_table(catalog, table_def)
'''
)