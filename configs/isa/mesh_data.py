import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'mesh_data'
schema_name = 'isa'

column_defs = [
    em.Column.define('url', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/previews/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}', 'md5': 'md5'}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('byte_count', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('md5', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('derived_from', em.builtin_types['text'],
    ),
    em.Column.define('anatomy', em.builtin_types['text'],
    ),
    em.Column.define('label', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('biosample', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'mesh_data_pkey')],
    ),
    em.Key.define(['url'],
                   constraint_names=[('isa', 'mesh_data_url_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['biosample'],
            'Beta_Cell', 'Biosample', ['RID'],
            constraint_names=[('isa', 'mesh_data_biosample_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['dataset'],
            'Beta_Cell', 'Dataset', ['RID'],
            constraint_names=[('isa', 'mesh_data_dataset_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['derived_from'],
            'Beta_Cell', 'XRay_Tomography_Data', ['RID'],
            constraint_names=[('isa', 'mesh_data_derived_from_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns = \
{'compact': [['isa', 'mesh_data_pkey'], 'biosample',
             ['isa', 'mesh_data_derived_from_fkey'], 'url', 'byte_count',
             'md5'],
 'detailed': [['isa', 'mesh_data_pkey'], ['isa', 'mesh_data_dataset_fkey'],
              ['isa', 'mesh_data_biosample_fkey'],
              ['isa', 'mesh_data_derived_from_fkey'], 'filename', 'byte_count',
              'md5', ['isa', 'mesh_data_anatomy_fkey'], 'label',
              'description'],
 'entry': ['RID', ['isa', 'mesh_data_biosample_fkey'],
           ['isa', 'mesh_data_derived_from_fkey'], 'url', 'filename',
           'byte_count', 'md5', ['isa', 'mesh_data_anatomy_fkey'], 'label',
           'description'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'File Name',
                     'open': False,
                     'source': 'filename'},
                    {'entity': True,
                     'markdown_name': 'Dataset',
                     'open': True,
                     'source': [{'outbound': ['isa', 'mesh_data_dataset_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Biosample',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'mesh_data_biosample_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Derived From File',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'mesh_data_derived_from_fkey']},
                                'RID']}]}}

visible_foreign_keys = {}
table_comment = \
None

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
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}

column_annotations = \
{'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
 'url': {'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/previews/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}'}}}



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