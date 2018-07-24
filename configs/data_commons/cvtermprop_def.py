import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cvtermprop'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('cvtermprop_id', em.builtin_types['serial8'],
        nullok=False,
    ),
    em.Column.define('cvterm_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('type_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('value', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('rank', em.builtin_types['int4'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'cvtermprop_RID_key')],
    ),
    em.Key.define(['cvterm_dbxref', 'rank', 'value', 'type_dbxref'],
                   constraint_names=[('data_commons', 'cvtermprop_cvterm_dbxref_type_dbxref_value_rank_key')],
    ),
    em.Key.define(['cvtermprop_id'],
                   constraint_names=[('data_commons', 'cvtermprop_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['cvterm_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvtermprop_cvterm_dbxref_fkey')],
    ),
    em.ForeignKey.define(['type_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvtermprop_type_dbxref_fkey')],
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


table_def = em.Table.define('cvtermprop',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
