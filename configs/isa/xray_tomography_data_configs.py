import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
visible_columns = \
{   'compact': [   ['isa', 'xray_tomography_data_pkey'],
                   'replicate_fkey',
                   'url',
                   ['isa', 'xray_tomography_data_file_type_fkey'],
                   'byte_count',
                   'md5',
                   'submitted_on'],
    'detailed': [   ['isa', 'xray_tomography_data_pkey'],
                    ['isa', 'xray_tomography_data_dataset_fkey'],
                    ['isa', 'xray_tomography_data_replicate_fkey'],
                    ['isa', 'xray_tomography_data_device_fkey'],
                    'filename',
                    ['isa', 'xray_tomography_data_file_type_fkey'],
                    'byte_count',
                    'md5',
                    'submitted_on'],
    'entry': [   'RID',
                 ['isa', 'xray_tomography_data_replicate_fkey'],
                 ['isa', 'xray_tomography_data_anatomy_fkey'],
                 ['isa', 'xray_tomography_data_device_fkey'],
                 ['isa', 'xray_tomography_data_equipment_model_fkey'],
                 'description',
                 'url',
                 ['isa', 'xray_tomography_data_file_type_fkey'],
                 'filename',
                 ['isa', 'xray_tomography_data_file_type_fkey'],
                 'byte_count',
                 'md5',
                 'submitted_on'],
    'filter': {   'and': [   {   'entity': True,
                                 'markdown_name': 'File Name',
                                 'open': False,
                                 'source': 'filename'},
                             {   'entity': True,
                                 'markdown_name': 'Replicate',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'xray_tomography_data_replicate_fkey']},
                                               'RID']},
                             {   'entity': True,
                                 'markdown_name': 'Anatomy',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'xray_tomography_data_anatomy_fkey']},
                                               'id']},
                             {   'entity': True,
                                 'markdown_name': 'Imaging Device',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'xray_tomography_data_device_fkey']},
                                               'id']},
                             {   'entity': True,
                                 'markdown_name': 'Equipment Model',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'xray_tomography_data_equipment_model_fkey']},
                                               'id']},
                             {   'entity': True,
                                 'markdown_name': 'File Type',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'xray_tomography_data_file_type_fkey']},
                                               'id']},
                             {   'entity': True,
                                 'markdown_name': 'Submitted On',
                                 'open': False,
                                 'source': 'submitted_on'}]}}
visible_foreign_keys = \
{   'detailed': [   ['isa', 'thumbnail_thumbnail_of_fkey'],
                    ['isa', 'mesh_data_derived_from_fkey']],
    'entry': [   ['isa', 'thumbnail_thumbnail_of_fkey'],
                 ['isa', 'mesh_data_derived_from_fkey']]}
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'xray_tomography_data_pkey'],
                                                                'replicate_fkey',
                                                                'url',
                                                                [   'isa',
                                                                    'xray_tomography_data_file_type_fkey'],
                                                                'byte_count',
                                                                'md5',
                                                                'submitted_on'],
                                                 'detailed': [   [   'isa',
                                                                     'xray_tomography_data_pkey'],
                                                                 [   'isa',
                                                                     'xray_tomography_data_dataset_fkey'],
                                                                 [   'isa',
                                                                     'xray_tomography_data_replicate_fkey'],
                                                                 [   'isa',
                                                                     'xray_tomography_data_device_fkey'],
                                                                 'filename',
                                                                 [   'isa',
                                                                     'xray_tomography_data_file_type_fkey'],
                                                                 'byte_count',
                                                                 'md5',
                                                                 'submitted_on'],
                                                 'entry': [   'RID',
                                                              [   'isa',
                                                                  'xray_tomography_data_replicate_fkey'],
                                                              [   'isa',
                                                                  'xray_tomography_data_anatomy_fkey'],
                                                              [   'isa',
                                                                  'xray_tomography_data_device_fkey'],
                                                              [   'isa',
                                                                  'xray_tomography_data_equipment_model_fkey'],
                                                              'description',
                                                              'url',
                                                              [   'isa',
                                                                  'xray_tomography_data_file_type_fkey'],
                                                              'filename',
                                                              [   'isa',
                                                                  'xray_tomography_data_file_type_fkey'],
                                                              'byte_count',
                                                              'md5',
                                                              'submitted_on'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'markdown_name': 'File '
                                                                                               'Name',
                                                                              'open': False,
                                                                              'source': 'filename'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Replicate',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_replicate_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Anatomy',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_anatomy_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Imaging '
                                                                                               'Device',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_device_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Equipment '
                                                                                               'Model',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_equipment_model_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'File '
                                                                                               'Type',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_file_type_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Submitted '
                                                                                               'On',
                                                                              'open': False,
                                                                              'source': 'submitted_on'}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'thumbnail_thumbnail_of_fkey'],
                                                                      [   'isa',
                                                                          'mesh_data_derived_from_fkey']],
                                                      'entry': [   [   'isa',
                                                                       'thumbnail_thumbnail_of_fkey'],
                                                                   [   'isa',
                                                                       'mesh_data_derived_from_fkey']]}}
column_annotations = \
{   'file_type': {   'tag:isrd.isi.edu,2016:column-display': {   'compact': {   'markdown_pattern': '{{{$fkeys.isa.xray_tomography_data_file_type_fkey.rowName}}}'}}},
    'filename': {   'tag:isrd.isi.edu,2016:column-display': {   'compact': {   'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                                'detailed': {   'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    'url': {   'tag:isrd.isi.edu,2017:asset': {   'byte_count_column': 'byte_count',
                                                  'filename_column': 'filename',
                                                  'md5': 'md5',
                                                  'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}'}}}

def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:xray_tomography_data')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = 'isa'
        table_name = 'xray_tomography_data'

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
        table.annotations['table_display'] = table_display

        table.apply(catalog)


if __name__ == "__main__":
        main()
