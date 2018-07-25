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
    em.ForeignKey.define(['person'],
            'isa', 'person', ['RID'],
            constraint_names=[('isa', 'project_investigator_person_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['project_id'],
            'isa', 'project', ['id'],
            constraint_names=[('isa', 'project_investigator_project_id_fkey')],
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
]


visible_columns={}
visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings=\
{'project_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'project_investigator_project_id_fkey']},
                                             {'outbound': ['isa',
                                                           'project_groups_fkey']},
                                             'groups'],
                              'projection_type': 'acl',
                              'scope_acl': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                            'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                              'types': ['update', 'delete']}}

table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}


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
