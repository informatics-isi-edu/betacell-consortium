import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'dbxref'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('db', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('accession', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('version', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('description', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['db', 'version', 'accession'],
                   constraint_names=[('data_commons', 'dbxref_db_accession_version_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'dbxref_RID_key')],
    ),
    em.Key.define(['name'],
                   constraint_names=[('data_commons', 'dbxref_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['db'],
            'data_commons', 'db', ['name'],
            constraint_names=[('data_commons', 'dbxref_db_fkey')],
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


table_def = em.Table.define('dbxref',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
