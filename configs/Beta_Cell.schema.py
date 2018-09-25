import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    'Protocol_Step',
    'Protocol',
    'Protocol_Type',
    'Protocol_Step_Additive_Term',
]
annotations = \
{'tag:misd.isi.edu,2015:display': {'name_style': {'underline_space': True}}}

schema_def = em.Schema.define(
        'Beta_Cell',
        comment=None,
        acls=acls,
        annotations=annotations,
    )

def main():
    parser = argparse.ArgumentParser(description='Load  defs for schema Beta_Cell')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'Beta_Cell'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(catalog, schema_def)


if __name__ == "__main__":
    main()
