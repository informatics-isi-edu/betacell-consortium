import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'imaging_data'
schema_name = 'isa'

column_annotations = {
    'RCB': {},
    'RCT': {},
    'RID': {},
    'RMB': {},
    'RMT': {},
    'file_type': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '{{{$fkeys.isa.imaging_data_file_type_fkey.rowName}}}'}}},
    'filename': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    'submitted_on': {
        'tag:isrd.isi.edu,2016:immutable': None},
    'url': {
        'tag:isrd.isi.edu,2017:asset': {
            'byte_count_column': 'byte_count',
            'filename_column': 'filename',
            'md5': 'md5',
            'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}'}}}

column_comment = {'RCB': 'System-generated row created by user provenance.',
                  'RCT': 'System-generated row creation timestamp.',
                  'RID': 'System-generated unique row ID.',
                  'RMB': 'System-generated row modified by user provenance.',
                  'RMT': 'System-generated row modification timestamp'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False, comment=column_comment['RID'],),
               em.Column.define('dataset', em.builtin_types['text'], nullok=False,),
               em.Column.define('anatomy', em.builtin_types['text'],),
               em.Column.define('description', em.builtin_types['markdown'],),
               em.Column.define('url', em.builtin_types['text'], nullok=False, annotations=column_annotations['url'],),
               em.Column.define('filename', em.builtin_types['text'], nullok=False, annotations=column_annotations['filename'],),
               em.Column.define('file_type', em.builtin_types['text'], nullok=False, annotations=column_annotations['file_type'],),
               em.Column.define('byte_count', em.builtin_types['int8'], nullok=False,),
               em.Column.define('submitted_on', em.builtin_types['timestamptz'], annotations=column_annotations['submitted_on'],),
               em.Column.define('md5', em.builtin_types['text'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'], comment=column_comment['RCB'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'], comment=column_comment['RMB'],),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False, comment=column_comment['RCT'],),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False, comment=column_comment['RMT'],),
               em.Column.define('file_id', em.builtin_types['int4'],),
               em.Column.define('replicate', em.builtin_types['text'],),
               ]

visible_columns = {'compact': [['isa', 'imaging_data_pkey'],
                               'replicate_fkey',
                               'url',
                               'file_type',
                               'byte_count',
                               'md5',
                               'submitted_on'],
                   'detailed': [['isa', 'imaging_data_pkey'],
                                ['isa', 'imaging_data_dataset_fkey'],
                                ['isa', 'imaging_data_replicate_fkey'],
                                ['isa', 'imaging_data_device_fkey'],
                                'filename',
                                ['isa', 'imaging_data_file_type_fkey'],
                                'byte_count',
                                'md5',
                                'submitted_on'],
                   'entry': ['RID',
                             ['isa', 'imaging_data_replicate_fkey'],
                             ['isa', 'imaging_data_anatomy_fkey'],
                             ['isa', 'imaging_data_device_fkey'],
                             ['isa', 'imaging_data_equipment_model_fkey'],
                             'description',
                             'url',
                             'filename',
                             ['isa', 'imaging_data_file_type_fkey'],
                             'byte_count',
                             'md5',
                             'submitted_on'],
                   'filter': {'and': [{'entity': True,
                                       'markdown_name': 'File Name',
                                       'open': False,
                                       'source': 'filename'},
                                      {'entity': True,
                                       'markdown_name': 'Replicate',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'imaging_data_replicate_fkey']},
                                                  'RID']},
                                      {'entity': True,
                                       'markdown_name': 'Anatomy',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'imaging_data_anatomy_fkey']},
                                                  'id']},
                                      {'entity': True,
                                       'markdown_name': 'Imaging Device',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'imaging_data_device_fkey']},
                                                  'id']},
                                      {'entity': True,
                                       'markdown_name': 'Equipment Model',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'imaging_data_equipment_model_fkey']},
                                                  'id']},
                                      {'entity': True,
                                       'markdown_name': 'File Type',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'imaging_data_file_type_fkey']},
                                                  'id']},
                                      {'entity': True,
                                       'markdown_name': 'Submitted On',
                                       'open': False,
                                       'source': 'submitted_on'}]}}

visible_foreign_keys = {'detailed': [['isa', 'thumbnail_thumbnail_of_fkey'],
                                     ['isa', 'mesh_data_derived_from_fkey']],
                        'entry': [['isa', 'thumbnail_thumbnail_of_fkey'],
                                  ['isa', 'mesh_data_derived_from_fkey']]}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_alternatives = {'compact': ['isa', 'imaging_compact'],
                      'compact/brief': ['isa', 'imaging_compact']}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
    'tag:isrd.isi.edu,2016:table-alternatives': table_alternatives,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['dataset', 'RID'],
                  constraint_names=[('isa', 'imaging_data_dataset_RID_key')],
                  ),
    em.Key.define(['url'],
                  constraint_names=[('isa', 'imaging_data_url_key')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('isa', 'imaging_data_pkey')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['dataset'],
                         'Beta_Cell', 'Dataset', ['RID'],
                         constraint_names=[
                             ('isa', 'imaging_data_dataset_fkey')],
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
]

table_def = em.Table.define(table_name,
                            column_defs=column_defs,
                            key_defs=key_defs,
                            fkey_defs=fkey_defs,
                            annotations=table_annotations,
                            acls=table_acls,
                            acl_bindings=table_acl_bindings,
                            comment=table_comment,
                            provide_system=True
                            )


def main():
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    update_catalog.update_table(server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
