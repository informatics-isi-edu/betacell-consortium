import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cvterm_dbxref'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('cvterm_dbxref_id', em.builtin_types['serial8'],
        nullok=False,
    ),
    em.Column.define('cvterm', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('alternate_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('is_for_definition', em.builtin_types['boolean'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'cvterm_dbxref_RID_key')],
    ),
    em.Key.define(['cvterm_dbxref_id'],
                   constraint_names=[('data_commons', 'cvterm_dbxref_pkey')],
    ),
    em.Key.define(['cvterm', 'alternate_dbxref'],
                   constraint_names=[('data_commons', 'cvterm_dbxref_cvterm_alternate_dbxref_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['cvterm'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvterm_dbxref_cvterm_fkey')],
    ),
    em.ForeignKey.define(['alternate_dbxref'],
            'data_commons', 'dbxref', ['name'],
            constraint_names=[('data_commons', 'cvterm_dbxref_alternate_dbxref_fkey')],
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


table_def = em.Table.define('cvterm_dbxref',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
