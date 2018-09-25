import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'processed_tomography_data'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('process', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.processed_tomography_data_process_fkey.rowName}}}'}}},
    ),
    em.Column.define('url', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}', 'md5': 'md5'}, 'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('data_type', em.builtin_types['text'],
    ),
    em.Column.define('file_type', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.processed_tomography_data_file_type_fkey.rowName}}}'}}},
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
    em.Column.define('biosample', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['url'],
                   constraint_names=[('isa', 'processed_tomography_data_url_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'processed_tomography_data_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['process'],
            'isa', 'process', ['RID'],
            constraint_names=[('isa', 'processed_tomography_data_process_fkey')],
    ),
    em.ForeignKey.define(['biosample', 'dataset'],
            'isa', 'biosample', ['RID', 'dataset'],
            constraint_names=[('isa', 'processed_tomography_data_biosample_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'processed_tomography_data_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['file_type'],
            'vocab', 'file_type_terms', ['id'],
            constraint_names=[('isa', 'processed_tomography_data_file_type_fkey')],
    ),
]


visible_columns = \
{'compact': [['isa', 'processed_tomography_data_pkey'], 'biosample', 'url',
             'file_type', 'mapping_assembly', 'pipeline', 'byte_count', 'md5',
             'submitted_on'],
 'detailed': [['isa', 'processed_tomography_data_pkey'],
              ['isa', 'processed_tomography_data_dataset_fkey'],
              ['isa', 'processed_tomography_data_biosample_fkey'],
              ['isa', 'processed_tomography_data_process_fkey'],
              ['isa', 'processed_tomography_data_output_type_fkey'],
              ['isa', 'processed_tomography_data_file_type_fkey'], 'byte_count',
              'md5', 'submitted_on'],
 'entry': ['RID', ['isa', 'processed_tomography_data_biosample_fkey'],
           ['isa', 'processed_tomography_data_process_fkey'],
           ['isa', 'processed_tomography_data_output_type_fkey'],
           ['isa', 'processed_tomography_data_file_type_fkey'], 'url',
           'submitted_on'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'File Name',
                     'open': False,
                     'source': 'filename'},
                    {'entity': True,
                     'markdown_name': 'Biosample',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'processed_tomography_data_biosample_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Type',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'processed_tomography_data_type_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Derived From File',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'processed_tomography_data_derived_from_file_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Pipeline',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'processed_tomography_data_pipeline_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Output Type',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'processed_tomography_data_output_type_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Submitted On',
                     'open': False,
                     'source': 'submitted_on'}]}}

visible_foreign_keys = {}
table_comment = \
'None'

table_display = \
{'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "table_display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_annotations = \
{'file_type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.processed_tomography_data_file_type_fkey.rowName}}}'}}},
 'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
 'process': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.processed_tomography_data_process_fkey.rowName}}}'}}},
 'submitted_on': {'tag:isrd.isi.edu,2016:immutable': None},
 'url': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                  'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}},
         'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}'}}}



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
