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
    em.Column.define('protocol', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_protocol_fkey.rowName}}}'}}},
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
]


key_defs = [
    em.Key.define(['dataset', 'RID'],
                   constraint_names=[('isa', 'experiment_RID_dataset_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'experiment_pkey')],
    ),
    em.Key.define(['local_identifier', 'dataset'],
                   constraint_names=[('isa', 'experiment_dataset_local_identifier_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'experiment_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['protocol'],
            'Beta_Cell', 'Protocol', ['RID'],
            constraint_names=[('isa', 'experiment_protocol_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['experiment_type'],
            'vocab', 'experiment_type_terms', ['RID'],
            constraint_names=[('isa', 'experiment_experiment_type_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns = \
{'*': ['RID', ['isa', 'specimen_pkey'], ['isa','experiment_protocol_fkey'],
       ['isa','experiment_experiment_type_fkey'],
       {'aggregate': 'array_d',
        'entity': True,
        'markdown_name': 'Cell Line',
        'open': True,
        'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_cell_line_fkey']},
                   {'outbound': ['isa', 'cell_line_cell_line_terms_fkey']},
                   'name']},
       {'markdown_name': 'Cellular Location',
        'source': [{'inbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa',
                                 'specimen_cellular_location_terms_fkey']},
                   'name']},
       {'aggregate': 'array_d',
        'comment': 'Additives used to treat the specimens for the experiment',
        'entity': True,
        'markdown_name': 'Additive',
        'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_protocol_fkey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   {'outbound': ['Beta_Cell',
                                 'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                   'RID']},
       {'aggregate': 'array_d',
        'comment': 'Concentration of additive applied to cell line in mM',
        'entity': True,
        'markdown_name': 'Concentration',
        'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_protocol_fkey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   'Additive_Concentration'],
        'ux_mode': 'choices'},
       {'aggregate': 'array_d',
        'comment': 'Duration in minutes of additive applied to cell line in ',
        'entity': True,
        'markdown_name': 'Duration',
        'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_protocol_fkey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'Duration'],
        'ux_mode': 'choices'},
       'description'],
 'entry': [['isa', 'specimen_dataset_fkey'],
           ['isa', 'experiment_protocol_fkey'],
           ['isa', 'experiment_protocol_fkey'], 'description',
           'collection_date'],
 'filter': {'and': ['RID', ['isa', 'specimen_pkey'], 'local_identifier',
                    'protocol', 'experiment_type',
                    {'aggregate': 'array_d',
                     'entity': True,
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
                    {'markdown_name': 'Cellular Location',
                     'source': [{'inbound': ['isa', 'biosample_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_cellular_location_terms_fkey']},
                                'name']},
                    {'aggregate': 'array_d',
                     'comment': 'Additives used to treat the specimens for the '
                                'experiment',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'inbound': ['isa',
                                             'biosample_experiment_fkey']},
                                {'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                'RID']},
                    {'aggregate': 'array_d',
                     'comment': 'Concentration of additive applied to cell '
                                'line in mM',
                     'entity': True,
                     'markdown_name': 'Concentration',
                     'source': [{'inbound': ['isa',
                                             'biosample_experiment_fkey']},
                                {'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                'Additive_Concentration'],
                     'ux_mode': 'choices'},
                    {'aggregate': 'array_d',
                     'comment': 'Duration in minutes of additive applied to '
                                'cell line in ',
                     'entity': True,
                     'markdown_name': 'Duration',
                     'source': [{'inbound': ['isa',
                                             'biosample_experiment_fkey']},
                                {'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                'Duration'],
                     'ux_mode': 'choices'}]}}

visible_foreign_keys = \
{'*': [['viz', 'model_experiment_fkey'],
       {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']}, 'RID']},
       {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'inbound': ['isa', 'xray_tomography_data_biosample_fkey']},
                   'RID']},
       {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'inbound': ['isa', 'processed_data_bioasample_fkey']},
                   'RID']},
       {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'inbound': ['isa', 'imaging_data_biosample_fkey']},
                   'RID']},
       {'source': [{'inbound': ['isa', 'biosample_experiment_fkey']},
                   {'inbound': ['isa', 'mesh_data_biosample_fkey']}, 'RID']}]}

table_comment = \
None

table_display = \
{'row_name': {'row_markdown_pattern': '{{RID}}{{#local_identifier}} - '
                                      '{{local_identifier}} '
                                      '{{/local_identifier}}{{#biosample_summary}} '
                                      '- '
                                      '{{biosample_summary}}{{/biosample_summary}}'}}



table_acls = {}
table_acl_bindings = \
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
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:misd.isi.edu,2015:display":
{}
,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:table-alternatives":
{}
,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp',
 'biosample_summary': 'System-generated column with summary of all related '
                      'biosamples'}

column_annotations = \
{'biosample_summary': {'tag:isrd.isi.edu,2016:generated': None},
 'experiment_type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_experiment_type_fkey.rowName}}}'}}},
 }



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
