import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'file_extension'
schema_name = 'vocab'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('term', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('file_format', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('vocab', 'file_extension_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('vocab', 'file_extension_rid_key')],
    ),
    em.Key.define(['term'],
                   constraint_names=[('vocab', 'file_extension_term_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['file_format'],
            'vocab', 'file_format_terms', ['RID'],
            constraint_names=[('vocab', 'file_extension_file_format_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'File Format'}},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns={}
visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}


table_def = em.Table.define('file_extension',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
