import argparse
import dump_table
import pprint
import os
import autopep8
from deriva.core import ErmrestCatalog, get_credential

tag_map = {
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
    'generated':          'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':        'tag:isrd.isi.edu,2017:bulk-upload'
}



def print_variable(name, value, stream):
    """
    Print out a variable assignment on one line if empty, otherwise pretty print.
    :param name:
    :param value:
    :param stream:
    :return:
    """
    if not value or value == '' or value == [] or value == {}:
        s = '{} = {}'.format(name,value)
    else:
 #       s = '{} = '.format(name)
        s = '{} = {}'.format(name, pprint.pformat(value, indent=4, width=80, depth=None, compact=False))
#        s += ''
    print(autopep8.fix_code(s, options={'aggressive': 4}), file=stream)


def print_tag_variables(annotations, cdtag_map, stream):
    """
    For each convenient annotation name in tag_map, print out a variable declaration of the form annotation = v where
    v is the value of the annotation the dictionary.  If the tag is not in the set of annotations, do nothing.
    :param annotations:
    :param tag_map:
    :param stream:
    :return:
    """
    for t,v in tag_map.items():
        if v in annotations:
            print_variable(t, annotations[v], stream)


def print_annotations(annotations, tag_map, stream, var_name='annotations'):
    """
    Print out the annotation definition in annotations, substituting the python variable for each of the tags specified
    in tag_map.
    :param annotations:
    :param tag_map:
    :param stream:
    :return:
    """
    var_map = {v: k for k, v in tag_map.items()}
    if annotations == {}:
        s = '{} = {{}}'.format(var_name)
    else:
        s = '{} = {{'.format(var_name)
        for t,v in annotations.items():
            if t in var_map:
                # Use variable value rather then inline annotation value.
                s += "'{}' : {},".format(t, var_map[t])
            else:
                s +=  "'{}' : ".format(t)
                s += pprint.pformat(v, width=80, depth=None, compact=True)
                s += ','
        s += '}'
    print(autopep8.fix_code(s, options={'aggressive': 4}), file=stream)

def print_schema(server, catalog_id, schema_name, stream):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]

    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog
""", file=stream)
    print('table_names = [', file=stream)
    for i in schema.tables:
        print("    '{}',".format(i), file=stream)
    print(']\n', file=stream)
    print_tag_variables(schema.annotations, tag_map, stream)
    print_annotations(schema.annotations, tag_map, stream)
    print_variable('acls', schema.acls, stream)
    print_variable('comment', schema.comment, stream)
    print('''schema_def = em.Schema.define(
        '{0}',
        comment=comment,
        acls=acls,
        annotations=annotations,
    )


def main():
    server = '{0}'
    catalog_id = {1}
    schema_name = '{2}'
    update_catalog.update_schema(server, catalog_id, schema_name, schema_def, annotations, acls, comment)


if __name__ == "__main__":
    main()'''.format(server, catalog_id, schema_name), file=stream)


def print_catalog(server, catalog_id, dumpdir):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()

    try:
        os.makedirs(dumpdir, exist_ok=True)
    except OSError:
        print("Creation of the directory %s failed" % dumpdir)

    with open('{}/catalog_{}.py'.format(dumpdir,catalog_id), 'w') as f:
        print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import update_catalog
import deriva.core.ermrest_model as em
""", file=f)
        print_tag_variables(model_root.annotations, tag_map, f)
        print_annotations(model_root.annotations, tag_map, f)
#        print_variable('comment', model_root.comment, f)
        print_variable('acls', model_root.acls, f)
        print('''
comment = None


def main():
    server = '{0}'
    catalog_id = {1}
    update_catalog.update_catalog(server, catalog_id, annotations, acls, comment)
    

if __name__ == "__main__":
    main()'''.format(server, catalog_id), file=f)

    for schema_name, schema in model_root.schemas.items():
        filename = '{}/{}.schema.py'.format(dumpdir, schema_name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as f:
            print_schema(server, catalog_id, schema_name, f)
        f.close()

        for i in schema.tables:
            print('Dumping {}:{}'.format(schema_name, i))
            filename = '{}/{}/{}.py'.format(dumpdir, schema_name, i)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
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