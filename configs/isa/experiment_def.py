import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'experiment'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('local_identifier', em.builtin_types['text'],
    ),
    em.Column.define('biosample_summary', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:generated': None},
        comment='System-generated column with summary of all related biosamples',
    ),
    em.Column.define('experiment_type', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_experiment_type_fkey.rowName}}}'}}},
    ),
    em.Column.define('control_assay', em.builtin_types['text'],
    ),
    em.Column.define('protocol', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_protocol_fkey.rowName}}}'}}},
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'experiment_pkey')],
    ),
    em.Key.define(['dataset', 'RID'],
                   constraint_names=[('isa', 'experiment_RID_dataset_key')],
    ),
    em.Key.define(['local_identifier', 'dataset'],
                   constraint_names=[('isa', 'experiment_dataset_local_identifier_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['protocol'],
            'isa', 'protocol', ['RID'],
            constraint_names=[('isa', 'experiment_protocol_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'experiment_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['experiment_type'],
            'vocab', 'experiment_type_terms', ['RID'],
            constraint_names=[('isa', 'experiment_experiment_type_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns=\
{'compact': [['isa', 'experiment_pkey'], ['isa', 'experiment_dataset_fkey'],
             ['isa', 'experiment_experiment_type_fkey'],
             {'aggregate': 'array',
              'comment': 'Compound used to treat the cell line for the '
                         'experiment',
              'entity': True,
              'markdown_name': 'Compound',
              'source': [{'outbound': ['isa', 'experiment_protocol_fkey']},
                         {'inbound': ['isa',
                                      'protocol_compound_protocol_fkey']},
                         {'outbound': ['isa',
                                       'protocol_compound_compound_fkey']},
                         'RID']},
             {'aggregate': 'array',
              'comment': 'Concentration of compound applied to cell line in nM',
              'entity': True,
              'markdown_name': 'Concentration',
              'source': [{'outbound': ['isa', 'experiment_protocol_fkey']},
                         {'inbound': ['isa',
                                      'protocol_compound_protocol_fkey']},
                         'compound_concentration']},
             {'aggregate': 'array',
              'comment': 'Measured in minutes',
              'entity': True,
              'source': ['timepoint']}],
 'detailed': [['isa', 'experiment_pkey'], ['isa', 'experiment_dataset_fkey'],
              'local_identifier', ['isa', 'experiment_experiment_type_fkey'],
              'biosample_summary', ['isa', 'experiment_target_of_assay_fkey'],
              ['isa', 'experiment_control_assay_fkey'],
              ['isa', 'experiment_protocol_fkey'],
              {'aggregate': 'array',
               'comment': 'Compound used to treat the cell line for the '
                          'experiment',
               'entity': True,
               'markdown_name': 'Compound',
               'source': [{'outbound': ['isa', 'experiment_protocol_fkey']},
                          {'inbound': ['isa',
                                       'protocol_compound_protocol_fkey']},
                          {'outbound': ['isa',
                                        'protocol_compound_compound_fkey']},
                          'RID']},
              {'aggregate': 'array',
               'comment': 'Concentration of compound applied to cell line in '
                          'nM',
               'entity': True,
               'markdown_name': 'Concentration',
               'source': [{'outbound': ['isa', 'experiment_protocol_fkey']},
                          {'inbound': ['isa',
                                       'protocol_compound_protocol_fkey']},
                          'compound_concentration']},
              {'aggregate': 'array',
               'comment': 'Measured in minutes',
               'entity': True,
               'source': ['timepoint']}],
 'entry': [['isa', 'experiment_dataset_fkey'], 'local_identifier',
           'biosample_summary', ['isa', 'experiment_experiment_type_fkey'],
           ['isa', 'experiment_target_of_assay_fkey'],
           ['isa', 'experiment_control_assay_fkey'],
           ['isa', 'experiment_protocol_fkey']],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Cell Line',
                     'open': True,
                     'source': [{'inbound': ['isa',
                                             'biosample_experiment_fkey']},
                                {'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                {'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'entity': True,
                     'markdown_name': 'Compound',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'experiment_protocol_fkey']},
                                {'inbound': ['isa',
                                             'protocol_compound_protocol_fkey']},
                                {'outbound': ['isa',
                                              'protocol_compound_compound_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Compound Concentration',
                     'open': False,
                     'source': [{'outbound': ['isa',
                                              'experiment_protocol_fkey']},
                                {'inbound': ['isa',
                                             'protocol_compound_protocol_fkey']},
                                'compound_concentration'],
                     'ux_mode': 'choices'},
                    {'entity': True,
                     'markdown_name': 'Timepoint',
                     'open': False,
                     'source': [{'outbound': ['isa',
                                              'experiment_protocol_fkey']},
                                'timepoint'],
                     'ux_mode': 'choices'},
                    {'entity': True,
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'experiment_experiment_type_fkey']},
                                'name']}]}}

visible_foreign_keys=\
{'detailed': [['isa', 'experiment_control_assay_fkey'],
              {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                          'RID']},
              {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                          {'inbound': ['isa', 'processed_data_replicate_fkey']},
                          'RID']},
              {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                          {'inbound': ['isa',
                                       'xray_tomography_data_biosample_fkey']},
                          'RID']},
              {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                          {'inbound': ['isa', 'imaging_data_replicate_fkey']},
                          'RID']},
              {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                          {'inbound': ['isa', 'mesh_data_biosample_fkey']},
                          'RID']}],
 'entry': [['isa', 'experiment_control_assay_fkey'],
           ['viz', 'model_experiment_fkey'],
           ['isa', 'biosample_experiment_fkey'],
           {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                       {'inbound': ['isa',
                                    'xray_tomography_data_biosample_fkey']},
                       'RID']},
           {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                       {'inbound': ['isa', 'processed_data_replicate_fkey']},
                       'RID']},
           {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                       {'inbound': ['isa', 'imaging_data_replicate_fkey']},
                       'RID']},
           {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                       {'inbound': ['isa', 'mesh_data_replicate_fkey']},
                       'RID']},
           {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                       {'inbound': ['isa', 'track_data_replicate_fkey']},
                       'RID']}]}

table_display=\
{'row_name': {'row_markdown_pattern': '{{RID}}{{#local_identifier}} - '
                                      '{{local_identifier}} '
                                      '{{/local_identifier}}{{#biosample_summary}} '
                                      '- '
                                      '{{biosample_summary}}{{/biosample_summary}}'}}

table_acls={}
table_acl_bindings=\
{'curated_status_guard': {'projection': [{'outbound': ['isa',
                                                       'experiment_dataset_fkey']},
                                         {'filter': 'status',
                                          'operand': 'commons:226:',
                                          'operator': '='},
                                         'RID'],
                          'projection_type': 'nonnull',
                          'scope_acl': ['*'],
                          'types': ['select']},
 'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'experiment_dataset_fkey']},
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
{'row_name': {'row_markdown_pattern': '{{RID}}{{#local_identifier}} - '
                                      '{{local_identifier}} '
                                      '{{/local_identifier}}{{#biosample_summary}} '
                                      '- '
                                      '{{biosample_summary}}{{/biosample_summary}}'}}
,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
}
column_annotations = \
{'biosample_summary': {'tag:isrd.isi.edu,2016:generated': None},
 'experiment_type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_experiment_type_fkey.rowName}}}'}}},
 'protocol': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_protocol_fkey.rowName}}}'}}}}



table_def = em.Table.define('experiment',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
