import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'BellCellStatus'
schema_name = 'isa'

column_defs = [
    em.Column.define('ID', em.builtin_types['int8'],
    ),
    em.Column.define('Status', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'BellCellStatus_RIDkey1')],
    ),
]


fkey_defs = [
]


visible_columns = {}
visible_foreign_keys = {}
table_comment = \
'Request status'

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
