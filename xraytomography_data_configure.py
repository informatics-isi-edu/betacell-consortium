from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

server = 'pbcconsortium.isrd.isi.edu'

schema_name = 'isa'
table_name = 'xraytomography_data'

visible_columns = {
    'filter':
        {'and': [{'source': 'filename',
                  'open': False,
                  'markdown_name': 'File Name',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'xray_tomography_data_replicate_fkey']}, 'RID'],
                  'open': True,
                  'markdown_name': 'Replicate',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'xray_tomography_data_anatomy_fkey']}, 'id'],
                  'open': True,
                  'markdown_name': 'Anatomy',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'xray_tomography_data_device_fkey']}, 'id'],
                  'open': True,
                  'markdown_name': 'Imaging Device',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'xray_tomography_data_equipment_model_fkey']},
                             'id'],
                  'open': True,
                  'markdown_name': 'Equipment Model',
                  'entity': True},
                 {'source': [{'outbound': ['isa', 'xray_tomography_data_file_type_fkey']}, 'id'],
                  'open': True,
                  'markdown_name': 'File Type',
                  'entity': True},
                 {'source': 'submitted_on',
                  'open': False,
                  'markdown_name': 'Submitted On',
                  'entity': True}]},
    'entry':
        ['RID',
         ['isa', 'xray_tomography_data_replicate_fkey'],
         ['isa', 'xray_tomography_data_anatomy_fkey'],
         ['isa', 'xray_tomography_data_device_fkey'],
         ['isa', 'xray_tomography_data_equipment_model_fkey'],
         'description',
         'url',
         'filename'
         ['isa', 'xray_tomography_data_file_type_fkey'],
         'byte_count',
         'md5',
         'submitted_on'],
    'detailed':
        [['isa', 'xray_tomography_data_pkey'],
         ['isa', 'xray_tomography_data_dataset_fkey'],
         ['isa', 'xray_tomography_data_replicate_fkey'],
         ['isa', 'xray_tomography_data_device_fkey'],
         'filename',
         ['isa', 'xray_tomography_data_file_type_fkey'],
         'byte_count',
         'md5',
         'submitted_on'],
    'compact':
        [['isa', 'xray_tomography_data_pkey'],
         'replicate_fkey',
         'url',
         ['isa', 'xray_tomography_data_file_type_fkey'],
         'byte_count',
         'md5',
         'submitted_on']}

visible_foreign_keys = {
    'detailed':
        [['isa', 'thumbnail_thumbnail_of_fkey'],
         ['isa', 'mesh_data_derived_from_fkey']],
    'entry':
        [['isa', 'thumbnail_thumbnail_of_fkey'],
         ['isa', 'mesh_data_derived_from_fkey']]
}

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
