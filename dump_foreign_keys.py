import argparse
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import re


def dump_foreign_keys(table):
    fks = []
    for key in table.foreign_keys:
        fk = {
            'foreign_key_columns': [c['column_name'] for c in key.foreign_key_columns],
            'pk_schema': key.referenced_columns[0]['schema_name'],
            'pk_table': key.referenced_columns[0]['table_name'],
            'pk_columns': [c['column_name'] for c in key.referenced_columns],
            'constraint_names': key.names,
        }
        for i in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            a = getattr(key, i)
            if not (a == {} or a == None or a == 'NO ACTION'):
                fk[i] = "'" + a + "'" if re.match('comment|on_update|on_delete', i) else a
        fks.append(fk)
    return fks


def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {}:{}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', help='delete existing foreign keys before loading)')
    parser.add_argument('table', help='schema:table_name)')

    args = parser.parse_args()

    server = args.server
    schema_name = args.table.split(':')[0]
    table_name = args.table.split(':')[1]

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]
    print("""import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em""")

    print('\nfkey_defs = [')
    for i in dump_foreign_keys(table):
        print("""    em.ForeignKey.define(
        {},
        '{}', '{}', {},
        constraint_names = {},""".format(i['foreign_key_columns'],
                                         i['pk_schema'],
                                         i['pk_table'],
                                         i['pk_columns'],
                                         i['constraint_names']))

        for k in ['annotations', 'acls', 'acl_bindings', 'on_update', 'on_delete', 'comment']:
            if k in i:
                print("        {} = {},".format(k, i[k]))
        print('    ),')

    print(']')
    print("""
def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {0}:{1}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', action="store_true", help='delete existing foreign keys before loading)')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = '{0}'
    table_name = '{1}'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]
    
    if delete_fkeys:
        for k in table.foreign_keys:
            k.delete(catalog)
            
    model_root = catalog.getCatalogModel()
    for i in fkey_defs:
        table.create_fkey(catalog,i)

if __name__ == "__main__":
    main()""".format(schema_name, table_name))


if __name__ == "__main__":
    main()
