import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'domain_registry'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('term_schema', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('term_table', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('rel_type_schema', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('rel_type_table', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('path_schema', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('path_table', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('data_commons', 'domain_registry_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'domain_registry_RID_key')],
    ),
    em.Key.define(['term_schema', 'term_table'],
                   constraint_names=[('data_commons', 'domain_registry_term_schema_term_table_key')],
    ),
]


fkey_defs = [
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
