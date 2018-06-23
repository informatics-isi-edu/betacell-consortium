# This script will query a catalog and dump out the annotations for a table. These are then output into a new
# script that can recreate those annotations.

import argparse
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint

def print_table_annotations(server, schema_name, table_name, stream):

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]
    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    """, file=stream)

    table_annotations = {
        'visible_columns': table.visible_columns,
        'visible_foreign_keys': table.visible_foreign_keys,
        'table_display': table.table_display,
        'annotations': table.annotations,
        'table_acls': table.acls,
        'table_acl_bindings': table.acl_bindings
    }
    for k, v in table_annotations.items():
        if v != {}:
            print('{} = \\'.format(k), file=stream)
            pprint.pprint(v, indent=4, width=80, depth=None, compact=False, stream=stream)

    column_annotations = {}
    column_acls = {}
    column_acl_bindings = {}
    for i in table.column_definitions:
        if i.annotations != {}:
            column_annotations[i.name] = i.annotations
        if i.acls != {}:
            column_acls[i.name] = i.acls
        if i.acl_bindings != {}:
            column_acl_bindings[i.name] = i.acl_bindings
    if column_annotations != {}:
        print('column_annotations = \\', file=stream)
        pprint.pprint(column_annotations, indent=4, width=80, depth=None, compact=False, stream=stream)
    if column_acls != {}:
        print('column_acls = \\', file=stream)
        pprint.pprint(column_acls, indent=4, width=80, depth=None, compact=False, stream=stream)
    if column_acl_bindings != {}:
        print('column_acl_bindings = \\', file=stream)
        pprint.pprint(column_acl_bindings, indent=1, width=80, depth=None, compact=False, stream=stream)

    print("""
def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table {0}:{1}')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = '{0}'
        table_name = '{1}'

        credential = get_credential(server)
        catalog = ErmrestCatalog('https', server, 1, credentials=credential)
        model_root = catalog.getCatalogModel()
        schema = model_root.schemas[schema_name]
        table = schema.tables[table_name]

        if len(visible_columns) > 0:
            for k, v in visible_columns.items():
                table.visible_columns[k] = v

        if len(visible_foreign_keys) > 0:
            for k, v in visible_foreign_keys.items():
                table.visible_foreign_keys[k] = v
        table.annotations['table_display'] = table_display

        table.apply(catalog)


if __name__ == "__main__":
        main()""".format(schema_name, table_name), file=stream)

def main():
    parser = argparse.ArgumentParser(description='Dump annotations  for table {}:{}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('table', help='schema:table_name)')
    parser.add_argument('--outfile', default="stdout", help='output file name)')
    args = parser.parse_args()

    server = args.server
    schema_name = args.table.split(':')[0]
    table_name = args.table.split(':')[1]
    outfile = args.outfile

    if outfile == 'stdout':
        print_table_annotations(server, schema_name, table_name, sys.stdout)
    else:
        with open(outfile, 'w') as f:
            print_table_annotations(server, schema_name, table_name, f)
        f.close()


if __name__ == "__main__":
    main()
