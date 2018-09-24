import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'relationship_types'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('cvterm_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('is_reflexive', em.builtin_types['boolean'],
        nullok=False,
    ),
    em.Column.define('is_transitive', em.builtin_types['boolean'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'relationship_types_RID_key')],
    ),
    em.Key.define(['cvterm_dbxref'],
                   constraint_names=[('data_commons', 'relationship_types_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['cvterm_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'relationship_types_cvterm_dbxref_fkey')],
        on_delete='CASCADE',
    ),
]


visible_columns = {}
visible_foreign_keys = {}
table_comment = \
None

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}
column_annotations = \
{}



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
