import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'dataset_experiment_type'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset_id', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('experiment_type', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['dataset_id', 'experiment_type'],
                   constraint_names=[('isa', 'dataset_experiment_type_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'dataset_experiment_type_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset_id'],
            'isa', 'dataset', ['id'],
            constraint_names=[('isa', 'dataset_experiment_type_dataset_id_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Datasets'}},
    ),
]


visible_columns={}
visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings=\
{'dataset_tags_edit_guard': {'projection': [{'outbound': ['isa',
                                                          'dataset_experiment_type_dataset_id_fkey']},
                                            {'outbound': ['isa',
                                                          'dataset_project_fkey']},
                                            {'outbound': ['isa',
                                                          'project_groups_fkey']},
                                            'groups'],
                             'projection_type': 'acl',
                             'scope_acl': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                           'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                           'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                             'types': ['update', 'delete']}}

table_annotations = {
    "tag:misd.isi.edu,2015:display":
{'name': 'Experiment_type'}
,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp',
 'dataset_id': None,
 'experiment_type': None}



table_def = em.Table.define('dataset_experiment_type',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
