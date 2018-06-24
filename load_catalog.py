import importlib
import argparse
from deriva.core import ErmrestCatalog, get_credential


def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {0}:{1}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', help='delete existing foreign keys before loading)')
    parser.add_argument('file', help='Name of file with table definitions.')
    parser.add_argument('mode', help='Operation to perform: table|annotations|fkeys')

    create_table = load_fkeys = load_annotations = load_acls = False

    args = parser.parse_args()
    server = args.server
    if args.mode == 'table':
        create_table = True
    elif args.mode == 'annotations':
        load_annotations = True
    elif args.mode == 'fkeys':
        load_fkeys = True
    elif args.mode == 'acls':
        load_acls = True
    else:
        print("Invalad mode")
        return

    print('Importing ', args.file)
    mod = importlib.import_module(args.file)

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[mod.schema_name]
    table = schema.tables[mod.table_name]

    skip_fkeys = False

    if create_table:
        if skip_fkeys:
            mod.table_def.fkey_defs = []
        print(mod.table_def)
  #      table = schema.create_table(catalog, mod.table_def)
    if load_fkeys:
            for k in table.foreign_keys:
                k.delete(catalog)
            for i in mod.fkey_defs:
                table.create_fkey(catalog, i)

    if load_annotations:
        if len(mod.visible_columns) > 0:
            for k, v in mod.visible_columns.items():
                table.visible_columns[k] = v

        if len(mod.visible_foreign_keys) > 0:
            for k, v in mod.visible_foreign_keys.items():
                table.visible_foreign_keys[k] = v
        table.annotations['table_display'] = mod.table_display
        table.apply(catalog)

    if load_acls:
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
