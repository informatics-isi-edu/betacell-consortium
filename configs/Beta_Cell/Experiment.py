import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Experiment'
schema_name = 'Beta_Cell'

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
    em.Key.define(['local_identifier', 'dataset'],
                   constraint_names=[('isa', 'experiment_dataset_local_identifier_key')],
    ),
    em.Key.define(['RID', 'dataset'],
                   constraint_names=[('isa', 'experiment_RID_dataset_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'experiment_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['experiment_type'],
            'vocab', 'experiment_type_terms', ['RID'],
            constraint_names=[('isa', 'experiment_experiment_type_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['protocol'],
            'Beta_Cell', 'Protocol', ['RID'],
            constraint_names=[('isa', 'experiment_protocol_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'experiment_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns = \
{'*': ['RID', ['isa', 'experiment_dataset_fkey'],
       ['isa', 'experiment_protocol_fkey'],
       ['isa', 'experiment_experiment_type_fkey'],
       {'aggregate': 'array_d',
        'entity': True,
        'markdown_name': 'Cell Line',
        'open': True,
        'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']},
                   {'outbound': ['isa', 'specimen_cell_line_fkey']},
                   {'outbound': ['isa', 'cell_line_cell_line_terms_fkey']},
                   'name']},
       {'markdown_name': 'Cellular Location',
        'source': [{'inbound': ['isa', 'Biosample_Specimen_FKey']},
                   {'outbound': ['isa',
                                 'specimen_cellular_location_terms_fkey']},
                   'name']},
       {'aggregate': 'array_d',
        'comment': 'Additives used to treat the specimens for the experiment',
        'entity': True,
        'markdown_name': 'Additive',
        'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']},
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
        'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']},
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
        'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']},
                   {'outbound': ['isa', 'specimen_protocol_fkey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'Duration'],
        'ux_mode': 'choices'},
       'description'],
 'entry': [['isa', 'experiment_dataset_fkey'],
           ['isa', 'experiment_protocol_fkey'],
           ['isa', 'experiment_experiment_type_fkey'], 'description',
           'collection_date'],
 'filter': {'and': [{'entity': True, 'source': 'RID'},
                    {'source': [{'outbound': ['isa',
                                              'experiment_dataset_fkey']},
                                'RID']},
                    {'source': [{'outbound': ['isa',
                                              'experiment_protocol_fkey']},
                                'RID']},
                    {'source': [{'outbound': ['isa',
                                              'experiment_experiment_type_fkey']},
                                'RID']},
                    {'aggregate': 'array_d',
                     'entity': True,
                     'markdown_name': 'Cell Line',
                     'open': True,
                     'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                {'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'markdown_name': 'Cellular Location',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Specimen_FKey']},
                                {'outbound': ['isa',
                                              'specimen_cellular_location_terms_fkey']},
                                'name']},
                    {'aggregate': 'array_d',
                     'comment': 'Additives used to treat the specimens for the '
                                'experiment',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
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
                     'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'outbound': ['isa',
                                              'Biosample_Specimen_FKey']},
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
                     'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                'Duration'],
                     'ux_mode': 'choices'}]}}

visible_foreign_keys = \
{'*': [['viz', 'model_experiment_fkey'],
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   'RID']},
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'inbound': ['Beta_Cell',
                                'XRay_Tomography_Data_Biosample_FKey']},
                   'RID']},
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'inbound': ['isa', 'processed_data_bioasample_fkey']},
                   'RID']},
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'inbound': ['isa', 'imaging_data_biosample_fkey']},
                   'RID']},
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
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
{'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
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
 'protocol': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_protocol_fkey.rowName}}}'}}}}



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
