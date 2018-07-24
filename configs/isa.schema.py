import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    protocol,
    dataset_gene,
    library,
    dataset,
    sample,
    dataset_instrument,
    mesh_data,
    file,
    project_publication,
    cell_line,
    dataset_data_type,
    alignment,
    project_investigator,
    publication,
    imaging_data,
    experiment,
    replicate,
    processed_data,
    project_member,
    BellCellPlate,
    thumbnail,
    biosample,
    dataset_experiment_type,
    specimen,
    previews,
    dataset_gender,
    dataset_anatomy,
    icon,
    pipeline,
    dataset_human_age,
    external_reference,
    sample_replicate_group,
    BellCellStatus,
    project,
    person,
    xray_tomography_data,
    protocol_compound,
    dataset_organism,
]
annotations = \
{   'tag:misd.isi.edu,2015:display': {   'name_style': {   'title_case': True,
                                                           'underline_space': True}}}
acls = \
{   'delete': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                  'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                  'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a'],
    'insert': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                  'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                  'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                  'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
    'update': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                  'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                  'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a']}

schema_def = em.Schema.define(
        'isa',
        comment=None,
        acls=acls,
        acl_bindings=acl_bindings
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
