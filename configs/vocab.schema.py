import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    'uniprot_terms',
    'anatomy_terms',
    'cellular_location_terms',
    'dataset_status_terms',
    'data_type_terms',
    'gender_terms',
    'cell_line_terms',
    'experiment_type_terms',
    'image_creation_device_terms',
    'file_type_terms',
    'origin_terms',
    'specimen_terms',
    'instrument_terms',
    'phenotype_terms',
    'file_format_terms',
    'specimen_type_terms',
    'species_terms',
]
annotations = \
{   'tag:misd.isi.edu,2015:display': {   'name_style': {   'title_case': True,
                                                           'underline_space': True}}}

schema_def = em.Schema.define(
        'vocab',
        comment=None,
        acls=acls,
        annotations=annotations,
    )

def main():
    parser = argparse.ArgumentParser(description='Load  defs for schema vocab')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'vocab'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(catalog, schema_def)


if __name__ == "__main__":
    main()
