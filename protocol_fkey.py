import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

fkey_defs = [
]

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:protocol')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', default=False, help='delete existing foreign keys before loading)')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'isa'
    table_name = 'protocol'

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
    main()
