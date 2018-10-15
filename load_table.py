import importlib
import argparse
from deriva.core import ErmrestCatalog, get_credential


def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {0}:{1}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--replace', action='store_true', help='replace existing values with new ones ')
    parser.add_argument('--defpath', default='configs', help='path to table definitions')
    parser.add_argument('--catalog', default=1, help='Catalog id (integer)')
    parser.add_argument('table', help='Name table to be loaded schema:table.')
    parser.add_argument('mode', choices=['table', 'columns', 'annotations', 'comment', 'keys', 'fkeys', 'acls'],
                        help='Operation to perform')

    args = parser.parse_args()
    server = args.server
    catalog_number = args.catalog
    mode = args.mode
    defpath = args.defpath
    replace = args.replace

    schema_arg = args.table.split(':')[0]
    table_arg = args.table.split(':')[1]

    print('Importing {}:{}'.format(schema_arg, table_arg) )

    module_spec = importlib.util.spec_from_file_location(table_arg, '{}/{}/{}.py'.format(defpath, schema_arg, table_arg))
    mod = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(mod)

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_number, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[mod.schema_name]

    if mode != 'table':
        table = schema.tables[mod.table_name]

    skip_fkeys = False

    if mode == 'table':
        if replace:
            print('deleting table', table.name)
            table.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[mod.schema_name]
        if skip_fkeys:
            mod.table_def.fkey_defs = []
        table = schema.create_table(catalog, mod.table_def)
    if mode == 'columns':
        if replace:
            print('deleting columns')
            for k in table.column_definitions:
                k.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[mod.schema_name]
            table = schema.tables[mod.table_name]
        cnames = [i.name for i in table.column_definitions]
        # Go through the column definitions and add a new column if it doesn't already exist.
        for i in mod.column_defs:
            if i['name'] not in cnames:
                print('Creating column {}'.format(i['name']))
                table.create_column(catalog, i)
    if mode == 'fkeys':
            if replace:
                print('deleting foreign_keys')
                for k in table.foreign_keys:
                    k.delete(catalog)
                model_root = catalog.getCatalogModel()
                schema = model_root.schemas[mod.schema_name]
                table = schema.tables[mod.table_name]
            fknames = [i.names for i in table.foreign_keys]
            for i in mod.fkey_defs:
                if i['names'] not in fknames:
                    print('Creating foreign key {} {}'.format(i['names'], i))
                    table.create_fkey(catalog, i)
    if mode == 'keys':
            if replace:
                print('deleting keys')
                for k in table.keys:
                    k.delete(catalog)
                model_root = catalog.getCatalogModel()
                schema = model_root.schemas[mod.schema_name]
                table = schema.tables[mod.table_name]
            knames = [i.names for i in table.keys]
            for i in mod.key_defs:
                if i['names'] not in knames:
                    print('Creating key {} {}'.format(i['names'], i))
                    table.create_key(catalog, i)
    if mode == 'annotations':
        if len(mod.table_annotations) > 0:
            for k,v in mod.table_annotations.items():
                print('setting table annotation', k)
                table.annotations[k] = v

        if len(mod.column_annotations) > 0:
            for c in table.column_definitions:
                if c.name in mod.column_annotations:
                    for k, v in mod.column_annotations[c.name].items():
                        print('setting column annotation', c.name, k)
                        c.annotations[k] = v

        table.apply(catalog)

    if mode == 'comment':
        table._comment = mod.table_comment
        for c in table.column_definitions:
            if c.name in mod.column_comment:
                c._comment = mod.column_comment[c.name]
        table.apply(catalog)

    if mode == 'acls':
        for k, v in mod.table_acls.items():
            table.acls[k] = v

        for k, v in mod.acl_bindings.items():
            table.acl_bindings[k] = v
        table.acl_bindings['table_display'] = mod.table_display
        table.apply(catalog)

    if mode == 'catalog':
        model_root.annotations['tag:isrd.isi.edu,2017:bulk-upload'] = config
        model_root.apply(catalog)

if __name__ == "__main__":
    main()
