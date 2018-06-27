import importlib
import argparse
from deriva.core import ErmrestCatalog, get_credential


def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {0}:{1}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--deletefks', help='delete existing foreign keys before loading)')
    parser.add_argument('--defpath', default='.', help='path to table definitions)')
    parser.add_argument('table', help='Name table to be loaded.')
    parser.add_argument('mode', choices=['table', 'annotations', 'fkeys', 'acls'],
                        help='Operation to perform')

    args = parser.parse_args()
    server = args.server
    mode = args.mode
    table = args.table
    defpath = args.defpath

    print('Importing ', table)

    module_spec = importlib.util.spec_from_file_location(table , '{}/{}_def.py'.format(defpath, table))
    mod = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(mod)

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[mod.schema_name]

    if mode != 'table':
        table = schema.tables[mod.table_name]

    skip_fkeys = False

    if mode == 'table':
        if skip_fkeys:
            mod.table_def.fkey_defs = []
        table = schema.create_table(catalog, mod.table_def)
    if mode == 'fkeys':
            print('deleting foreign_keys')
            for k in table.foreign_keys:
                k.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[mod.schema_name]
            table = schema.tables[mod.table_name]
            for i in mod.fkey_defs:
                table.create_fkey(catalog, i)

    if mode == 'annotations':
        if len(mod.visible_columns) > 0:
            for k, v in mod.visible_columns.items():
                table.visible_columns[k] = v

        if len(mod.visible_foreign_keys) > 0:
            for k, v in mod.visible_foreign_keys.items():
                table.visible_foreign_keys[k] = v
        table.annotations['table_display'] = mod.table_display
        table.apply(catalog)

    if mode == 'acls':
        if len(mod.acls > 0):
            for k, v in mod.acls.items():
                table.acls[k] = v

        if len(mod.acl_bindings > 0):
            for k, v in mod.acl_bindings.items():
                table.acl_bindings[k] = v
        table.acl_bindings['table_display'] = mod.table_display
        table.apply(catalog)


if __name__ == "__main__":
    main()
