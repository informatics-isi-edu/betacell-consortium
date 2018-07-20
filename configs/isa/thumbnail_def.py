import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'thumbnail'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('url', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/thumbnail/{{{_dataset}}}/{{{md5}}}/{{#encode}}{{{filename}}}{{/encode}}', 'md5': 'md5'}, 'tag:misd.isi.edu,2015:display': {'name': 'Image'}, 'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[![{{{filename}}}]({{{url}}}){height=330}]({{{url}}}){target=_blank}'}, 'detailed': {'markdown_pattern': '[![{{{filename}}}]({{{url}}}){height=330}]({{{url}}}){target=_blank}'}}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('caption', em.builtin_types['markdown'],
    ),
    em.Column.define('byte_count', em.builtin_types['int4'],
    ),
    em.Column.define('submitted_on', em.builtin_types['timestamptz'],
    ),
    em.Column.define('md5', em.builtin_types['text'],
    ),
    em.Column.define('thumbnail_of', em.builtin_types['text'],
    ),
    em.Column.define('show_in_dataset', em.builtin_types['boolean'],
        nullok=False,
    ),
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'thumbnail_RID_key')],
    ),
    em.Key.define(['url'],
                   constraint_names=[('isa', 'thumbnail_url_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('isa', 'thumbnail_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'thumbnail_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['thumbnail_of'],
            'isa', 'imaging_data', ['RID'],
            constraint_names=[('isa', 'thumbnail_thumbnail_of_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns=\
{'compact': ['url', 'filename', 'caption'],
 'detailed': ['url', 'filename', 'caption', ['isa', 'thumbnail_dataset_fkey'],
              ['isa', 'thumbnail_thumbnail_of_fkey'], 'byte_count', 'md5',
              'submitted_on']}

visible_foreign_keys={}
table_display=\
{'compact/brief': {'row_markdown_pattern': '{{#_show_in_dataset}}:::image '
                                           '[{{#caption}}{{{caption}}}{{/caption}}]({{{url}}}){height=330 '
                                           'link="{{{url}}}"} \n'
                                           ':::{{/_show_in_dataset}}'},
 'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_acls={}
table_acl_bindings=\
{'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'thumbnail_dataset_fkey']},
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
                                                        'thumbnail_dataset_fkey']},
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
{'url': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[![{{{filename}}}]({{{url}}}){height=330}]({{{url}}}){target=_blank}'},
                                                  'detailed': {'markdown_pattern': '[![{{{filename}}}]({{{url}}}){height=330}]({{{url}}}){target=_blank}'}},
         'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/thumbnail/{{{_dataset}}}/{{{md5}}}/{{#encode}}{{{filename}}}{{/encode}}'},
         'tag:misd.isi.edu,2015:display': {'name': 'Image'}}}



table_def = em.Table.define('thumbnail',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
