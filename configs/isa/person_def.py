import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'person'
schema_name = 'isa'

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
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'person_RID_key')],
    ),
    em.Key.define(['name'],
                   constraint_names=[('isa', 'person_pkey')],
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


table_def = em.Table.define('person',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='domain',
    provide_system = True
)
