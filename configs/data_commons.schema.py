import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    'db',
    'cvtermprop',
    'cv',
    'cvterm_dbxref',
    'domain_registry',
    'cvtermpath',
    'cvterm',
    'cvterm_relationship',
    'relationship_types',
    'dbxref',
    'cvtermsynonym',
]

schema_def = em.Schema.define(
        'data_commons',
        comment=None,
        acls=acls,
        annotations=annotations,
    )

def main():
    parser = argparse.ArgumentParser(description='Load  defs for schema data_commons')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'data_commons'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(catalog, schema_def)


if __name__ == "__main__":
    main()
