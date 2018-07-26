import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'person'
schema_name = 'common'

column_defs = [
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('first_name', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('middle_name', em.builtin_types['text'],
    ),
    em.Column.define('last_name', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('email', em.builtin_types['text'],
    ),
    em.Column.define('degrees', em.builtin_types['json'],
    ),
    em.Column.define('affiliation', em.builtin_types['text'],
    ),
    em.Column.define('website', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['name'],
                   constraint_names=[('common', 'person_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('common', 'person_RID_key')],
    ),
]


fkey_defs = [
]


visible_columns=\
{'compact': ['name', 'email', 'affiliation'],
 'detailed': ['name', 'email', 'affiliation']}

visible_foreign_keys={}
table_display=\
{'*': {'row_order': [{'column': 'last_name', 'descending': False}]},
 'row_name': {'row_markdown_pattern': '{{{first_name}}} {{{last_name}}}'}}

table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
}
column_comment = \
{'RCB': None,
 'RCT': None,
 'RID': None,
 'RMB': None,
 'RMT': None,
 'affiliation': None,
 'degrees': None,
 'email': None,
 'first_name': None,
 'last_name': None,
 'middle_name': None,
 'name': None,
 'website': None}



table_def = em.Table.define('person',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='Standard definition for a person in catalog',
    provide_system = True
)
