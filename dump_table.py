# This script will query a catalog and dump out the definetions for a table. These are then output into a new
# script that can recreate the table.

import argparse
from deriva.core import ErmrestCatalog, get_credential
import deriva.core.ermrest_model as em
import deriva.core.ermrest_model as ec

import pprint
import re
import sys

tag_map = {
    'generated':          'tag:isrd.isi.edu,2016:generated',
    'immutable':          'tag:isrd.isi.edu,2016:immutable',
    'display':            'tag:misd.isi.edu,2015:display',
    'visible_columns':    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys': 'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':        'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':      'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives': 'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':     'tag:isrd.isi.edu,2016:column-display',
    'asset':              'tag:isrd.isi.edu,2017:asset',
    'export':             'tag:isrd.isi.edu,2016:export',
}

def print_annotations(table, stream):

    tag_rmap = {v: k for k, v in tag_map.items()}

    table_annotations = {
        'visible_columns': table.visible_columns,
        'visible_foreign_keys': table.visible_foreign_keys,
        'table_comment': table.comment,
        'table_display': table.table_display,
        'table_acls': table.acls,
        'table_acl_bindings': table.acl_bindings
    }
    if tag_map['export'] in table.annotations:
        table_annotations['export'] =  table.annotations[tag_map['export']]

    # Print out variable definitions for annotations that we are going to pull out seperately.
    for k, v in table_annotations.items():
        if v == {} or v == '':
            print('{} = {}'.format(k, v), file=stream)
        else:
            print('{} = \\'.format(k), file=stream)
            pprint.pprint(v, width=80, depth=None, compact=True, stream=stream)
            print('', file=stream)

    print('table_annotations = {', file=stream)
    for k, v in table.annotations.items():
        tag_name = tag_rmap.get(k,k)
        if tag_name in table_annotations:
            # Put tag value in a variable to make editing file easier.....
            print('    "{}": {},'.format(k,tag_name), file=stream)
        else:
            if tag_name not in tag_map:
                print('WARNING: Unknown tag: {}'.format(k))
            print('    "{}":'.format(k), file=stream)
            pprint.pprint(v, compact=True, stream=stream)
            print(',', file=stream)
    print('}', file=stream)

    column_annotations = {}
    column_acls = {}
    column_acl_bindings = {}
    column_comment = {}
    for i in table.column_definitions:
        if not (i.comment == '' or i.comment == None):
            column_comment[i.name] = i.comment
        if i.annotations != {}:
            column_annotations[i.name] = i.annotations
        if i.acls != {}:
            column_acls[i.name] = i.acls
        if i.acl_bindings != {}:
            column_acl_bindings[i.name] = i.acl_bindings
    if column_comment != {}:
        print('column_comment = \\', file=stream)
        pprint.pprint(column_comment, width=80, depth=None, compact=False, stream=stream)
        print('', file=stream)

    print('column_annotations = \\', file=stream)
    pprint.pprint(column_annotations, width=80, depth=None, compact=False, stream=stream)
    print('', file=stream)

    if column_acls != {}:
        print('column_acls = \\', file=stream)
        pprint.pprint(column_acls, width=80, depth=None, compact=False, stream=stream)
        print('', file=stream)
    if column_acl_bindings != {}:
        print('column_acl_bindings = \\', file=stream)
        pprint.pprint(column_acl_bindings, width=80, depth=None, compact=False, stream=stream)
        print('', file=stream)
    return


def print_foreign_key_defs(table, stream):
    print('fkey_defs = [', file=stream)
    for fkey in table.foreign_keys:
        print("""    em.ForeignKey.define({},
            '{}', '{}', {},
            constraint_names={},""".format([c['column_name'] for c in fkey.foreign_key_columns],
                                           fkey.referenced_columns[0]['schema_name'],
                                           fkey.referenced_columns[0]['table_name'],
                                           [c['column_name'] for c in fkey.referenced_columns],
                                           fkey.names), file=stream)

        for i in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            a = getattr(fkey, i)
            if i == 'annotations':
                print('Found annotation',a)
            if not (a == {} or a is None or a == 'NO ACTION' or a == ''):
                v = "'" + a + "'" if re.match('comment|on_update|on_delete', i) else a
                print("        {}={},".format(i, v), file=stream)
        print('    ),', file=stream)

    print(']', file=stream)


def print_key_defs(table, stream):
    print('key_defs = [', file=stream)
    for key in table.keys:
        print("""    em.Key.define({},
                   constraint_names={},""".format(key.unique_columns, key.names), file=stream)
        for i in ['annotations',  'comment']:
            a = getattr(key, i)
            if not (a == {} or a is None or a == ''):
                v = "'" + a + "'" if i == 'comment' else a
                print("       {} = {},".format(i, v), file=stream)
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
        print('''    em.Column.define('{}', em.builtin_types['{}'],'''.format(col.name,
                               col.type.typename + '[]' if 'is_array' is True else col.type.typename,
                               ), file=stream)
        if col.nullok is False:
            print("        nullok=False,", file=stream)
        for i in ['annotations', 'acls', 'acl_bindings', 'comment']:
            a = getattr(col, i)
            if not (a == {} or a is None):
                v = "'" + a + "'" if i == 'comment' else a
                print("        {}={},".format(i, v), file=stream)
        print('    ),', file=stream)
    print(']', file=stream)
    return provide_system


def print_table_def(table, provide_system, stream):
    print("""table_def = em.Table.define(table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system = {}
)""".format(provide_system), file=stream)


def print_defs(server, catalog_id, schema_name, table_name, stream):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
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
    parser.add_argument('server', help='Catalog server name')
    parser.add_argument('--catalog', default=1, help='ID number of desired catalog')
    parser.add_argument('table', help='schema:table_name)')
    parser.add_argument('--outfile', default="stdout", help='output file name)')
    args = parser.parse_args()

    server = args.server
    schema_name = args.table.split(':')[0]
    table_name = args.table.split(':')[1]
    catalog_id = args.catalog
    outfile = args.outfile

    if outfile == 'stdout':
        print_defs(server, catalog_id, schema_name, table_name, sys.stdout)
    else:
        with open(outfile, 'w') as f:
            print_defs(server, catalog_id, schema_name, table_name, f)
        f.close()


if __name__ == "__main__":
    main()
