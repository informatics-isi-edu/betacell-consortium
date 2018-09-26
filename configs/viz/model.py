import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'model'
schema_name = 'viz'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}},
    ),
    em.Column.define('label', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('bg_color_r', em.builtin_types['int4'],
    ),
    em.Column.define('bg_color_g', em.builtin_types['int4'],
    ),
    em.Column.define('bg_color_b', em.builtin_types['int4'],
    ),
    em.Column.define('bounding_box_color_r', em.builtin_types['int4'],
    ),
    em.Column.define('bounding_box_color_g', em.builtin_types['int4'],
    ),
    em.Column.define('bounding_box_color_b', em.builtin_types['int4'],
    ),
    em.Column.define('show_bounding_box', em.builtin_types['boolean'],
    ),
    em.Column.define('rotate', em.builtin_types['boolean'],
    ),
    em.Column.define('volume', em.builtin_types['text'],
    ),
    em.Column.define('biosample', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('viz', 'model_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('viz', 'model_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['biosample'],
            'isa', 'biosample', ['RID'],
            constraint_names=[('viz', 'model_biosample_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
]


visible_columns = \
{'compact': [['viz', 'model_dataset_fkey'], 'label', 'description',
             {'markdown_name': 'Cell Line',
              'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'outbound': ['isa', 'specimen_cell_line_fkey']},
                         {'outbound': ['isa',
                                       'cell_line_cell_line_terms_fkey']},
                         'name']},
             {'aggregate': 'array',
              'comment': 'Compound used to treat the cell line for the '
                         'experiment',
              'entity': True,
              'markdown_name': 'Compound',
              'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'inbound': ['isa',
                                      'specimen_compound_specimen_fkey']},
                         {'outbound': ['isa',
                                       'specimen_compound_compound_fkey']},
                         'RID']},
             {'aggregate': 'array',
              'comment': 'Concentration of compound applied to cell line in mM',
              'entity': True,
              'markdown_name': 'Concentration',
              'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'inbound': ['isa',
                                      'specimen_compound_specimen_fkey']},
                         'compound_concentration']},
             {'comment': 'Measured in minutes',
              'entity': True,
              'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_specimen_fkey']},
                         'timepoint']}],
 'detailed': [['viz', 'model_dataset_fkey'], 'label', 'description',
              'bg_color_r', 'bg_color_g', 'bg_color_b', 'bounding_box_color_r',
              'bounding_box_color_g', 'bounding_box_color_b',
              'show_bounding_box', 'rotate', 'volume',
              {'entity': True,
               'markdown_name': 'Cell Line',
               'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                          {'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'outbound': ['isa', 'specimen_cell_line_fkey']},
                          {'outbound': ['isa',
                                        'cell_line_cell_line_terms_fkey']},
                          'name']},
              {'aggregate': 'array',
               'entity': True,
               'markdown_name': 'Compound',
               'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                          {'outbound': ['isa', 'experiment_protocol_fkey']},
                          {'inbound': ['isa',
                                       'protocol_treatment_protocol_fkey']},
                          {'outbound': ['isa',
                                        'protocol_treatment_treatment_fkey']},
                          'RID']},
              {'aggregate': 'array',
               'entity': True,
               'markdown_name': 'Concentration',
               'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                          {'outbound': ['isa', 'experiment_protocol_fkey']},
                          {'inbound': ['isa',
                                       'protocol_treatment_protocol_fkey']},
                          'treatment_concentration']},
              ['viz', 'model_derived_from_fkey']],
 'filter': {'and': [{'markdown_name': 'Cell Line',
                     'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                                {'outbound': ['isa',
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
                     'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                                {'outbound': ['isa',
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
                     'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                                {'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'inbound': ['isa',
                                             'specimen_compound_specimen_fkey']},
                                'compound_concentration']},
                    {'comment': 'Measured in minutes',
                     'entity': True,
                     'source': [{'outbound': ['viz', 'model_biosample_fkey']},
                                {'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                'timepoint']}]}}

visible_foreign_keys = \
{'detailed': [{'source': [{'outbound': ['viz', 'model_biosammple_fkey']},
                          'RID']}]}

table_comment = \
None

table_display = \
{'compact': {'row_markdown_pattern': ':::iframe '
                                     '[{{{label}}}](/mesh-viewer/view.html?model=/ermrest/catalog/1/entity/viz:model_json/RID={{{_RID}}}){width=1024 '
                                     'height=768 .iframe} \n'
                                     ':::'}}

table_acls = {}
table_acl_bindings = {}
export = \
{'templates': [{'format_name': 'BDBag',
                'format_type': 'BAG',
                'name': 'default',
                'outputs': [{'destination': {'name': 'surface-model',
                                             'type': 'csv'},
                             'source': {'api': 'entity', 'table': 'viz:model'}},
                            {'destination': {'name': 'OBJS',
                                             'type': 'download'},
                             'source': {'api': 'attribute',
                                        'path': 'isa:mesh_data/url',
                                        'table': 'viz:model_mesh_data'}}]}]}

table_annotations = {
    "tag:isrd.isi.edu,2016:export": export,
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:misd.isi.edu,2015:display":
{'name': '3D Surface Models'}
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
 'RMT': 'System-generated row modification timestamp'}

column_annotations = \
{'id': {'tag:isrd.isi.edu,2016:column-display': {},
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
