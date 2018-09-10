import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    'protocol',
    'process',
    'dataset',
    'dataset_instrument',
    'mesh_data',
    'file',
    'project_publication',
    'cell_line',
    'project_investigator',
    'publication',
    'imaging_data',
    'specimen_compound',
    'experiment',
    'replicate',
    'biosample',
    'project_member',
    'BellCellPlate',
    'processed_tomography_data',
    'dataset_experiment_type',
    'specimen',
    'icon',
    'pipeline',
    'external_reference',
    'BellCellStatus',
    'project',
    'person',
    'xray_tomography_data',
]
annotations = \
{   'tag:misd.isi.edu,2015:display': {   'name_style': {   'title_case': True,
                                                           'underline_space': True}}}

schema_def = em.Schema.define(
        'isa',
        comment=None,
        acls=acls,
        annotations=annotations,
    )

def main():
    parser = argparse.ArgumentParser(description='Load  defs for schema isa')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'isa'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(catalog, schema_def)


if __name__ == "__main__":
    main()
