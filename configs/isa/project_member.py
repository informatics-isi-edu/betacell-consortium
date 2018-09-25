import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'project_member'
schema_name = 'isa'

column_defs = [
    em.Column.define('project_id', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('person', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['project_id', 'person'],
                   constraint_names=[('isa', 'project_member_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'project_member_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['person'],
            'isa', 'person', ['RID'],
            constraint_names=[('isa', 'project_member_person_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['project_id'],
            'isa', 'project', ['id'],
            constraint_names=[('isa', 'project_member_project_id_fkey')],
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
]


visible_columns = {}
visible_foreign_keys = {}
table_comment = \
'domain'

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}

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
