import importlib
import argparse
from deriva.core import ErmrestCatalog, get_credential



def parse_args(server,catalog_id, is_table=False, is_catalog=False):

    parser = argparse.ArgumentParser(description='Update catalog configuration')
    parser.add_argument('--server',  default=server, help='Catalog server name')
    parser.add_argument('--catalog', default=catalog_id, help='ID of desired catalog')
    parser.add_argument('--replace', action='store_true', help='replace existing values with new ones ')

    modes = ['annotations','comment','acls'] + (['keys','fkeys','columns'] if is_table else [])
    modes = modes + (['create'] if not is_catalog else [])
    parser.add_argument('mode', choices=modes,
                        help='Operation to perform')

    args = parser.parse_args()
    return args.server, args.catalog,args.mode,args.replace

def update_annotations(object, annotations):
    for k,v in annotations.items():
        print('setting annotation', k)
        object.annotations[k] = v
    return


def update_comment(object, comment):
    object.comment = comment
    return

def update_acls(object, acls):
    object.acls = acls
    return

def update_catalog(server, catalog_id, annotations, acls, comment):
    server, catalog_id, mode, replace = parse_args(server,catalog_id, is_catalog=True)

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    if mode == 'annotations':
        update_annotations(model_root, annotations)
    elif mode == 'acls':
        update_acls(model_root,acls)
    elif mode == 'comment':
        update_comment(model_root, comment)
    model_root.apply(catalog)

def update_schema(server, catalog_id, schema_name, schema_def, annotations, acls, comment):

    server, catalog_id, mode, replace = parse_args(server,catalog_id)

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    if mode == 'create':
        schema = model_root.create_schema(catalog, schema_def)
    else:
        schema = model_root.schemas[schema_name]
        if mode == 'annotations':
            update_annotations(schema, annotations)
        elif mode == 'acls':
            update_acls(schema,acls)
        elif mode == 'comment':
            update_comment(schema, comment)
    model_root.apply(catalog)

def update_table(server, catalog_id, schema_name, table_name, table_def, column_defs, key_defs, fkey_defs,
                            table_annotations, table_acls, acl_bindings, table_comment,
                            column_annotations, column_acls, column_acl_bindings, column_comment):

    server, catalog_id, mode, replace = parse_args(server,catalog_id, is_table=True)

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    print('Importing {}:{}'.format(schema_name, table_name) )

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]

    if mode != 'create':
        table = schema.tables[table_name]

    skip_fkeys = False

    if mode == 'create':
        if replace:
            print('deleting table', table.name)
            table.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[schema_name]
        if skip_fkeys:
            table_def.fkey_defs = []
        table = schema.create_table(catalog, table_def)
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
            fknames = [i.names for i in table.foreign_keys]
            for i in fkey_defs:
                if i['names'] not in fknames:
                    print('Creating foreign key {} {}'.format(i['names'], i))
                    table.create_fkey(catalog, i)
    if mode == 'keys':
            if replace:
                print('deleting keys')
                for k in table.keys:
                    k.delete(catalog)
                model_root = catalog.getCatalogModel()
                schema = model_root.schemas[schema_name]
                table = schema.tables[table_name]
            knames = [i.names for i in table.keys]
            for i in key_defs:
                if i['names'] not in knames:
                    print('Creating key {} {}'.format(i['names'], i))
                    table.create_key(catalog, i)
    if mode == 'annotations':
        if len(table_annotations) > 0:
            for k,v in table_annotations.items():
                print('setting table annotation', k)
                table.annotations[k] = v

        if len(column_annotations) > 0:
            for c in table.column_definitions:
                if c.name in column_annotations:
                    for k, v in column_annotations[c.name].items():
                        print('setting column annotation', c.name, k)
                        c.annotations[k] = v

        table.apply(catalog)

    if mode == 'comment':
        table._comment = table_comment
        for c in table.column_definitions:
            if c.name in column_comment:
                c._comment = column_comment[c.name]
        table.apply(catalog)

    if mode == 'acls':
        for k, v in table_acls.items():
            table.acls[k] = v

        for k, v in acl_bindings.items():
            table.acl_bindings[k] = v
        table.acl_bindings['table_display'] = table_display
        table.apply(catalog)

