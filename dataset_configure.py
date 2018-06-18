from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

server = 'pbcconsortium.isrd.isi.edu'
schema_name = 'isa'
table_name = 'dataset'

visible_columns = {
    'filter':
        {'and': [{'source': [{'inbound': ['isa',
                                          'dataset_organism_dataset_id_fkey']},
                             {'outbound': ['isa', 'dataset_organism_organism_fkey']},
                             'dbxref'],
                  'open': False,
                  'entity': True},
                 {'source': [
                     {'inbound': ['isa', 'dataset_experiment_type_dataset_id_fkey']},
                     {'outbound': ['isa', 'dataset_experiment_type_experiment_type_fkey']},
                     'dbxref'],
                     'open': False,
                     'entity': True},
                 {'source': [{'inbound': ['isa', 'dataset_data_type_data_type_fkey']},
                             {'outbound': ['isa', 'dataset_data_type_dataset_id_fkey']},
                             'dbxref'],
                  'open': False,
                  'entity': True},
                 {'source': [{'inbound': ['isa', 'dataset_anatomy_dataset_id_fkey']},
                             {'outbound': ['isa', 'dataset_anatomy_anatomy_fkey']},
                             'dbxref'],
                  'open': False,
                  'entity': True},
                 {'source': [{'inbound': ['isa', 'dataset_phenotype_dataset_fkey']},
                             {'outbound': ['isa', 'dataset_phenotype_phenotype_fkey']},
                             'dbxref'],
                  'open': False,
                  'entity': True},
                 {'source': [{'inbound': ['isa', 'publication_dataset_fkey']}, 'pmid'],
                  'open': False,
                  'markdown_name': 'Pubmed ID',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'dataset_project_fkey']},
                             {'inbound': ['isa', 'project_investigator_project_id_fkey']},
                             {'outbound': ['isa', 'project_investigator_person_fkey']},
                             'RID'],
                  'open': False,
                  'markdown_name': 'Project Investigator',
                  'entity': True},
                 {'source': 'accession', 'open': False, 'entity': False},
                 {'source': 'title', 'open': False, 'entity': False},
                 {'source': [{'outbound': ['isa', 'dataset_project_fkey']}, 'id'],
                  'open': False,
                  'entity': True},
                 {'source': 'release_date', 'open': False, 'entity': False},
                 {'source': [{'outbound': ['isa', 'dataset_status_fkey']}, 'name'],
                  'open': False,
                  'entity': True}]},
    'entry': ['accession',
              'title',
              ['isa', 'dataset_project_fkey'],
              'description',
              'study_design',
              'release_date',
              ['isa', 'dataset_status_fkey'],
              'show_in_jbrowse'],
    'detailed': [['isa', 'dataset_RID_key'],
                 'accession',
                 'description',
                 'study_design',
                 ['isa', 'dataset_project_fkey'],
                 ['isa', 'dataset_status_fkey'],
                 'funding',
                 'release_date',
                 'show_in_jbrowse',
                 ['isa', 'publication_dataset_fkey'],
                 ['isa', 'dataset_experiment_type_dataset_id_fkey'],
                 ['isa', 'dataset_data_type_dataset_id_fkey'],
                 ['isa', 'dataset_phenotype_dataset_fkey'],
                 ['isa', 'dataset_organism_dataset_id_fkey'],
                 ['isa', 'dataset_anatomy_dataset_id_fkey'],
                 ['isa', 'dataset_gender_dataset_id_fkey'],
                 ['isa', 'dataset_instrument_dataset_id_fkey']],
    'compact': [['isa', 'dataset_RID_key'],
                ['isa', 'accession_unique'],
                'title',
                ['isa', 'dataset_project_fkey'],
                'status',
                'release_date']
}

visible_foreign_keys = {
    '*': [['isa', 'thumbnail_dataset_fkey'],
          ['viz', 'model_dataset_fkey'],
          ['isa', 'previews_dataset_id_fkey'],
          ['isa', 'experiment_dataset_fkey'],
          ['isa', 'biosample_dataset_fkey'],
          ['isa', 'enhancer_dataset_fkey'],
          ['isa', 'clinical_assay_dataset_fkey'],
          ['isa', 'file_dataset_fkey'],
          ['isa', 'external_reference_id_fkey']]}

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]

if len(visible_columns) > 0:
    for k, v in visible_columns.items():
        table.visible_columns[k] = v

if len(visible_foreign_keys) > 0:
    for k, v in visible_foreign_keys.items():
        table.visible_foreign_keys[k] = v

table.apply(catalog)