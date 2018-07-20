import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'tracks'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('name', em.builtin_types['text'],
    ),
    em.Column.define('format', em.builtin_types['text'],
    ),
    em.Column.define('software', em.builtin_types['text'],
    ),
    em.Column.define('version', em.builtin_types['text'],
    ),
    em.Column.define('settings', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('isa', 'tracks_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'tracks_RID_key')],
    ),
]


fkey_defs = [
]


visible_columns=\
{'compact': ['name', 'format', 'software', 'version', 'settings'],
 'detailed': ['name', 'format', 'software', 'version', 'settings']}

visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}


table_def = em.Table.define('tracks',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
