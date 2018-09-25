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
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'file_RID_key')],
    ),
    em.Key.define(['url'],
                   constraint_names=[('isa', 'file_url_key')],
    ),
    em.Key.define(['legacy_file_id'],
                   constraint_names=[('isa', 'file_legacy_file_id_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('isa', 'file_pkey')],
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


visible_columns = \
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

visible_foreign_keys = {}
table_comment = \
None

table_display = \
{'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:misd.isi.edu,2015:display":
{'name': 'Supplementary Files'}
,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:table-alternatives":
{'compact': ['isa', 'file_compact'], 'compact/brief': ['isa', 'file_compact']}
,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}

column_annotations = \
{'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
 'url': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                  'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}},
         'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{dataset}}}/{{#encode}}{{{filename}}}{{/encode}}'}}}



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
