import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'ermrest_client'
schema_name = 'public'

column_defs = [
    em.Column.define('id', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('display_name', em.builtin_types['text'],
    ),
    em.Column.define('full_name', em.builtin_types['text'],
    ),
    em.Column.define('email', em.builtin_types['text'],
    ),
    em.Column.define('client_obj', em.builtin_types['jsonb'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('public', 'ermrest_client_id_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('public', 'ermrest_client_pkey')],
    ),
]


fkey_defs = [
]


visible_columns={}
visible_foreign_keys={}
table_display={}
table_acls=\
{'delete': [], 'enumerate': [], 'insert': [], 'select': [], 'update': []}

table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}
column_comment = \
{'RCB': None,
 'RCT': None,
 'RID': None,
 'RMB': None,
 'RMT': None,
 'client_obj': None,
 'display_name': None,
 'email': None,
 'full_name': None,
 'id': None}



table_def = em.Table.define('ermrest_client',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
