import os
import autopep8
import re

from tableschema import Table, Schema, Field
from tableschema import validate, exceptions

from deriva.core import ErmrestCatalog, get_credential

from dump_catalog import print_variable, print_tag_variables, print_annotations, tag_map

# We should get range info in there....
table_schema_type_map = {
    'timestamp': ('timestamp', 'default'),
    'jsonb': ('object', 'default'),
    'float4': ('number', 'default'),
    'int4': ('integer', 'default'),
    'int8': ('integer', 'default'),
    'float8': ('number', 'default'),
    'text': ('string', 'default'),
    'date': ('date', 'default'),
    'json': ('object', 'default'),
    'boolean': ('boolean', 'default'),
    'int2': ('integer', 'default'),
    'timestamptz': ('datetime', 'default'),
    'timestamp[]': ('any', 'default'),
    'jsonb[]': ('array', 'default'),
    'float4[]': ('any', 'default'),
    'int4[]': ('integer', 'default'),
    'int8[]': ('integer', "default"),
    'float8[]': ('number', 'default'),
    'text[]': ('any', 'default'),
    'date[]': ('any', 'default'),
    'json[]': ('array', 'default'),
    'boolean[]': ('boolean', 'default'),
    'int2[]': ('integer', 'default'),
    'timestamptz[]': ('any', 'default'),
    'ermrest_uri': ('string', 'uri'),
    'ermrest_rid': 'string',
    'ermrest_rct': ('datetime', 'default'),
    'ermrest_rmt': ('datetime', 'default'),
    'ermrest_rcb': ('string', 'default'),
    'ermrest_rmb': ('string', 'default'),
}

table_schema_ermrest_type_map = {
    'string:default': 'text',
    'string:email': 'ermrest_uri',
    'string:uri': 'ermrest_uri',
    'string:binary': 'text',
    'string:uuid': 'text',
    'number:default': 'float8',
    'integer:default': 'integer4',
    'boolean:default': 'boolean',
    'object:default': 'json',
    'array:default': 'json[]',
    'date:default': 'date',
    'date:any': 'date',
    'time:default': 'timestampz',
    'time:any': 'timestampz',
    'datetime:default': 'date',
    'datetime:any': 'date',
    'year:default': 'date',
    'yearmonth:default': 'date'
}


def schema_from_catalog(server, catalog_id, schema_name, table_name):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    try:
        table_schema = Schema({})
        for col in table.column_definitions:
            field = Field({
                "name": col.name,
                "type": table_schema_type_map[col.type.typename],
            })
            if col.display:
                field.title = col.display
            if col.comment:
                field.description = col.comment
            if [col.name] in [i.unique_columns for i in table.keys]:
                field.constraints['unique'] = True
            field.constraints['required'] = not col.nullok
            if col.default:
                field.missingvalues = [col.default]
            table_schema.add_field(field.descriptor)
        table_schema.commit()
        if not table_schema.valid:
            print(table_schema.errors)
    except exceptions.ValidationError as exception:
        print('error.....')
        print(exception.errors)
    return table_schema


def print_table_annotations(table, stream):
    print_tag_variables({}, tag_map, stream)
    print_annotations({}, tag_map, stream, var_name='table_annotations')
    print_variable('table_comment', None, stream)
    print_variable('table_acls', None, stream)
    print_variable('table_acl_bindings', None, stream)


def print_column_annotations(schema, stream):
    column_annotations = {}
    column_acls = {}
    column_acl_bindings = {}
    column_comment = {}

    for i in schema.fields:
        if 'description' in i.descriptor and not (i.descriptor['description'] == '' or not i.descriptor['description']):
            column_comment[i.name] = i.comment

    print_variable('column_annotations', column_annotations, stream)
    print_variable('column_comment', column_comment, stream)
    print_variable('column_acls', column_acls, stream)
    print_variable('column_acl_bindings', column_acl_bindings, stream)
    return


def print_foreign_key_defs(table_schema, stream):
    s = 'fkey_defs = [\n'
    for fkey in table_schema.foreign_keys:
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


def print_key_defs(table_schema, schema_name, table_name, stream):
    s = 'key_defs = [\n'
    constraint_name = (schema_name, cannonical_column_name(f'{table_name}_{table_schema.primary_key}_Key)'))
    s += f"""    em.Key.define({table_schema.primary_key},
                 constraint_names={constraint_name},\n)\n"""

    for col in table_schema.fields:
        if col.required and col.constraints['unique']:
            constraint_name = (schema_name, cannonical_column_name(f'{table_name}_{col.name}_Key)'))
            s += f"""    em.Key.define([{col.name!r}],
                     constraint_names={constraint_name},\n"""
            s += '),\n'
    s += ']'
    print(autopep8.fix_code(s, options={}), file=stream)
    return


def print_column_defs(table_schema, stream):
    provide_system = True
    system_columns = ['RID', 'RCB', 'RMB', 'RCT', 'RMT']

    s = 'column_defs = ['
    for col in table_schema.fields:
        if col.name in system_columns:
            continue
        t = f"{col.type}:{col.format}"
        s += f"    em.Column.define('{col.name}', em.builtin_types['{table_schema_ermrest_type_map[t]}'],"
        if col.required:
            s += "nullok=False,"
        try:
            s += f"comment=column_comment['{col.descriptor['description']}'],"
        except KeyError:
            pass
        s += '),\n'
    s += ']'
    print(autopep8.fix_code(s, options={'aggressive': 8}), file=stream)
    return provide_system


def print_table_def(schema, stream):
    print_tag_variables({}, tag_map, stream)
    print_annotations({}, tag_map, stream, var_name='table_annotations')
    print_variable('table_comment', None, stream)
    print_variable('table_acls', {}, stream)
    print_variable('table_acl_bindings', {}, stream)
    return


def print_table(server, catalog_id, table_schema, schema_name, table_name, stream):
    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = '{}'
schema_name = '{}'
""".format(table_name, schema_name), file=stream)

    print_column_annotations(table_schema, stream)
    provide_system = print_column_defs(table_schema, stream)
    print_table_annotations(table_schema, stream)
    print_key_defs(table_schema, schema_name, table_name, stream)
    print_foreign_key_defs(table_schema, stream)
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


def cannonical_column_name(name):
    split_words = '[A-Z]+[a-z0-9]*|[a-z0-9]+'
    return '_'.join(list(map(lambda x: x[0].upper() + x[1:], re.findall(split_words, name))))


def convert_table_to_deriva(table_loc, server, catalog_id=1, schema_name, table_name=None, outfile=None,
                            map_column_names=False, key_columns=[]):
    """
    Read in a table, try to figure out the type of its columns and output a deriva-py program that can be used to create
    the table in a catalog.

    :param table_loc: Path or URL to the table
    :param server: Default server in which the table should be created.
    :param catalog_id: Default catalog_id into which the table should be created
    :param schema_name: Schema to be used for the table definition.
    :param table_name: Table name to be used.  Will default to file name.
    :param outfile: Where to put the deriva_py program.
    :param map_column_names:
    :param key_columns:
    :return:
    """
    column_map = {}
    table = Table(table_loc)
    table.infer()
    if map_column_names:
        for c in table.schema.fields:
            column_map[c.name] = cannonical_column_name(c.name)
            c.descriptor['name'] = column_map[c.name]
    table.schema.descriptor['primaryKey'] = 'RID'
    for i,col in enumerate(table.schema.fields):
        if col.name in key_columns:
            table.schema.descriptor['fields'][i]['constraints'] = {'required':True, 'unique':True}
    table.schema.commit()

    with open(outfile, 'w') as stream:
        print_table(server, catalog_id, table.schema, schema_name, table_name, stream)
    return column_map
