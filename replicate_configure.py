from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

server = 'pbcconsortium.isrd.isi.edu'

schema_name = 'isa'
table_name = 'replicate'

visible_columns = {
    'filter':
        {'and': [{'source': [{'outbound': ['isa',
                                           'replicate_dataset_fkey']},
                             'RID'],
                  'open': True,
                  'markdown_name': 'Dataset',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'replicate_experiment_fkey']}, 'RID'],
                  'open': True,
                  'markdown_name': 'Experiment',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'replicate_biosample_fkey']}, 'RID'],
                  'open': True,
                  'markdown_name': 'Biosample',
                  'entity': True}]},
    'entry': [['isa', 'replicate_experiment_fkey'],
              ['isa', 'replicate_biosample_fkey'],
              'bioreplicate_number',
              'technical_replicate_number'],
    'detailed': [['isa', 'replicate_pkey'],
                 ['isa', 'replicate_experiment_fkey'],
                 ['isa', 'replicate_biosample_fkey'],
                 'bioreplicate_number',
                 'technical_replicate_number'],
    'compact': [['isa', 'replicate_pkey'],
                ['isa', 'replicate_biosample_fkey'],
                'bioreplicate_number',
                'technical_replicate_number']}

visible_foreign_keys = {
    'detailed':
        [['isa', 'xray_tomography_data_replicate_fkey'],
         ['isa', 'mesh_data_replicate_fkey'],
         ['isa', 'processed_data_replicate_fkey'],
         ['isa', 'imaging_data_replicate_fkey'], ],
    'entry':
        [['isa', 'xray_tomography_data_replicate_fkey'],
         ['isa', 'mesh_data_replicate_fkey'],
         ['isa', 'processed_data_replicate_fkey'],
         ['isa', 'imaging_data_replicate_fkey'],
         ]}

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
