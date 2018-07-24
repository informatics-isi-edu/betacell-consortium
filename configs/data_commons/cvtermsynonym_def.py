import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cvtermsynonym'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('cvtermsynonym_id', em.builtin_types['serial8'],
        nullok=False,
    ),
    em.Column.define('dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('synonym', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('synonym_type', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['dbxref', 'synonym'],
                   constraint_names=[('data_commons', 'cvtermsynonym_dbxref_synonym_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'cvtermsynonym_RID_key')],
    ),
    em.Key.define(['cvtermsynonym_id'],
                   constraint_names=[('data_commons', 'cvtermsynonym_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvtermsynonym_dbxref_fkey')],
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


table_def = em.Table.define('cvtermsynonym',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
