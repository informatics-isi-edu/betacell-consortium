import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'icon'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('url', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/thumbnail/icon/{{{md5}}}', 'md5': 'md5'}, 'tag:misd.isi.edu,2015:display': {'name': 'Image'}, 'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[![{{{filename}}}]({{{url}}}){height=330}]({{{url}}}){target=_blank}'}, 'detailed': {'markdown_pattern': '[![{{{filename}}}]({{{url}}}){height=330}]({{{url}}}){target=_blank}'}}},
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
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('isa', 'icon_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'icon_RID_key')],
    ),
    em.Key.define(['url'],
                   constraint_names=[('isa', 'icon_url_key')],
    ),
]


fkey_defs = [
]


visible_columns=\
{'compact': ['url', 'filename', 'caption']}

visible_foreign_keys={}
table_display=\
{'compact/brief': {'row_markdown_pattern': ':::image '
                                           '[{{#caption}}{{{caption}}}{{/caption}}]({{{url}}}){height=330 '
                                           'link="{{{url}}}"} \n'
                                           ':::'},
 'row_name': {'row_markdown_pattern': '![ImageWithSize]({{{url}}}){width=70 '
                                      'height=70}'}}

table_acls={}
table_acl_bindings={}
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
                                         'url_pattern': '/hatrac/commons/thumbnail/icon/{{{md5}}}'},
         'tag:misd.isi.edu,2015:display': {'name': 'Image'}}}



table_def = em.Table.define('icon',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
