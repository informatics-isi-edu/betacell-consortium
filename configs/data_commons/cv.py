import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cv'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('definition', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'cv_RID_key')],
    ),
    em.Key.define(['name'],
                   constraint_names=[('data_commons', 'cv_pkey')],
    ),
]


fkey_defs = [
]


visible_columns = {}
visible_foreign_keys = {}
table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}


table_def = em.Table.define('cv',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
