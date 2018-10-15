import argparse
import dump_table
import dump_schema
import pprint
import os
from deriva.core import ErmrestCatalog, get_credential

tag_map = {
    'bulk_upload':          'tag:isrd.isi.edu,2016:generated',
    'immutable':          'tag:isrd.isi.edu,2016:immutable',
    'display':            'tag:misd.isi.edu,2015:display',
    'visible_columns':    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys': 'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':        'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':      'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives': 'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':     'tag:isrd.isi.edu,2016:column-display',
    'asset':              'tag:isrd.isi.edu,2017:asset',
    'export':             'tag:isrd.isi.edu,2016:export',
}

def print_variable(name, value, stream):
    """
    Print out a variable assignment on one line if empty, otherwise pretty print.
    :param name:
    :param value:
    :param stream:
    :return:
    """
    if value == None or value == '' or value == [] or value == {}:
        print('{} = {}'.format(name,value), file= stream)
    else:
        print('{} = \\'.format(name), file=stream)
        pprint.pprint(value, width=80, depth=None, compact=True, stream=stream)
        print('', file=stream)


def print_tag_variables(annotations, tag_map, stream):
    for t,v in tag_map.items():
        if v in annotations:
            if v == '' or v == {} or v == None or v == {}:
                print("{} = {}".format(t,v))
            else:
                print('{} = \\'.format(t), file=stream)
                pprint.pprint(v, width=80, depth=None, compact=True, stream=stream)
                print('', file=stream)

def print_annotations(annotations, tag_map, stream):
    var_map = {v: k for k, v in tag_map.items()}
    if annotations == {}:
        print('annotations = {}', file=stream)
        return
    print('annotations = \\', file=stream)
    for t,v in annotations.items():
        if t in var_map:
            print('{} : {}'.format(t,var_map[t]), file=stream)
        else:
            print('{} : \\'.format(t), file=stream)
            pprint.pprint(v, width=80, depth=None, compact=True, stream=stream)


def print_catalog(server, catalog_id, dumpdir):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    with open('{}/catalog-{}'.format(dumpdir,catalog_id), 'w') as f:
        print_tag_variables(model_root.annotations, tag_map, f)
        print_annotations(model_root.annotations, tag_map, f)

        print_variable('acls', model_root.acls, f)
        print_variable('display', model_root.display, f)

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