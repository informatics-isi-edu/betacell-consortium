import argparse
import dump_table
import dump_schema
import os
from deriva.core import ErmrestCatalog, get_credential

def print_catalog(server, catalog_id, dumpdir):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    for schema_name, schema in model_root.schemas.items():
        filename = '{}/{}.schema.py'.format(dumpdir, schema_name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as f:
            dump_schema.print_schema(server, catalog_id, schema_name, f)
        f.close()

        for i in schema.tables:
            print('Dumping {},{}'.format(schema_name, i))
            filename = 'configs/{}/{}.py'.format(schema_name, i)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                print('dumping table ', filename)
                dump_table.print_defs(server, catalog_id, schema_name, i, f)
            f.close()

def main():
    parser = argparse.ArgumentParser(description='Dump definition for catalog {}:{}')
    parser.add_argument('server', help='Catalog server name')
    parser.add_argument('--catalog', default=1, help='ID number of desired catalog')
    parser.add_argument('--dir', default="configs", help='output directory name)')
    args = parser.parse_args()

    server = args.server
    dumpdir = args.dir
    server = args.server
    catalog_id = args.catalog

    print_catalog(server, catalog_id,dumpdir)


if __name__ == "__main__":
    main()