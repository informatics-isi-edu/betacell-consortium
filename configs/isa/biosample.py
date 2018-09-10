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
    em.Column.define('local_identifier', em.builtin_types['text'],
    ),
    em.Column.define('summary', em.builtin_types['text'],
    ),
    em.Column.define('collection_date', em.builtin_types['date'],
    ),
    em.Column.define('_keywords', em.builtin_types['text'],
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
]


key_defs = [
    em.Key.define(['dataset', 'RID'],
                   constraint_names=[('isa', 'biosample_RID_dataset_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'biosample_pkey')],
       annotations = {'tag:misd.isi.edu,2015:display': {}},
    ),
    em.Key.define(['dataset', 'local_identifier'],
                   constraint_names=[('isa', 'biosample_dataset_local_identifier_key')],
       annotations = {'tag:misd.isi.edu,2015:display': {}},
    ),
]


fkey_defs = [
    em.ForeignKey.define(['specimen'],
            'isa', 'specimen', ['RID'],
            constraint_names=[('isa', 'biosample_specimen_fkey')],
    ),
    em.ForeignKey.define(['experiment'],
            'isa', 'experiment', ['RID'],
            constraint_names=[('isa', 'biosample_experiment_fkey')],
    ),
    em.ForeignKey.define(['specimen_type'],
            'vocab', 'specimen_type_terms', ['id'],
            constraint_names=[('isa', 'biosample_specimen_type_fkey')],
        comment='Must be a valid reference to a specimen type.',
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'biosample_dataset_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns = \
{'compact': [['isa', 'biosample_pkey'],
             {'markdown_name': 'Cell Line',
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'outbound': ['isa', 'specimen_cell_line_fkey']},
                         {'outbound': ['isa',
                                       'cell_line_cell_line_terms_fkey']},
                         'name']},
             {'aggregate': 'array',
              'comment': 'Compound used to treat the cell line for the '
                         'experiment',
              'entity': True,
              'markdown_name': 'Compound',
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'inbound': ['isa',
                                      'specimen_compound_specimen_fkey']},
                         {'outbound': ['isa',
                                       'specimen_compound_compound_fkey']},
                         'RID']},
             {'aggregate': 'array',
              'comment': 'Concentration of compound applied to cell line in mM',
              'entity': True,
              'markdown_name': 'Concentration',
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'inbound': ['isa',
                                      'specimen_compound_specimen_fkey']},
                         'compound_concentration']},
             {'comment': 'Measured in minutes',
              'entity': True,
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         'timepoint']},
             'capillary_number', 'sample_position'],
 'detailed': [['isa', 'biosample_pkey'], ['isa', 'biosample_dataset_fkey'],
              'summary', ['isa', 'biosample_specimen_fkey'],
              ['isa', 'biosample_experiment_fkey'],
              {'source': [{'outbound': ['isa', 'biosample_experiment_fkey']},
                          'RID']},
              {'markdown_name': 'Cell Line',
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'outbound': ['isa', 'specimen_cell_line_fkey']},
                          {'outbound': ['isa',
                                        'cell_line_cell_line_terms_fkey']},
                          'name']},
              {'aggregate': 'array',
               'comment': 'Compound used to treat the cell line for the '
                          'experiment',
               'entity': True,
               'markdown_name': 'Compound',
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'inbound': ['isa',
                                       'specimen_compound_specimen_fkey']},
                          {'outbound': ['isa',
                                        'specimen_compound_compound_fkey']},
                          'RID']},
              {'aggregate': 'array',
               'comment': 'Concentration of compound applied to cell line in '
                          'mM',
               'entity': True,
               'markdown_name': 'Concentration',
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'inbound': ['isa',
                                       'specimen_compound_specimen_fkey']},
                          'compound_concentration']},
              {'comment': 'Measured in minutes',
               'entity': True,
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          'timepoint']},
              [['isa', 'biosample_specimen_fkey'],
               ['isa', 'specimen_species_fkey']],
              ['isa', 'biosample_specimen_type_fkey'], 'capillary_number',
              'sample_position', 'collection_date'],
 'entry': [['isa', 'biosample_dataset_fkey'],
           ['isa', ['biosample_experiment_fkey']], 'local_identifier',
           ['isa', 'biosample_specimen_fkey'],
           ['isa', 'biosample_specimen_type_fkey'], 'capillary_number',
           'sample_position', 'collection_date'],
 'filter': {'and': [{'entity': True, 'source': 'RID'},
                    {'markdown_name': 'Cell Line',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                {'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'aggregate': 'array',
                     'comment': 'Compound used to treat the cell line for the '
                                'experiment',
                     'entity': True,
                     'markdown_name': 'Compound',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'inbound': ['isa',
                                             'specimen_compound_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_compound_compound_fkey']},
                                'RID']},
                    {'aggregate': 'array',
                     'comment': 'Concentration of compound applied to cell '
                                'line in mM',
                     'entity': True,
                     'markdown_name': 'Concentration',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'inbound': ['isa',
                                             'specimen_compound_specimen_fkey']},
                                'compound_concentration'],
                     'ux_mode': 'choices'},
                    {'comment': 'Measured in minutes',
                     'entity': True,
                     'markdown_name': 'Timepoint',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                'timepoint'],
                     'ux_mode': 'choices'},
                    {'markdown_name': 'Species',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_species_fkey']},
                                'name']},
                    {'markdown_name': 'Anatomy',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_anatomy_fkey']},
                                'name']},
                    {'source': [{'inbound': ['isa',
                                             'mesh_data_biosample_fkey']},
                                'url']},
                    {'source': [{'inbound': ['isa',
                                             'processed_tomography_data_biosample_fkey']},
                                'url']},
                    {'entity': True, 'source': 'capillary_number'}]}}

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
    "table_display": table_display,
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



table_def = em.Table.define('biosample',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
