import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Specimen'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Description', em.builtin_types['text'],
        comment='Description of the specimen.',
    ),
    em.Column.define('Collection_Date', em.builtin_types['date'],
        comment='Date the specimen was obtained',
    ),
    em.Column.define('Cell_Line', em.builtin_types['text'],
        comment='Cell line used for the specimen.',
    ),
    em.Column.define('Cellular_Location', em.builtin_types['text'],
        comment='Cellular location of the specimen',
    ),
    em.Column.define('Protocol', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'}}},
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'Specimen_RIDkey1')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Cell_Line'],
            'Beta_Cell', 'Cell_Line', ['RID'],
            constraint_names=[('Beta_Cell', 'Specimen_Cell_Line_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(['Cellular_Location'],
            'vocab', 'cellular_location_terms', ['id'],
            constraint_names=[('Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['Protocol'],
            'Beta_Cell', 'Protocol', ['RID'],
            constraint_names=[('Beta_Cell', 'Specimen_Protocol_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns = \
{'*': ['RID', 'Protocol',
       {'entity': True,
        'markdown_name': 'Cell Line',
        'open': True,
        'source': [{'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']},
                   {'outbound': ['Beta_Cell',
                                 'Cell_Line_Cell_Line_Terms_FKey']},
                   'name']},
       {'markdown_name': 'Cellular Location',
        'source': [{'outbound': ['Beta_Cell',
                                 'Specimen_Cellular_Location_Terms_FKey']},
                   'name']},
       {'aggregate': 'array',
        'comment': 'Additive used to treat the cell line for the experiment',
        'entity': True,
        'markdown_name': 'Additive',
        'source': [{'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']},
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
        'source': [{'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   'Additive_Concentration'],
        'ux_mode': 'choices'},
       {'aggregate': 'array',
        'comment': 'Duration in minutes',
        'entity': True,
        'markdown_name': 'Duration',
        'source': [{'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'Duration'],
        'ux_mode': 'choices'},
       'Description', 'Collection_Date'],
 'entry': [['Beta_Cell', 'Specimen_Cell_Line_FKey'],
           ['Beta_Cell', 'Specimen_Protocol_FKey'],
           ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey'],
           'Description', 'Collection_Date'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Cell Line',
                     'open': True,
                     'source': [{'outbound': ['Beta_Cell',
                                              'Specimen_Cell_Line_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Cell_Line_Cell_Line_Terms_FKey']},
                                'name']},
                    {'markdown_name': 'Cellular Location',
                     'source': [{'outbound': ['Beta_Cell',
                                              'Specimen_Cellular_Location_Terms_FKey']},
                                'name']},
                    {'aggregate': 'array',
                     'comment': 'Additive used to treat the cell line for the '
                                'experiment',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'outbound': ['Beta_Cell',
                                              'Specimen_Protocol_FKey']},
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
                     'source': [{'outbound': ['Beta_Cell',
                                              'Specimen_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                'Additive_Concentration'],
                     'ux_mode': 'choices'},
                    {'aggregate': 'array',
                     'comment': 'Duration in minutes',
                     'entity': True,
                     'markdown_name': 'Duration',
                     'source': [{'outbound': ['Beta_Cell',
                                              'Specimen_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                'Duration'],
                     'ux_mode': 'choices'},
                    {'source': [{'inbound': ['Beta_Cell',
                                             'Biosample_Specimen_FKey']},
                                'RID']},
                    'Description', 'Collection_Date']}}

visible_foreign_keys = \
{'*': [{'source': [{'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']},
                   {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'RID']},
       {'source': [{'inbound': ['Beta_Cell', 'Biosample_Specimen_FKey']},
                   'RID']}]}

table_comment = \
'Table of biological speciments from which biosamples will be created.'

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "table_display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Cell_Line': 'Cell line used for the specimen.',
 'Cellular_Location': 'Cellular location of the specimen',
 'Collection_Date': 'Date the specimen was obtained',
 'Description': 'Description of the specimen.'}

column_annotations = \
{'Protocol': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'}}}}



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
