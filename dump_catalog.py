from __future__ import print_function

import argparse
import pprint
import os
import re
import autopep8
from deriva.core import ErmrestCatalog, get_credential

tag_map = {
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
    'generated':          'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':        'tag:isrd.isi.edu,2017:bulk-upload'
}


def print_variable(name, value, stream):
    """
    Print out a variable assignment on one line if empty, otherwise pretty print.
    :param name:
    :param value:
    :param stream:
    :return:
    """
    if not value or value == '' or value == [] or value == {}:
        s = '{} = {}'.format(name, value)
    else:
        s = '{} = {}'.format(name, pprint.pformat(value, indent=4, width=80, depth=None))
    print(autopep8.fix_code(s, options={'aggressive': 4}), file=stream)


def print_tag_variables(annotations, tag_map, stream):
    """
    For each convenient annotation name in tag_map, print out a variable declaration of the form annotation = v where
    v is the value of the annotation the dictionary.  If the tag is not in the set of annotations, do nothing.
    :param annotations:
    :param tag_map:
    :param stream:
    :return:
    """
    for t, v in tag_map.items():
        if v in annotations:
            print_variable(t, annotations[v], stream)


def print_annotations(annotations, tag_map, stream, var_name='annotations'):
    """
    Print out the annotation definition in annotations, substituting the python variable for each of the tags specified
    in tag_map.
    :param annotations:
    :param tag_map:
    :param stream:
    :return:
    """
    var_map = {v: k for k, v in tag_map.items()}
    if annotations == {}:
        s = '{} = {{}}'.format(var_name)
    else:
        s = '{} = {{'.format(var_name)
        for t, v in annotations.items():
            if t in var_map:
                # Use variable value rather then inline annotation value.
                s += "'{}' : {},".format(t, var_map[t])
            else:
                s += "'{}' : ".format(t)
                s += pprint.pformat(v, width=80, depth=None)
                s += ','
        s += '}'
    print(autopep8.fix_code(s, options={'aggressive': 4}), file=stream)


def print_schema(server, catalog_id, schema_name, stream):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]

    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog
""", file=stream)
    print('table_names = [', file=stream)
    for i in schema.tables:
        print("    '{}',".format(i), file=stream)
    print(']\n', file=stream)
    print_tag_variables(schema.annotations, tag_map, stream)
    print_annotations(schema.annotations, tag_map, stream)
    print_variable('acls', schema.acls, stream)
    print_variable('comment', schema.comment, stream)
    print('''schema_def = em.Schema.define(
        '{0}',
        comment=comment,
        acls=acls,
        annotations=annotations,
    )


def main():
    server = '{0}'
    catalog_id = {1}
    schema_name = '{2}'
    
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id)
    update_catalog.update_schema(mode, replace, server, catalog_id, schema_name, schema_def, annotations, acls, comment)


if __name__ == "__main__":
    main()'''.format(server, catalog_id, schema_name), file=stream)


def print_catalog(server, catalog_id, dumpdir):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    try:
        os.makedirs(dumpdir, exist_ok=True)
    except OSError:
        print("Creation of the directory %s failed" % dumpdir)

    with open('{}/catalog_{}.py'.format(dumpdir, catalog_id), 'w') as f:
        print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import update_catalog
import deriva.core.ermrest_model as em
""", file=f)
        print_tag_variables(model_root.annotations, tag_map, f)
        print_annotations(model_root.annotations, tag_map, f)
        print_variable('acls', model_root.acls, f)
        print('''


def main():
    server = '{0}'
    catalog_id = {1}
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_catalog=True)
    update_catalog.update_catalog(mode, replace, server, catalog_id, annotations, acls)
    

if __name__ == "__main__":
    main()'''.format(server, catalog_id), file=f)

    for schema_name, schema in model_root.schemas.items():
        if schema_name == 'public':
            continue
        filename = '{}/{}.schema.py'.format(dumpdir, schema_name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as f:
            print_schema(server, catalog_id, schema_name, f)
        f.close()

        for i in schema.tables:
            print('Dumping {}:{}'.format(schema_name, i))
            filename = '{}/{}/{}.py'.format(dumpdir, schema_name, i)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                print_table(server, catalog_id, schema_name, i, f)
            f.close()


def print_table_annotations(table, stream):
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
        if not (i.annotations == '' or not i.comment):
            column_annotations[i.name] = i.annotations
        if not (i.comment == '' or not i.comment):
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
    s = 'fkey_defs = [\n'
    for fkey in table.foreign_keys:
        s += """    em.ForeignKey.define({},
            '{}', '{}', {},
            constraint_names={},\n""".format([c['column_name'] for c in fkey.foreign_key_columns],
                                             fkey.referenced_columns[0]['schema_name'],
                                             fkey.referenced_columns[0]['table_name'],
                                             [c['column_name'] for c in fkey.referenced_columns],
                                             fkey.names)

        for i in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            a = getattr(fkey, i)
            if not (a == {} or a is None or a == 'NO ACTION' or a == ''):
                v = "'" + a + "'" if re.match('comment|on_update|on_delete', i) else a
                s += "        {}={},\n".format(i, v)
        s += '    ),\n'

    s += ']'
    print(autopep8.fix_code(s, options={}), file=stream)


def print_key_defs(table, stream):
    s = 'key_defs = [\n'
    for key in table.keys:
        s += """    em.Key.define({},
                   constraint_names={},\n""".format(key.unique_columns, key.names)
        for i in ['annotations',  'comment']:
            a = getattr(key, i)
            if not (a == {} or a is None or a == ''):
                v = "'" + a + "'" if i == 'comment' else a
                s += "       {} = {},\n".format(i, v)
        s += '),\n'
    s += ']'
    print(autopep8.fix_code(s, options={}), file=stream)
    return


def print_column_defs(table, stream):
    system_columns = ['RID', 'RCB', 'RMB', 'RCT', 'RMT']
    provide_system = False

    s = 'column_defs = ['
    for col in table.column_definitions:
        if col.name in system_columns:
            provide_system = True
        s += '''    em.Column.define('{}', em.builtin_types['{}'],'''.\
            format(col.name, col.type.typename + '[]' if 'is_array' is True else col.type.typename)
        if col.nullok is False:
            s += "nullok=False,"
        if col.default and col.name not in system_columns:
            s += "default={!r},".format(col.default)
        for i in ['annotations', 'acls', 'acl_bindings', 'comment']:
            colvar = getattr(col, i)
            if colvar:  # if we have a value for this field....
                s += "{}=column_{}['{}'],".format(i, i, col.name)
        s += '),\n'
    s += ']'
    print(autopep8.fix_code(s, options={'aggressive': 8}), file=stream)
    return provide_system


def print_table_def(provide_system, stream):
    s = \
"""table_def = em.Table.define(table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system = {}
)""".format(provide_system)
    print(autopep8.fix_code(s, options={'aggressive': 8}), file=stream)


def print_table(server, catalog_id, schema_name, table_name, stream):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = '{}'
schema_name = '{}'
""".format(table_name, schema_name), file=stream)

    print_column_annotations(table, stream)
    provide_system = print_column_defs(table, stream)
    print_table_annotations(table, stream)
    print_key_defs(table, stream)
    print_foreign_key_defs(table, stream)
    print_table_def(provide_system, stream)
    print('''
def main():
    server = '{0}'
    catalog_id = {1}
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()'''.format(server, catalog_id), file=stream)
    return


def main():
    parser = argparse.ArgumentParser(description='Dump definition for catalog {}:{}')
    parser.add_argument('server', help='Catalog server name')
    parser.add_argument('--catalog', default=1, help='ID number of desired catalog')
    parser.add_argument('--dir', default="configs", help='output directory name)')
    args = parser.parse_args()

    dumpdir = args.dir
    server = args.server
    catalog_id = args.catalog

    print_catalog(server, catalog_id, dumpdir)


if __name__ == "__main__":
    main()
