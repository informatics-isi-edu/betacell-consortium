import argparse
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import sys


def print_schema(server, schema_name, stream):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]

    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
""", file=stream)
    print('table_names = [', file=stream)
    for i in schema.tables:
        print("    '{}',".format(i), file=stream)
    print(']', file=stream)

    if schema.annotations != {}:
        print('annotations = \\', file=stream)
        pprint.pprint(schema.annotations, indent=4, width=80, depth=None, compact=False, stream=stream)
    if schema.acls != {}:
        print('acls = \\', file=stream)
        pprint.pprint(schema.acls, indent=4, width=80, depth=None, compact=False, stream=stream)

    print('''
schema_def = em.Schema.define(
        '{}',
        comment={},
        acls=acls,
        annotations=annotations,
    )'''.format(schema.name,
                "'" + schema.comment + "'" if schema.comment is not None else None), file=stream)

    print("""
def main():
    parser = argparse.ArgumentParser(description='Load  defs for schema {0}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = '{0}'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(catalog, schema_def)


if __name__ == "__main__":
    main()""".format(schema_name), file=stream)


def main():
    parser = argparse.ArgumentParser(description='Dump definition for schema {}:{}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('schema', help='schema)')
    parser.add_argument('--outfile', default="stdout", help='output file name)')
    args = parser.parse_args()

    server = args.server
    outfile = args.outfile
    server = args.server
    schema_name = args.schema

    if outfile == 'stdout':
        print_schema(server, schema_name, sys.stdout)
    else:
        with open(outfile, 'w') as f:
            print_schema(server, schema_name, f)
        f.close()

if __name__ == "__main__":
    main()
