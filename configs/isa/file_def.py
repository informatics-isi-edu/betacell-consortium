import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'file'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('url', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/data/{{{dataset}}}/{{#encode}}{{{filename}}}{{/encode}}', 'md5': 'md5'}, 'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('byte_count', em.builtin_types['int8'],
    ),
    em.Column.define('submitted_on', em.builtin_types['timestamptz'],
    ),
    em.Column.define('md5', em.builtin_types['text'],
    ),
    em.Column.define('legacy_file_id', em.builtin_types['int4'],
    ),
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['legacy_file_id'],
                   constraint_names=[('isa', 'file_legacy_file_id_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'file_RID_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('isa', 'file_pkey')],
    ),
    em.Key.define(['url'],
                   constraint_names=[('isa', 'file_url_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['accession'],
            constraint_names=[('isa', 'file_dataset_fkey')],
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
]


visible_columns=\
{'compact': [['isa', 'file_RID_key'], 'url', 'byte_count', 'md5',
             'description'],
 'detailed': ['filename', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'],
              ['isa', 'file_dataset_fkey'], 'submitted_on', 'description'],
 'entry': ['url', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'],
           ['isa', 'file_dataset_fkey'], 'submitted_on', 'description'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Dataset',
                     'open': False,
                     'source': [{'outbound': ['isa', 'file_dataset_fkey']},
                                'accession']}]}}

visible_foreign_keys={}
table_display=\
{'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_acls={}
table_acl_bindings=\
{'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'file_dataset_fkey']},
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
                                                        'file_dataset_fkey']},
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
    "tag:misd.isi.edu,2015:display":
{'name': 'Supplementary Files'}
,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:table-alternatives":
{'compact': ['isa', 'file_compact'], 'compact/brief': ['isa', 'file_compact']}
,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
}
column_annotations = \
{'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
 'url': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                  'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}},
         'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{dataset}}}/{{#encode}}{{{filename}}}{{/encode}}'}}}



table_def = em.Table.define('file',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
