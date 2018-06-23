# This script will query a catalog and dump out the definetions for a table. These are then output into a new
# script that can recreate the table.

import argparse
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import re
import sys

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
            'type':  i.type.typename + '[]' if 'is_array' is True else  i.type.typename,
            'nullok': i.nullok,
            'annotations': i.annotations,
            'comment': i.comment,
            'acls' : i.acls,
            'acl_bindings' : i.acl_bindings
        }
        for i in table.column_definitions
    ]
    return cols


def print_table_def(server, schema_name, table_name, stream):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]
    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
""", file=stream)

    provide_system = False
    system_columns = ['RID', 'RCB', 'RMB', 'RCT', 'RMT']

    print('column_defs = [', file=stream)
    for i in dump_columns(table):
        if i['name'] in system_columns:
            provide_system = True
            continue
        print('''    em.Column.define(
            '{}', em.builtin_types['{}'],
            nullok = {},
            annotations = {},
            acls = {},
            acl_bindings = {},
            comment={}),'''.format(i['name'], i['type'], i['nullok'], i['annotations'],i['acls'], i['acl_bindings'],
               "'" + i['comment'] + "'" if i['comment'] is not None else None), file=stream)
    print(']', file=stream)
    print('key_defs = [', file=stream)
    for i in dump_keys(table):
        print("""    em.Key.define(
                {},
                constraint_names={},
                annotations={},
                comment={}),""".format(i['key_columns'], i['names'], i['annotations'],
                                       "'" + i['comment'] + "'" if i['comment'] is not None else None), file=stream)
    print(']', file=stream)

    print('\nfkey_defs = [', file=stream)
    for i in dump_foreign_keys(table):
        print("""    em.ForeignKey.define(
            {},
            '{}', '{}', {},
            constraint_names = {},""".format(i['foreign_key_columns'],
                                             i['pk_schema'],
                                             i['pk_table'],
                                             i['pk_columns'],
                                             i['constraint_names']), file=stream)

        for k in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            if k in i:
                print("        {} = {},".format(k, i[k]), file=stream)
        print('    ),', file=stream)

    print(']\n', file=stream)


    print('annotations = \\', file=stream)
    pprint.pprint(table.annotations, indent=4, stream=stream)
    print('acls = \\', file=stream)
    pprint.pprint(table.acls, indent=4, stream=stream)
    print('acl_bindings = \\', file=stream)
    pprint.pprint(table.acl_bindings, indent=4, stream=stream)
    print('comment = \\', file=stream)
    pprint.pprint(table.comment, indent=4, stream=stream)

    print("""
table_def = em.Table.define(
    '{}',
    column_defs = column_defs,
    key_defs = key_defs,
    fkey_defs = fkey_defs,
    annotations = annotations,
    acls = acls,
    acl_bindings = acl_bindings,
    comment = comment,
    provide_system = {}
)""".format(table.name, provide_system), file = stream)


    print("""
def main():
    parser = argparse.ArgumentParser(description='Load table defs for table {0}:{1}')
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

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()""".format(schema_name, table_name), file=stream)


def main():
    parser = argparse.ArgumentParser(description='Dump annotations  for table {}:{}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('table', help='schema:table_name)')
    parser.add_argument('--outfile', default="stdout", help='output file name)')
    args = parser.parse_args()

    server = args.server
    schema_name = args.table.split(':')[0]
    table_name = args.table.split(':')[1]
    outfile = args.outfile

    if outfile == 'stdout':
        print_table_def(server, schema_name, table_name, sys.stdout)
    else:
        with open(outfile, 'w') as f:
            print_table_def(server, schema_name, table_name, f)
        f.close()

if __name__ == "__main__":
    main()
