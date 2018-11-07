import importlib
import argparse
from requests.exceptions import HTTPError

from deriva.core import ErmrestCatalog, get_credential


def parse_args(server, catalog_id, is_table=False, is_catalog=False):

    parser = argparse.ArgumentParser(description='Update catalog configuration')
    parser.add_argument('--server', default=server, help='Catalog server name')
    parser.add_argument('--catalog', default=catalog_id, help='ID of desired catalog')
    parser.add_argument('--replace', action='store_true',
                        help='Replace existing values with new ones.  Otherwise, attempt to merge in values provided.')

    if is_table:
        modes = ['table', 'annotations', 'acls', 'comments', 'keys', 'fkeys', 'columns']
    elif is_catalog:
        modes = ['annotations', 'acls']
    else:
        modes = ['schema', 'annotations', 'acls', 'comments']

    parser.add_argument('mode', choices=modes,
                        help='Model element to be updated.')

    args = parser.parse_args()
    return args.server, args.catalog, args.mode, args.replace


def update_annotations(o,annotations, replace=False):
    if replace:
        o.annotations.update(annotations)
    else:
        for k, v in annotations.items():
            o.annotations[k] = v

def update_acls(o,acls, replace=False):
    if replace:
        o.acls.update(acls)
    else:
        for k, v in acls.items():
            o.acls[k] = v

def update_acl_bindings(o,acl_bindings, replace=False):
    if replace:
        o.acl_bindings.update(acl_bindings)
    else:
        for k, v in acl_bindings.items():
            o.acl_bindingss[k] = v

def update_catalog(mode, replace, server, catalog_id, annotations, acls):

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    if mode == 'annotations':
        update_annotations(model_root, annotations, replace)
    elif mode == 'acls':
        update_acls(model_root,acls, replace)
    model_root.apply(catalog)


def update_schema(mode, replace, server, catalog_id, schema_name, schema_def, annotations, acls, comment):

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    if mode == 'schema':
        if replace:
            schema = model_root.schemas[schema_name]
            print('Deleting schema ', schema.name)
            ok = input('Type YES to confirm:')
            if ok == 'YES':
                schema.delete(catalog)
            model_root = catalog.getCatalogModel()
        schema = model_root.create_schema(catalog, schema_def)
    else:
        schema = model_root.schemas[schema_name]
        if mode == 'annotations':
            update_annotations(schema,annotations, replace)
        elif mode == 'acls':
            update_acls(schema, acls, replace)
        elif mode == 'comment':
            schema.comment = comment
    model_root.apply(catalog)
    return schema


def update_table(mode, replace, server, catalog_id, schema_name, table_name, table_def, column_defs, key_defs, fkey_defs,
                 table_annotations, table_acls, table_acl_bindings, table_comment,
                 column_annotations, column_acls, column_acl_bindings, column_comment):

    print('Importing {}:{}'.format(schema_name, table_name))

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]

    skip_fkeys = False

    if mode == 'table':
        if replace:
            table = schema.tables[table_name]
            print('Deleting table ', table.name)
            ok = input('Type YES to confirm:')
            if ok == 'YES':
                table.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[schema_name]
        if skip_fkeys:
            table_def.fkey_defs = []
        table = schema.create_table(catalog, table_def)
        return table

    table = schema.tables[table_name]
    if mode == 'columns':
        if replace:
            print('deleting columns')
            for k in table.column_definitions:
                k.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[schema_name]
            table = schema.tables[table_name]
        cnames = [i.name for i in table.column_definitions]
        # Go through the column definitions and add a new column if it doesn't already exist.
        for i in column_defs:
            if i['name'] not in cnames:
                print('Creating column {}'.format(i['name']))
                table.create_column(catalog, i)
    if mode == 'fkeys':
        if replace:
            print('deleting foreign_keys')
            for k in table.foreign_keys:
                k.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[schema_name]
            table = schema.tables[table_name]

        for i in fkey_defs:
            try:
                table.create_fkey(catalog, i)
                print('Created foreign key {} {}'.format(i['names'], i))
            except HTTPError:
                print("Skipping: foreign key {} {} already exists".format(i['names'], i))
    if mode == 'keys':
        if replace:
            print('deleting keys')
            for k in table.keys:
                k.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[schema_name]
            table = schema.tables[table_name]
        for i in key_defs:
            try:
                table.create_key(catalog, i)
                print('Created key {}'.format(i['names']))
            except HTTPError:
                print("Skipping: key {} already exists".format(i['names']))

    if mode == 'annotations':
        update_annotations(table, table_annotations, replace)

        for c in table.column_definitions:
            if c.name in column_annotations:
                update_annotations(c, column_annotations[c.name], replace)

    if mode == 'comment':
        table.comment = table_comment
        for c in table.column_definitions:
            if c.name in column_comment:
                c.comment = column_comment[c.name]

    if mode == 'acls':
        update_acls(table, table_acls, replace)
        update_acl_bindings(table, table_acl_bindings, replace)
        for c in table.column_definitions:
            if c.name in column_acls:
                update_acls(c, column_acls[c.name], replace)
            if c.name in column_acl_bindings:
                update_acl_bindings(c, column_acl_bindings[c.name], replace)

    table.apply(catalog)