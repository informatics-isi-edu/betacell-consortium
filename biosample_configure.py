from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

server = 'pbcconsortium.isrd.isi.edu'
schema_name = 'isa'
table_name = 'biosample'

visible_columns = {
    'filter':
        {'and': [{'source': [{'outbound': ['isa',
                                           'biosample_species_fkey']},
                             'term'],
                  'open': True,
                  'markdown_name': 'Species',
                  'entity': True},
                 {'source': 'local_identifier',
                  'open': False,
                  'markdown_name': 'Local Identifier',
                  'entity': True},
                 {'source': 'capillary_number', 'entity': True},
                 {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                             {'outbound': ['isa', 'specimen_cell_line_fkey']},
                             'name'],
                  'markdown_name': 'Cell Line'},
                 {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                             {'outbound': ['isa', 'specimen_species_fkey']},
                             'name'],
                  'markdown_name': 'Species'},
                 {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                             {'outbound': ['isa', 'specimen_gender_fkey']},
                             'name'],
                  'markdown_name': 'Gender'},
                 {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                             {'outbound': ['isa', 'specimen_anatomy_fkey']},
                             'name'],
                  'markdown_name': 'Anatomy'},
                 ]},
    'entry':
        [['isa', 'biosample_dataset_fkey'],
         'local_identifier',
         ['isa', 'biosample_specimen_hack_fkey'],
         ['isa', 'biosample_specimen_type_fkey'],
         'capillary_number',
         'sample_position',
         'collection_date'],
    'detailed':
        [['isa', 'biosample_pkey'],
         ['isa', 'biosample_dataset_fkey'],
         'local_identifier',
         'summary',
         ['isa', 'biosample_species_fkey'],
         ['isa', 'biosample_specimen_hack_fkey'],
         {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                     {'outbound': ['isa', 'specimen_cell_line_fkey']},
                     'name'],
          'markdown_name': 'Cell Line'},
         {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                     {'outbound': ['isa', 'specimen_species_fkey']},
                     'name'],
          'markdown_name': 'Species'},
         {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                     {'outbound': ['isa', 'specimen_gender_fkey']},
                     'name'],
          'markdown_name': 'Gender'},
         {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                     {'outbound': ['isa', 'specimen_anatomy_fkey']},
                     'name'],
          'markdown_name': 'Anatomy'},
         [['isa', 'biosample_specimen_hack_fkey'], ['isa', 'specimen_species_fkey']],
         ['isa', 'biosample_specimen_type_fkey'],
         'capillary_number',
         'sample_position',
         'collection_date'],
    'compact':
        [['isa', 'biosample_pkey'],
         'local_identifier',
         {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                     {'outbound': ['isa', 'specimen_cell_line_fkey']},
                     'name'],
          'markdown_name': 'Cell Line'},
         {'source': [{'outbound': ['isa', 'biosample_specimen_hack_fkey']},
                     {'outbound': ['isa', 'specimen_gender_fkey']},
                     'name'],
          'markdown_name': 'Gender'},
         'species',
         'capillary_number',
         'sample_position']}

visible_foreign_keys = {'detailed': [['isa', 'replicate_biosample_fkey']],
                        'entry': [['isa', 'replicate_biosample_fkey']]}

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
