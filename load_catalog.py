import importlib
import argparse
from deriva.core import ErmrestCatalog, get_credential


def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {0}:{1}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--replace', action='store_true', help='replace existing values with new ones )')
    parser.add_argument('--defpath', default='.', help='path to table definitions)')
    parser.add_argument('table', help='Name table to be loaded.')
    parser.add_argument('mode', choices=['table', 'columns', 'annotations', 'comment', 'fkeys', 'acls'],
                        help='Operation to perform')

    args = parser.parse_args()
    server = args.server
    mode = args.mode
    table = args.table
    defpath = args.defpath
    replace = args.replace

    print('Importing ', table)

    module_spec = importlib.util.spec_from_file_location(table, '{}/{}_def.py'.format(defpath, table))
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
    if mode == 'columns':
        if replace:
            print('deleting columns')
            for k in table.column_definitions:
                k.delete(catalog)
            model_root = catalog.getCatalogModel()
            schema = model_root.schemas[mod.schema_name]
            table = schema.tables[mod.table_name]
        cnames = [i.name for i in table.column_definitions]
        for i in mod.column_defs:
            if i.name not in cnames:
                print('Creating column {}'.format(i.name))
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
                    print('Creating foreign key {}'.format(i['names']))
                    table.create_fkey(catalog, i)
    if mode == 'annotations':
        if len(mod.table_annotations) > 0:
            for k,v in mod.table_annotations.items():
                table.annotations[k] = v

        if len(mod.column_annotations) > 0:
            for c in table.column_definitions:
                if c.name in mod.column_annotations:
                    for k, v in mod.column_annotations[c.name].items():
                        c.annotations[k] = v

        table.apply(catalog)

    if mode == 'comment':
        table._comment = mod.table_comment
        for c in table.column_definitions:
            if c.name in mod.column_comment:
                c._comment = mod.column_comment[c.name]

    if mode == 'acls':
        for k, v in mod.table_acls.items():
            table.acls[k] = v

        for k, v in mod.acl_bindings.items():
            table.acl_bindings[k] = v
        table.acl_bindings['table_display'] = mod.table_display
        table.apply(catalog)


if __name__ == "__main__":
    main()
