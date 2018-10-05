import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    'group_lists',
]

schema_def = em.Schema.define(
        '_acl_admin',
        comment=None,
        acls=acls,
        annotations=annotations,
    )

def main():
    parser = argparse.ArgumentParser(description='Load  defs for schema _acl_admin')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = '_acl_admin'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(catalog, schema_def)


if __name__ == "__main__":
    main()