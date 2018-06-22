# This script will query a catalog and dump out the definetions for a table. These are then output into a new
# script that can recreate the table.

import argparse
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint


def dump_table(table):
    tab = {
        'display': table.display,
        'table_display': table.table_display,
        'comment': table.comment
    }
    return tab


def dump_foreign_keys(table):
    fks = []
    for key in table.foreign_keys:
        fk = {
            'foreign_key_columns': [c['column_name'] for c in key.foreign_key_columns],
            'pk_schema': key.referenced_columns[0]['schema_name'],
            'pk_table': key.referenced_columns[0]['table_name'],
            'pk_columns': [c['column_name'] for c in key.referenced_columns],
            'constraint_names': key.names,
        }
        for i in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            a = getattr(key, i)
            if not (a == {} or a is None or a == 'NO ACTION'):
                fk[i] = "'" + a + "'" if re.match('comment|on_update|on_delete', i) else a
        fks.append(fk)
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
            'name': i.name,
            'type': {'typename': i.type.typename, 'is_array': i.type.is_array},
            'nullok': i.nullok,
            'annotations': i.annotations,
            'comment': i.comment
        }
        for i in table.column_definitions
    ]
    return cols


def main():
    parser = argparse.ArgumentParser(description='Dump annotations  for table {}:{}')
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
    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
""")

    provide_system = False
    system_columns = ['RID', 'RCB', 'RMB', 'RCT', 'RMT']

    print('column_defs = [')
    for i in dump_columns(table):
        if i['name'] in system_columns:
            provide_system = True
            continue
        print('''    em.Column.define(
        '{}',{},
        nullok={},
        annotations={}
        comment={}),
'''.format(i['name'], i['type'], i['nullok'], i['annotations'],
                               "'" + i['comment'] + "'" if i['comment'] is not None else None))

    print('key_defs = [')
    for i in dump_keys(table):
        print("""    em.Key.define(
            {},
            constraint_names={},
            annotation={},
            comment={}),""".format(i['key_columns'], i['names'], i['annotations'],
                                   "'" + i['comment'] + "'" if i['comment'] is not None else None))
    print(']')

    print('\nfkey_defs = [')
    for i in dump_foreign_keys(table):
        print("""    em.ForeignKey.define(
        {},
        '{}', '{}', {},
        constraint_names = {},""".format(i['foreign_key_columns'],
                                         i['pk_schema'],
                                         i['pk_table'],
                                         i['pk_columns'],
                                         i['constraint_names']))

        for k in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            if k in i:
                print("        {} = {},".format(k, i[k]))
        print('    ),')

    print(']\n')

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
)'''.format(table.name,
                "'" + table.comment + "'" if table.comment is not None else None, provide_system))

    print("""
def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {0}:{1}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = '{0}'
    table_name = '{1}'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
    main()""".format(schema_name, table_name))


if __name__ == "__main__":
    main()
