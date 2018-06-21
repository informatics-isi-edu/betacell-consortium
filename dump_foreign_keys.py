import argparse
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint


def dump_foreign_keys(table):
    fks =  [
        {
            'foreign_key_columns': [ c['column_name'] for c in i.foreign_key_columns],
            'pk_schema': i.referenced_columns[0]['schema_name'],
            'pk_table': i.referenced_columns[0]['table_name'],
            'pk_columns': [ c['column_name'] for c in i.referenced_columns],
            'constraint_names': i.names,
            'annotations': i.annotations,
            'acls': i.acls, 'acl_bindings' : i.acl_bindings,
            'on_update' : i.on_update, 'on_delete': i.on_delete,
            'comment': "'" + i.comment + "'"
        } for i in table.foreign_keys
    ]
    return fks

def main():
    parser = argparse.ArgumentParser(description='Generate a table configuration from an existing table.')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
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
from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em"""

    print('\nfkey_defs = [')
    for i in dump_foreign_keys(table):
        print("""    em.ForeignKey.define(
            {},
            '{}', '{}', {},
            constraint_names={},
            annotations={},
            acls={},
            acl_bindings={},
            on_update='{}', on_delete='{}',
            comment={}),""".format(i['foreign_key_columns'], i['pk_schema'], i['pk_table'], i['pk_columns'],
                                   i['constraint_names'], i['annotations'], i['acls'], i['acl_bindings'],
                                   i['on_update'], i['on_delete'], i['comment']))
    print(']')
    print("""
    
def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table {}:{}')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', help='delete existing foreign keys before loading)')

    args = parser.parse_args()

    delete_fkeys = args.delete
    
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    if delete_fkeys:
        pass
        
    for i in fkey_defs:
        table.create_fkey(catalog, i)

if __name__ == "__main__":
    main()    
    """.format(schema_name, table_name))

if __name__ == "__main__":
    main()