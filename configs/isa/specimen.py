import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'specimen'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
                     comment='Cell line used for the speciman.',
                     ),
    em.Column.define('description', em.builtin_types['text'],
                     comment='Description of the specimen.',
                     ),
    em.Column.define('collection_date', em.builtin_types['date'],
                     comment='Date the specimen was obtained',
                     ),
    em.Column.define('cell_line', em.builtin_types['text'],
                     comment='Cell line used for the speciman.',
                     ),
    em.Column.define('cellular_location', em.builtin_types['text'],
                     comment='Cellular location of the specimen',
                     ),
    em.Column.define('timepoint', em.builtin_types['int2'],
                     comment='Measured in minutes.',
                     ),
    em.Column.define('protocol', em.builtin_types['text'],
                     annotations={'tag:isrd.isi.edu,2016:column-display': {
                         'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_protocol_fkey.rowName}}}'}}},
                     ),
]

key_defs = [
    em.Key.define(['dataset', 'RID'],
                  constraint_names=[('isa', 'specimen_RID_key')],
                  comment='RID and dataset must be distinct.',
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('isa', 'specimen_RIDkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['cell_line'],
                         'isa', 'cell_line', ['RID'],
                         constraint_names=[('isa', 'specimen_cell_line_fkey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         comment='Must be a valid reference to a cell line.',
                         ),
    em.ForeignKey.define(['protocol'],
                         'Beta_Cell', 'Protocol', ['RID'],
                         constraint_names=[('isa', 'specimen_protocol_fkey')],
                         ),
    em.ForeignKey.define(['dataset'],
                         'isa', 'dataset', ['RID'],
                         constraint_names=[('isa', 'specimen_dataset_fkey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         ),
    em.ForeignKey.define(['cellular_location'],
                         'vocab', 'cellular_location_terms', ['id'],
                         constraint_names=[('isa', 'specimen_cellular_location_terms_fkey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         ),
]

visible_columns = \
    {'*': ['RID', ['isa', 'specimen_pkey'], 'local_identifier', 'Protocol',
           {'entity': True,
            'markdown_name': 'Cell Line',
            'open': True,
            'source': [{'outbound': ['isa', 'specimen_cell_line_fkey']},
                       {'outbound': ['isa', 'cell_line_cell_line_terms_fkey']},
                       'name']},
           {'markdown_name': 'Cellular Location',
            'source': [{'outbound': ['isa',
                                     'specimen_cellular_location_terms_fkey']},
                       'name']},
           {'aggregate': 'array',
            'comment': 'Compound used to treat the cell line for the experiment',
            'entity': True,
            'markdown_name': 'Compound',
            'source': [{'inbound': ['isa', 'specimen_compound_specimen_fkey']},
                       {'outbound': ['isa', 'specimen_compound_compound_fkey']},
                       'RID']},
           {'aggregate': 'array',
            'comment': 'Concentration of compound applied to cell line in mM',
            'entity': True,
            'markdown_name': 'Concentration',
            'source': [{'inbound': ['isa', 'specimen_compound_specimen_fkey']},
                       'compound_concentration'],
            'ux_mode': 'choices'},
           {'aggregate': 'array',
            'comment': 'Compound used to treat the cell line for the experiment',
            'entity': True,
            'markdown_name': 'Additive',
            'source': [{'outbound': ['isa', 'specimen_protocol_fkey']},
                       {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                       {'inbound': ['Beta_Cell',
                                    'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                       {'outbound': ['Beta_Cell',
                                     'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                       'RID']},
           {'aggregate': 'array',
            'comment': 'Concentration of compound applied to cell line in mM',
            'entity': True,
            'markdown_name': 'Additive Concentration',
            'source': [{'outbound': ['isa', 'specimen_protocol_fkey']},
                       {'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                       {'inbound': ['Beta_Cell',
                                    'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                       'Additive_Concentration'],
            'ux_mode': 'choices'},
           {'comment': 'Measured in minutes',
            'source': ['timepoint'],
            'ux_mode': 'choices'},
           'description', 'collection_date'],
     'entry': [['isa', 'local_identifier'], ['isa', 'specimen_dataset_fkey'],
               ['isa', 'specimen_cell_line_fkey'],
               ['isa', 'specimen_protocol_fkey'],
               ['isa', 'specimen_compound_specimen_fkey'], 'timepoint',
               ['isa', 'specimen_cellular_location_terms_fkey'], 'description',
               'collection_date'],
     'filter': {'and': [{'entity': True,
                         'markdown_name': 'Cell Line',
                         'open': True,
                         'source': [{'outbound': ['isa',
                                                  'specimen_cell_line_fkey']},
                                    {'outbound': ['isa',
                                                  'cell_line_cell_line_terms_fkey']},
                                    'name']},
                        {'markdown_name': 'Cellular Location',
                         'source': [{'outbound': ['isa',
                                                  'specimen_cellular_location_terms_fkey']},
                                    'name']},
                        {'aggregate': 'array',
                         'comment': 'Compound used to treat the cell line for the '
                                    'experiment',
                         'entity': True,
                         'markdown_name': 'Compound',
                         'source': [{'inbound': ['isa',
                                                 'specimen_compound_specimen_fkey']},
                                    {'outbound': ['isa',
                                                  'specimen_compound_compound_fkey']},
                                    'RID']},
                        {'aggregate': 'array',
                         'comment': 'Concentration of compound applied to cell '
                                    'line in mM',
                         'entity': True,
                         'markdown_name': 'Concentration',
                         'source': [{'inbound': ['isa',
                                                 'specimen_compound_specimen_fkey']},
                                    'compound_concentration'],
                         'ux_mode': 'choices'},
                        {'comment': 'Measured in minutes',
                         'source': ['timepoint'],
                         'ux_mode': 'choices'},
                        'description', 'collection_date']}}

visible_foreign_keys = \
    {'*': [['isa', 'specimen_compound_specimen_fkey']]}

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
    {'cell_line': 'Cell line used for the speciman.',
     'cellular_location': 'Cellular location of the specimen',
     'collection_date': 'Date the specimen was obtained',
     'dataset': 'Cell line used for the speciman.',
     'description': 'Description of the specimen.',
     'timepoint': 'Measured in minutes.'}

column_annotations = \
    {'protocol': {'tag:isrd.isi.edu,2016:column-display': {
        'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_protocol_fkey.rowName}}}'}}}}

table_def = em.Table.define('specimen',
                            column_defs=column_defs,
                            key_defs=key_defs,
                            fkey_defs=fkey_defs,
                            annotations=table_annotations,
                            acls=table_acls,
                            acl_bindings=table_acl_bindings,
                            comment='Table of biological speciments from which biosamples will be created.',
                            provide_system=True
                            )
