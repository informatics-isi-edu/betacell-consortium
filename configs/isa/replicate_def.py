import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'replicate'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('biosample', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('bioreplicate_number', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('technical_replicate_number', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('experiment', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['experiment', 'dataset', 'bioreplicate_number', 'biosample', 'technical_replicate_number'],
                   constraint_names=[('isa', 'replicate_dataset_experiment_biosample_bioreplicate_number__key')],
    ),
    em.Key.define(['dataset', 'RID'],
                   constraint_names=[('isa', 'replicate_RID_dataset_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'replicate_pkey')],
    ),
    em.Key.define(['experiment', 'biosample', 'dataset', 'technical_replicate_number'],
                   constraint_names=[('isa', 'replicate_dataset_experiment_biosample_technical_replicate__key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['biosample'],
            'isa', 'biosample', ['RID'],
            constraint_names=[('isa', 'replicate_biosample_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'domain_filter_pattern': 'dataset={{{_dataset}}}'}},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['dataset', 'experiment'],
            'isa', 'experiment', ['dataset', 'RID'],
            constraint_names=[('isa', 'replicate_experiment_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'replicate_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns=\
{'compact': [['isa', 'replicate_pkey'], ['isa', 'replicate_biosample_fkey'],
             'bioreplicate_number', 'technical_replicate_number'],
 'detailed': [['isa', 'replicate_pkey'], ['isa', 'replicate_experiment_fkey'],
              ['isa', 'replicate_biosample_fkey'], 'bioreplicate_number',
              'technical_replicate_number'],
 'entry': [['isa', 'replicate_experiment_fkey'],
           ['isa', 'replicate_biosample_fkey'], 'bioreplicate_number',
           'technical_replicate_number'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Dataset',
                     'open': True,
                     'source': [{'outbound': ['isa', 'replicate_dataset_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Experiment',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'replicate_experiment_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Biosample',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'replicate_biosample_fkey']},
                                'RID']}]}}

visible_foreign_keys=\
{'detailed': [['isa', 'xray_tomography_data_replicate_fkey'],
              ['viz', 'model_replicate_fkey'],
              ['isa', 'mesh_data_replicate_fkey'],
              ['isa', 'processed_data_replicate_fkey'],
              ['isa', 'imaging_data_replicate_fkey']],
 'entry': [['isa', 'xray_tomography_data_replicate_fkey'],
           ['isa', 'mesh_data_replicate_fkey'],
           ['isa', 'processed_data_replicate_fkey'],
           ['isa', 'imaging_data_replicate_fkey']]}

table_display=\
{'compact': {'row_order': [{'column': 'bioreplicate_number',
                            'descending': False}]},
 'row_name': {'row_markdown_pattern': '{{local_identifier}}'}}

table_acls={}
table_acl_bindings=\
{'curated_status_guard': {'projection': [{'outbound': ['isa',
                                                       'replicate_dataset_fkey']},
                                         {'filter': 'status',
                                          'operand': 'commons:226:',
                                          'operator': '='},
                                         'RID'],
                          'projection_type': 'nonnull',
                          'scope_acl': ['*'],
                          'types': ['select']},
 'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'replicate_dataset_fkey']},
                                             {'outbound': ['isa',
                                                           'dataset_project_fkey']},
                                             {'outbound': ['isa',
                                                           'project_groups_fkey']},
                                             'groups'],
                              'projection_type': 'acl',
                              'scope_acl': ['https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                              'types': ['update', 'delete']}}

table_annotations = {
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "table_display":
{'compact': {'row_order': [{'column': 'bioreplicate_number',
                            'descending': False}]},
 'row_name': {'row_markdown_pattern': '{{local_identifier}}'}}
,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
}


table_def = em.Table.define('replicate',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
