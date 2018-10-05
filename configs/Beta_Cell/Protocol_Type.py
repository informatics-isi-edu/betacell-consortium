import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Protocol_Type'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Protocol_Type', em.builtin_types['text'],
        nullok=False,
        comment='Type of entity this protocol describes.',
    ),
]


key_defs = [
    em.Key.define(['Protocol_Type'],
                   constraint_names=[('Beta_Cell', 'Protocol_Type_names_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'Protocol_Type_RIDkey1')],
    ),
]


fkey_defs = [
]


visible_columns = \
{'*': ['RID', 'Protocol_Type']}

visible_foreign_keys = {}
table_comment = \
'Table containing names of Beta Cell protocols'

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Protocol_Type': 'Type of entity this protocol describes.'}

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
