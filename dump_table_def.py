# This script will query a catalog and dump out the definetions for a table. These are then output into a new
# script that can recreate the table.

import argparse
from deriva.core import ErmrestCatalog, get_credential
import pprint
import re
import sys

server ='pbcconsortium.isrd.isi.edu'

def print_annotations(table, stream):
    table_annotations = {
        'visible_columns': table.visible_columns,
        'visible_foreign_keys': table.visible_foreign_keys,
        'table_display': table.table_display,
        'table_annotations': table.annotations,
        'table_acls': table.acls,
        'table_acl_bindings': table.acl_bindings
    }

    for k, v in table_annotations.items():
        if v != {}:
            print('{} = \\'.format(k), file=stream)
            pprint.pprint(v, indent=4, width=80, depth=None, compact=False, stream=stream)

    column_annotations = {}
    column_acls = {}
    column_acl_bindings = {}
    for i in table.column_definitions:
        if i.annotations != {}:
            column_annotations[i.name] = i.annotations
        if i.acls != {}:
            column_acls[i.name] = i.acls
        if i.acl_bindings != {}:
            column_acl_bindings[i.name] = i.acl_bindings
    if column_annotations != {}:
        print('column_annotations = \\', file=stream)
        pprint.pprint(column_annotations, indent=4, width=80, depth=None, compact=False, stream=stream)
        print('',file=stream)
    if column_acls != {}:
        print('column_acls = \\', file=stream)
        pprint.pprint(column_acls, indent=4, width=80, depth=None, compact=False, stream=stream)
        print('',file=stream)
    if column_acl_bindings != {}:
        print('column_acl_bindings = \\', file=stream)
        pprint.pprint(column_acl_bindings, indent=1, width=80, depth=None, compact=False, stream=stream)
        print('',file=stream)
    return


def print_foreign_key_defs(table, stream):
    print('\nfkey_defs = [', file=stream)
    for fkey in table.foreign_keys:
        print("""    em.ForeignKey.define(
            {},
            '{}', '{}', {},
            constraint_names = {},""".format([c['column_name'] for c in fkey.foreign_key_columns],
                                             fkey.referenced_columns[0]['schema_name'],
                                             fkey.referenced_columns[0]['table_name'],
                                             [c['column_name'] for c in fkey.referenced_columns],
                                             fkey.names), file=stream)

        for i in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            a = getattr(fkey, i)
            if not (a == {} or a is None or a == 'NO ACTION' or a == ''):
                v = "'" + a + "'" if re.match('comment|on_update|on_delete', i) else a
                print("        {} = {},".format(i, v), file=stream)
        print('    ),', file=stream)

    print(']', file=stream)


def print_key_defs(table, stream):
    print('key_defs = [', file=stream)
    for key in table.keys:
        print("""    em.Key.define(
                   {},
                   constraint_names={},""".format(key.unique_columns, key.names), file=stream)
        for i in ['annotations',  'comment']:
            a = getattr(key, i)
            if not (a == {} or a is None or a == ''):
                v = "'" + a + "'" if key.comment == 'comment' else a
                print("        {} = {},".format(i, v), file=stream)
        print('    ),', file=stream)
    print(']', file=stream)
    return


def print_column_defs(table, stream):
    system_columns = ['RID', 'RCB', 'RMB', 'RCT', 'RMT']
    provide_system = False
    print('column_defs = [', file=stream)
    for col in table.column_definitions:
        if col.name in system_columns:
            provide_system = True
            continue
        print('''    em.Column.define(
        '{}', em.builtin_types['{}'],
        nullok = {},'''.format(col.name,
                        col.type.typename + '[]' if 'is_array' is True else col.type.typename,
                        col.nullok,), file=stream)
        for i in ['annotations', 'acls', 'acl_bindings', 'comment']:
            a = getattr(col, i)
            if not (a == {} or a is None):
                v = "'" + a + "'" if i == 'comment' else a
                print("        {} = {},".format(i, v), file=stream)
        print('    ),', file=stream)
    print(']', file=stream)
    return provide_system


def print_table_def(table, provide_system, stream):
    print("""
table_def = em.Table.define(
    '{}',""".format(table.name), file=stream)
    for i in ['key_defs', 'fkey_defs', 'annotations', 'acls', 'acl_bindings', 'comment', ]:
            a = getattr(table, i)
            if not (a == {} or a is None or a == 'NO ACTION' or a == ''):
                v = "'" + a + "'" if re.match('comment|on_update|on_delete', i) else a
                print("        {} = {},".format(i, v), file=stream)
        print('    ),', file=stream)
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=acl_bindings,
    comment=comment,
    provide_system = {}
)""".format(table.name, provide_system), file=stream)


def print_defs(server, schema_name, table_name, stream):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]
    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = '{}'
schema_name = '{}'
""".format(table_name, schema_name), file=stream)

    provide_system = print_column_defs(table, stream)
    print('\n', file=stream)
    print_key_defs(table, stream)
    print('\n', file=stream)
    print_foreign_key_defs(table, stream)
    print('\n', file=stream)
    print_annotations(table, stream)
    print('\n', file=stream)
    print_table_def(table, provide_system, stream)
    return


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
        print_defs(server, schema_name, table_name, sys.stdout)
    else:
        with open(outfile, 'w') as f:
            print_defs(server, schema_name, table_name, f)
        f.close()


if __name__ == "__main__":
    main()
