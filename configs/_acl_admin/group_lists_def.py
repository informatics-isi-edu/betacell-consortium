import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'group_lists'
schema_name = '_acl_admin'

column_defs = [
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
        comment='Name of grouplist, used in foreign keys. This table is maintained by the rbk_acls program and should not be updated by hand.',
    ),
    em.Column.define('groups', em.builtin_types['text[]'],
        comment='List of groups. This table is maintained by the rbk_acls program and should not be updated by hand.',
    ),
]


key_defs = [
    em.Key.define(['name'],
                   constraint_names=[('_acl_admin', 'group_lists_name_u')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('_acl_admin', 'group_lists_RID_key')],
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
    "tag:isrd.isi.edu,2016:generated":
None
,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp',
 'groups': 'List of groups. This table is maintained by the rbk_acls program '
           'and should not be updated by hand.',
 'name': 'Name of grouplist, used in foreign keys. This table is maintained by '
         'the rbk_acls program and should not be updated by hand.'}



table_def = em.Table.define('group_lists',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='Named lists of groups used in ACLs. Maintained by the rbk_acls program. Do not update this table manually.',
    provide_system = True
)
