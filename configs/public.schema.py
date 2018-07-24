import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    ermrest_client,
]
acls = \
{'delete': [], 'enumerate': [], 'insert': [], 'select': [], 'update': []}

schema_def = em.Schema.define(
        'public',
        comment='standard public schema',
        acls=acls,
        acl_bindings=acl_bindings
        annotations=annotations,
    )

def main():
    parser = argparse.ArgumentParser(description='Load  defs for schema public')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'public'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(catalog, schema_def)


if __name__ == "__main__":
    main()
