# This script will query a catalog and dump out the definetions for a table. These are then output into a new
# script that can recreate the table.

import argparse
import autopep8
from deriva.core import ErmrestCatalog, get_credential

from dump_catalog import print_annotations, print_tag_variables, print_variable
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

def print_table_annotations(table, stream):
    tag_rmap = {v: k for k, v in tag_map.items()}

    print_tag_variables(table.annotations, tag_map, stream)

    print_annotations(table.annotations, tag_map, stream, var_name='table_annotations')
    print_variable('table_comment', table.comment, stream)
    print_variable('table_acls', table.acls, stream)
    print_variable('table_acl_bindings', table.acl_bindings, stream)


def print_column_annotations(table, stream):
    column_annotations = {}
    column_acls = {}
    column_acl_bindings = {}
    column_comment = {}

    for i in table.column_definitions:
        if not (i.annotations == '' or i.comment == None):
            column_annotations[i.name] = i.annotations
        if not (i.comment == '' or i.comment == None):
            column_comment[i.name] = i.comment
        if i.annotations != {}:
            column_annotations[i.name] = i.annotations
        if i.acls != {}:
            column_acls[i.name] = i.acls
        if i.acl_bindings != {}:
            column_acl_bindings[i.name] = i.acl_bindings

    print_variable('column_annotations', column_annotations, stream)
    print_variable('column_comment', column_comment, stream)
    print_variable('column_acls', column_acls, stream)
    print_variable('column_acl_bindings', column_acl_bindings, stream)
    return


def print_foreign_key_defs(table, stream):
    s = 'fkey_defs = ['
    for fkey in table.foreign_keys:
        s += """    em.ForeignKey.define({},
            '{}', '{}', {},
            constraint_names={},""".format([c['column_name'] for c in fkey.foreign_key_columns],
                                           fkey.referenced_columns[0]['schema_name'],
                                           fkey.referenced_columns[0]['table_name'],
                                           [c['column_name'] for c in fkey.referenced_columns],
                                           fkey.names)

        for i in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            a = getattr(fkey, i)
            if not (a == {} or a is None or a == 'NO ACTION' or a == ''):
                v = "'" + a + "'" if re.match('comment|on_update|on_delete', i) else a
                s += "        {}={},".format(i, v)
        s += '    ),'

    s += ']'
    print(autopep8.fix_code(s, options={'aggressive': 4}), file=stream)


def print_key_defs(table, stream):
    s = 'key_defs = ['
    for key in table.keys:
        s += """    em.Key.define({},
                   constraint_names={},""".format(key.unique_columns, key.names)
        for i in ['annotations',  'comment', 'acl_bindings', 'acls']:
            a = getattr(key, i)
            if not (a == {} or a is None or a == ''):
                v = "'" + a + "'" if i == 'comment' else a
                s += "       {} = {},".format(i, v)
        s += '),'
    s += ']'
    print(autopep8.fix_code(s, options={'aggressive': 4}), file=stream)
    return


def print_column_defs(table, stream):

    system_columns = ['RID', 'RCB', 'RMB', 'RCT', 'RMT']
    provide_system = False

    s = 'column_defs = ['
    for col in table.column_definitions:
        if col.name in system_columns:
            provide_system = True
        s += '''    em.Column.define('{}', em.builtin_types['{}'],'''.format(col.name,
                               col.type.typename + '[]' if 'is_array' is True else col.type.typename)
        if col.nullok is False:
            s += "nullok=False,"
        for i in ['annotations', 'acls', 'acl_bindings', 'comment']:
            colvar = getattr(col, i)
            if colvar:   #if we have a value for this field....
                s += "{}=column_{}['{}'],".format(i, i, col.name)
        s += '),\n'
    s += ']'
    print(autopep8.fix_code(s, options={'aggressive': 8}), file=stream)
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

    print_column_annotations(table, stream)
    provide_system = print_column_defs(table, stream)
    print('\n', file=stream)
    print_table_annotations(table, stream)
    print('\n', file=stream)
    print_key_defs(table, stream)
    print('\n', file=stream)
    print_foreign_key_defs(table, stream)
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
