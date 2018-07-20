import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'sequencing_data'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('paired', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.sequencing_data_paired_fkey.rowName}}}'}}},
    ),
    em.Column.define('read', em.builtin_types['int4'],
        comment='Possible values are 1 or 2',
    ),
    em.Column.define('rna_seq_library_yield', em.builtin_types['text'],
    ),
    em.Column.define('library', em.builtin_types['int4'],
    ),
    em.Column.define('url', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}', 'md5': 'md5'}, 'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('file_type', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.sequencing_data_file_type_fkey.rowName}}}'}}},
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
    em.Column.define('replicate', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['url'],
                   constraint_names=[('isa', 'sequencing_data_url_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'sequencing_data_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['replicate', 'dataset'],
            'isa', 'replicate', ['RID', 'dataset'],
            constraint_names=[('isa', 'sequencing_data_replicate_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['library'],
            'isa', 'library', ['id'],
            constraint_names=[('isa', 'sequencing_data_library_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'sequencing_data_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['file_type'],
            'vocab', 'file_format_terms', ['dbxref'],
            constraint_names=[('isa', 'sequencing_data_file_type_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'File Type'}},
    ),
    em.ForeignKey.define(['paired'],
            'vocab', 'paired_end_or_single_read_terms', ['dbxref'],
            constraint_names=[('isa', 'sequencing_data_paired_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Paired'}},
    ),
]


visible_columns=\
{'compact': [['isa', 'sequencing_data_pkey'], 'replicate', 'url', 'file_type',
             'paired', 'read', 'byte_count', 'md5', 'submitted_on'],
 'detailed': [['isa', 'sequencing_data_pkey'],
              ['isa', 'sequencing_data_replicate_fkey'], 'read',
              ['isa', 'sequencing_data_paired_fkey'], 'filename',
              ['isa', 'sequencing_data_type_fkey'], 'byte_count', 'md5',
              ['isa', 'sequencing_data_library_fkey'], 'submitted_on'],
 'entry': ['RID', ['isa', 'sequencing_data_replicate_fkey'], 'read',
           ['isa', 'sequencing_data_paired_fkey'], 'url', 'filename',
           ['isa', 'sequencing_data_type_fkey'], 'byte_count', 'md5',
           ['isa', 'sequencing_data_library_fkey'], 'submitted_on'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Replicate',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'sequencing_data_replicate_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Read',
                     'open': False,
                     'source': 'read'},
                    {'entity': True,
                     'markdown_name': 'File Name',
                     'open': False,
                     'source': 'filename'},
                    {'entity': True,
                     'markdown_name': 'Type',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'sequencing_data_type_fkey']},
                                'id']}]}}

visible_foreign_keys={}
table_display=\
{'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_acls={}
table_acl_bindings=\
{'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'sequencing_data_dataset_fkey']},
                                             {'outbound': ['isa',
                                                           'dataset_project_fkey']},
                                             {'outbound': ['isa',
                                                           'project_groups_fkey']},
                                             'groups'],
                              'projection_type': 'acl',
                              'scope_acl': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                            'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                              'types': ['update', 'delete']},
 'released_status_guard': {'projection': [{'outbound': ['isa',
                                                        'sequencing_data_dataset_fkey']},
                                          {'or': [{'filter': 'status',
                                                   'operand': 'commons:228:',
                                                   'operator': '='},
                                                  {'filter': 'status',
                                                   'operand': 'commons:226:',
                                                   'operator': '='}]},
                                          'RID'],
                           'projection_type': 'nonnull',
                           'scope_acl': ['*'],
                           'types': ['select']}}

table_annotations = {
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
}
column_annotations = \
{'file_type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.sequencing_data_file_type_fkey.rowName}}}'}}},
 'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
 'paired': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.sequencing_data_paired_fkey.rowName}}}'}}},
 'submitted_on': {'tag:isrd.isi.edu,2016:immutable': None},
 'url': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                  'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}},
         'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}'}}}



table_def = em.Table.define('sequencing_data',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
