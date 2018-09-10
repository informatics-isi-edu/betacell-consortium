import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'project_investigator'
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
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'project_investigator_RID_key')],
    ),
    em.Key.define(['project_id', 'person'],
                   constraint_names=[('isa', 'project_investigator_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['project_id'],
            'isa', 'project', ['id'],
            constraint_names=[('isa', 'project_investigator_project_id_fkey')],
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(['person'],
            'isa', 'person', ['RID'],
            constraint_names=[('isa', 'project_investigator_person_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
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
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}



table_def = em.Table.define('project_investigator',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
