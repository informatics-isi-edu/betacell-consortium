import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'previews'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset_id', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('preview_uri', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': ':::iframe [**{{{filename}}}** -- click the **load** button below to view the downsampled preview](/_viewer/xtk/view_on_load.html?url={{{preview_uri}}}){width=800 height=600 .iframe} \n:::'}}},
    ),
    em.Column.define('uri', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('byte_count', em.builtin_types['int8'],
    ),
    em.Column.define('md5', em.builtin_types['text'],
    ),
    em.Column.define('file_type', em.builtin_types['text'],
    ),
    em.Column.define('submitted_on', em.builtin_types['date'],
    ),
]


key_defs = [
    em.Key.define(['dataset_id', 'preview_uri'],
                   constraint_names=[('isa', 'previews_dataset_id_preview_uri_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'previews_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset_id'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'previews_dataset_id_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['file_type'],
            'vocab', 'file_format_terms', ['dbxref'],
            constraint_names=[('isa', 'previews_file_type_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'File Type'}},
    ),
]


visible_columns={}
visible_foreign_keys={}
table_display=\
{'compact': {'row_markdown_pattern': ':::iframe [**{{{filename}}}** -- click '
                                     'the **load** button below to view the '
                                     'downsampled '
                                     'preview](/_viewer/xtk/view_on_load.html?url={{{preview_uri}}}){width=800 '
                                     'height=600 .iframe} \n'
                                     ':::'}}

table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:misd.isi.edu,2015:display":
{'name': 'Downsampled Image Previews'}
,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
}
column_annotations = \
{'preview_uri': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': ':::iframe '
                                                                                          '[**{{{filename}}}** '
                                                                                          '-- '
                                                                                          'click '
                                                                                          'the '
                                                                                          '**load** '
                                                                                          'button '
                                                                                          'below '
                                                                                          'to '
                                                                                          'view '
                                                                                          'the '
                                                                                          'downsampled '
                                                                                          'preview](/_viewer/xtk/view_on_load.html?url={{{preview_uri}}}){width=800 '
                                                                                          'height=600 '
                                                                                          '.iframe} \n'
                                                                                          ':::'}}}}



table_def = em.Table.define('previews',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
