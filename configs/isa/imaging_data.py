import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'imaging_data'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('anatomy', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('url', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}', 'md5': 'md5'}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('file_type', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.imaging_data_file_type_fkey.rowName}}}'}}},
    ),
    em.Column.define('byte_count', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('submitted_on', em.builtin_types['timestamptz'],
        annotations={'tag:isrd.isi.edu,2016:immutable': None},
    ),
    em.Column.define('md5', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('file_id', em.builtin_types['int4'],
    ),
    em.Column.define('replicate', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'imaging_data_pkey')],
    ),
    em.Key.define(['dataset', 'RID'],
                   constraint_names=[('isa', 'imaging_data_dataset_RID_key')],
    ),
    em.Key.define(['url'],
                   constraint_names=[('isa', 'imaging_data_url_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'Beta_Cell', 'Dataset', ['RID'],
            constraint_names=[('isa', 'imaging_data_dataset_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns = \
{'compact': [['isa', 'imaging_data_pkey'], 'replicate_fkey', 'url', 'file_type',
             'byte_count', 'md5', 'submitted_on'],
 'detailed': [['isa', 'imaging_data_pkey'],
              ['isa', 'imaging_data_dataset_fkey'],
              ['isa', 'imaging_data_replicate_fkey'],
              ['isa', 'imaging_data_device_fkey'], 'filename',
              ['isa', 'imaging_data_file_type_fkey'], 'byte_count', 'md5',
              'submitted_on'],
 'entry': ['RID', ['isa', 'imaging_data_replicate_fkey'],
           ['isa', 'imaging_data_anatomy_fkey'],
           ['isa', 'imaging_data_device_fkey'],
           ['isa', 'imaging_data_equipment_model_fkey'], 'description', 'url',
           'filename', ['isa', 'imaging_data_file_type_fkey'], 'byte_count',
           'md5', 'submitted_on'],
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

visible_foreign_keys = \
{'detailed': [['isa', 'thumbnail_thumbnail_of_fkey'],
              ['isa', 'mesh_data_derived_from_fkey']],
 'entry': [['isa', 'thumbnail_thumbnail_of_fkey'],
           ['isa', 'mesh_data_derived_from_fkey']]}

table_comment = \
None

table_display = \
{'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:table-alternatives":
{'compact': ['isa', 'imaging_compact'],
 'compact/brief': ['isa', 'imaging_compact']}
,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}

column_annotations = \
{'file_type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.imaging_data_file_type_fkey.rowName}}}'}}},
 'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
 'submitted_on': {'tag:isrd.isi.edu,2016:immutable': None},
 'url': {'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}'}}}



table_def = em.Table.define(table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system = True
)