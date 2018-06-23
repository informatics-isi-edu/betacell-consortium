import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_names = [
    chromatin_modifier_terms,
    anatomy_terms,
    image_creation_device_terms,
    mutation_terms,
    file_extension,
    gender_terms,
    cell_line_terms,
    instrument_terms,
    target_of_assay_terms,
    phenotype_terms,
    human_age_terms,
    file_format_terms,
    origin_terms,
    dataset_status_terms,
    data_type_terms,
    rnaseq_selection_terms,
    specimen_terms,
    genotype_terms,
    histone_modification_terms,
    paired_end_or_single_read_terms,
    strandedness_terms,
    strain_terms,
    mapping_assembly_terms,
    experiment_type_terms,
    stage_terms,
    enhancer_terms,
    gene_terms,
    specimen_type_terms,
    species_terms,
    molecule_type_terms,
    treatment_terms,
    transcription_factor_terms,
    mouse_genetic_background_terms,
    output_type_terms,
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

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'vocab'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    schema = model_root.create_schema(schema_def)


if __name__ == "__main__":
    main()
