import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Experiment'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('Experiment_Type', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Experiment_Type_FKey.rowName}}}'}}},
    ),
    em.Column.define('Protocol', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'}}},
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
    ),
]


key_defs = [
    em.Key.define(['RID', 'Dataset'],
                   constraint_names=[('Beta_Cell', 'Experiment_RID_Dataset_Key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'Experiment_RID_Key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Dataset'],
            'Beta_Cell', 'Dataset', ['RID'],
            constraint_names=[('Beta_Cell', 'Experiment_Dataset_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['Protocol'],
            'Beta_Cell', 'Protocol', ['RID'],
            constraint_names=[('Beta_Cell', 'Experiment_Protocol_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['Experiment_Type'],
            'vocab', 'experiment_type_terms', ['RID'],
            constraint_names=[('Beta_Cell', 'Experiment_Experiment_Type_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns = \
{'*': ['RID', ['Beta_Cell', 'Experiment_Dataset_FKey'],
       ['Beta_Cell', 'Experiment_Protocol_FKey'],
       ['Beta_Cell', 'Experiment_Experiment_Type_FKey'],
       {'aggregate': 'array_d',
        'entity': True,
        'markdown_name': 'Cell Line',
        'open': True,
        'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']},
                   {'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']},
                   {'outbound': ['Beta_Cell',
                                 'Cell_Line_Cell_Line_Terms_FKey']},
                   'name']},
       {'aggregate': 'array_d',
        'comment': 'Additives used to treat the specimens for the experiment',
        'entity': True,
        'markdown_name': 'Additive',
        'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']},
                   {'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']},
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
                   {'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']},
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
                   {'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'Duration'],
        'ux_mode': 'choices'},
       'description'],
 'entry': [['Beta_Cell', 'Experiment_Dataset_FKey'],
           ['Beta_Cell', 'Experiment_Protocol_fkey'],
           ['Beta_Cell', 'Experiment_Experiment_Type_FKey'], 'description',
           'collection_date'],
 'filter': {'and': [{'entity': True, 'source': 'RID'},
                    {'source': [{'outbound': ['Beta_Cell',
                                              'Experiment_Dataset_FKey']},
                                'RID']},
                    {'source': [{'outbound': ['Beta_Cell',
                                              'Experiment_Protocol_FKey']},
                                'RID']},
                    {'source': [{'outbound': ['Beta_Cell',
                                              'Experiment_Experiment_Type_FKey']},
                                'RID']},
                    {'aggregate': 'array_d',
                     'entity': True,
                     'markdown_name': 'Cell Line',
                     'open': True,
                     'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Specimen_Cell_Line_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Cell_Line_cell_Line_Terms_fkey']},
                                'name']},
                    {'markdown_name': 'Cellular Location',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Specimen_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Specimen_cellular_location_terms_fkey']},
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
                                {'outbound': ['Beta_Cell',
                                              'Specimen_Protocol_FKey']},
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
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Specimen_Protocol_FKey']},
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
                                {'outbound': ['Beta_Cell',
                                              'Specimen_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                'Duration'],
                     'ux_mode': 'choices'},
                    {'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'XRay_Tomography_Data_Biosample_FKey']},
                                'RID']},
                    {'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Processed_Tomography_Data_Bioasample_FKey']},
                                'RID']},
                    {'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Experiment_FKey']},
                                {'inbound': ['isa',
                                             'mesh_data_biosample_fkey']},
                                'RID']}]}}

visible_foreign_keys = \
{'*': [['viz', 'model_experiment_fkey'],
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   'RID']},
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'inbound': ['Beta_Cell',
                                'XRay_Tomography_Data_Biosample_FKey']},
                   'RID']},
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Processed_Tomography_Data_Bioasample_FKey']},
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
table_acl_bindings = {}
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
column_annotations = \
{'Experiment_Type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Experiment_Type_FKey.rowName}}}'}}},
 'Protocol': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'}}}}



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
