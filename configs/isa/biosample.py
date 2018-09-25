import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'biosample'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}},
    ),
    em.Column.define('summary', em.builtin_types['text'],
    ),
    em.Column.define('collection_date', em.builtin_types['date'],
    ),
    em.Column.define('capillary_number', em.builtin_types['int2'],
        comment='ID number of the capillary constaining the biosample.',
    ),
    em.Column.define('sample_position', em.builtin_types['int2'],
        comment='Position in the capillary where the sample is located.',
    ),
    em.Column.define('specimen', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}},
        comment='Biological material used for the biosample.',
    ),
    em.Column.define('specimen_type', em.builtin_types['text'],
        comment='Method by which specimen is prepared.',
    ),
    em.Column.define('experiment', em.builtin_types['ermrest_rid'],
        comment='Experiment in which this biosample is used',
    ),
    em.Column.define('protocol', em.builtin_types['text'],
        comment='Experiment protocol.',
    ),
]


key_defs = [
    em.Key.define(['dataset', 'RID'],
                   constraint_names=[('isa', 'biosample_RID_dataset_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'biosample_pkey')],
       annotations = {'tag:misd.isi.edu,2015:display': {}},
    ),
]


fkey_defs = [
    em.ForeignKey.define(['protocol'],
            'Beta_Cell', 'Protocol', ['RID'],
            constraint_names=[('isa', 'biosample_protocol_fkey')],
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'biosample_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['experiment'],
            'isa', 'experiment', ['RID'],
            constraint_names=[('isa', 'biosample_experiment_fkey')],
    ),
    em.ForeignKey.define(['specimen'],
            'isa', 'specimen', ['RID'],
            constraint_names=[('isa', 'biosample_specimen_fkey')],
    ),
    em.ForeignKey.define(['specimen_type'],
            'vocab', 'specimen_type_terms', ['id'],
            constraint_names=[('isa', 'biosample_specimen_type_fkey')],
        comment='Must be a valid reference to a specimen type.',
    ),
]


visible_columns = \
{'*': [['isa', 'biosample_pkey'], ['isa', 'biosample_dataset_fkey'], 'summary',
       ['isa', 'biosample_specimen_fkey'], ['isa', 'biosample_experiment_fkey'],
       {'source': [{'outbound': ['isa', 'biosample_experiment_fkey']}, 'RID']},
       {'markdown_name': 'Cell Line',
        'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_cell_line_fkey']},
                   {'outbound': ['isa', 'cell_line_cell_line_terms_fkey']},
                   'name']},
       {'aggregate': 'array',
        'comment': 'Compound used to treat the cell line for the experiment',
        'entity': True,
        'markdown_name': 'Additive',
        'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_protocol_fkey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   {'outbound': ['Beta_Cell',
                                 'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                   'RID']},
       {'aggregate': 'array',
        'comment': 'Concentration of additive applied to cell line in mM',
        'entity': True,
        'markdown_name': 'Concentration',
        'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_protocol_fkey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   'Additive_Concentration']},
       {'aggregate': 'array',
        'comment': 'Duration in minutes of additive applied to cell line in ',
        'entity': True,
        'markdown_name': 'Duration',
        'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                   {'outbound': ['isa', 'specimen_protocol_fkey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'Duration']},
       ['isa', 'biosample_specimen_type_fkey'], 'capillary_number',
       'sample_position', 'collection_date'],
 'entry': [['isa', 'biosample_dataset_fkey'],
           ['isa', 'biosample_experiment_fkey'], 'local_identifier',
           ['isa', 'biosample_protocol_fkey'],
           ['isa', 'biosample_specimen_fkey'],
           ['isa', 'biosample_specimen_type_fkey'], 'capillary_number',
           'sample_position', 'collection_date'],
 'filter': {'and': [{'entity': True, 'source': 'RID'},
                    {'source': [{'outbound': ['isa', 'biosample_dataset_fkey']},
                                'RID']},
                    {'markdown_name': 'Cell Line',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                {'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'aggregate': 'array',
                     'comment': 'Additives used to treat the cell line for the '
                                'experiment',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                'RID']},
                    {'aggregate': 'array',
                     'comment': 'Concentration of additive applied to cell '
                                'line in mM',
                     'entity': True,
                     'markdown_name': 'Concentration',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                'Additive_Concentration'],
                     'ux_mode': 'choices'},
                    {'aggregate': 'array',
                     'comment': 'Duration in minutes of additive applied to '
                                'cell line in ',
                     'entity': True,
                     'markdown_name': 'Duration',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                'Duration'],
                     'ux_mode': 'choices'},
                    ['isa', 'biosample_specimen_type_fkey'],
                    {'source': [{'inbound': ['isa',
                                             'mesh_data_biosample_fkey']},
                                'url']},
                    {'source': [{'inbound': ['isa',
                                             'processed_tomography_data_biosample_fkey']},
                                'url']},
                    {'entity': True,
                     'source': 'capillary_number',
                     'ux_mode': 'choices'}]}}

visible_foreign_keys = \
{'*': [{'source': [{'inbound': ['isa', 'xray_tomography_data_biosample_fkey']},
                   'RID']},
       {'source': [{'inbound': ['isa',
                                'processed_tomography_data_biosample_fkey']},
                   'RID']},
       ['viz', 'model_biosample_fkey']]}

table_comment = \
None

table_display = \
{'row_name': {'row_markdown_pattern': '{{RID}} - '
                                      '{{summary}}{{#local_identifier}} '
                                      '[{{local_identifier}}] '
                                      '{{/local_identifier}}'}}

table_acls = {}
table_acl_bindings = {}
export = \
{'templates': [{'format_name': 'BDBag',
                'format_type': 'BAG',
                'name': 'default',
                'outputs': [{'destination': {'name': 'biosample',
                                             'type': 'csv'},
                             'source': {'api': 'entity',
                                        'table': 'isa:biosample'}},
                            {'destination': {'name': 'MRC', 'type': 'download'},
                             'source': {'api': 'attribute',
                                        'path': 'url',
                                        'table': 'isa:xray_tomography_data'}},
                            {'destination': {'name': 'processed_data',
                                             'type': 'download'},
                             'source': {'api': 'attribute',
                                        'path': 'url',
                                        'table': 'isa:processed_tomography_data'}},
                            {'destination': {'name': 'OBJS',
                                             'type': 'download'},
                             'source': {'api': 'attribute',
                                        'path': 'url',
                                        'table': 'isa:mesh_data'}}]}]}

table_annotations = {
    "tag:isrd.isi.edu,2016:export": export,
    "tag:isrd.isi.edu,2016:table-alternatives":
{}
,
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:misd.isi.edu,2015:display":
{}
,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp',
 'capillary_number': 'ID number of the capillary constaining the biosample.',
 'experiment': 'Experiment in which this biosample is used',
 'protocol': 'Experiment protocol.',
 'sample_position': 'Position in the capillary where the sample is located.',
 'specimen': 'Biological material used for the biosample.',
 'specimen_type': 'Method by which specimen is prepared.'}

column_annotations = \
{'dataset': {'tag:isrd.isi.edu,2016:column-display': {},
             'tag:isrd.isi.edu,2017:asset': {},
             'tag:misd.isi.edu,2015:display': {}},
 'specimen': {'tag:isrd.isi.edu,2016:column-display': {},
              'tag:isrd.isi.edu,2017:asset': {},
              'tag:misd.isi.edu,2015:display': {}}}



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
