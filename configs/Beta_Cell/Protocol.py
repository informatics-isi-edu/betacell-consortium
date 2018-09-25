import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Protocol'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Name', em.builtin_types['text'],
        nullok=False,
        comment='The name for this protocol.',
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
        comment='A description of the protocol.',
    ),
    em.Column.define('Type', em.builtin_types['text'],
        nullok=False,
        comment='The type of object for which this protocol is used.',
    ),
]


key_defs = [
    em.Key.define(['Name'],
                   constraint_names=[('Beta_Cell', 'Protocol_idkey1')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'Protocol_RIDkey1')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Type'],
            'Beta_Cell', 'Protocol_Type', ['RID'],
            constraint_names=[('Beta_Cell', 'Protocol_Protocol_Type_FKey')],
        comment='Must be a protocol type.',
    ),
]


visible_columns = \
{'*': ['RID', 'Name', ['Beta_Cell', 'Protocol_Protocol_Type_FKey'],
       {'aggregate': 'array',
        'comment': 'Additive used in protocol step',
        'entity': True,
        'markdown_name': 'Additive',
        'source': [{'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   {'outbound': ['Beta_Cell',
                                 'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                   'RID']},
       {'aggregate': 'array',
        'comment': 'Additive used in protocol step',
        'entity': True,
        'markdown_name': 'Concentration',
        'source': [{'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   'Additive_Concentration']},
       {'aggregate': 'array',
        'source': [{'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'Duration'],
        'ux_mode': 'choices'},
       'Description'],
 'filter': {'and': [{'source': 'RID'},
                    {'source': {'outbound': ['Beta_Cell',
                                             'Protocol_Protocol_Type_FKey']}},
                    {'aggregate': 'array',
                     'comment': 'Additive used in protocol step',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                'RID']},
                    {'aggregate': 'array',
                     'comment': 'Additive used in protocol step',
                     'entity': True,
                     'markdown_name': 'Concentration',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                'Additive_Concentration'],
                     'ux_mode': 'choices'},
                    {'aggregate': 'array',
                     'markdown_name': 'Duration',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                'Duration'],
                     'ux_mode': 'choices'},
                    'Description']}}

visible_foreign_keys = \
{'*': [['Beta_Cell', 'Protocol_Step_Protocol_FKey'],
       ['isa', 'experiment_protocol_fkey'], ['isa', 'biosample_protocol_fkey'],
       ['isa', 'specimen_protocol_fkey'], ['isa', 'cell_line_protocol_fkey']]}

table_comment = \
'Table containing names of Beta Cell protocols'

table_display = \
{'row_name': {'row_markdown_pattern': '{{#RID}}Pr:{{RID}}{{/RID}} - {{Name}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Description': 'A description of the protocol.',
 'Name': 'The name for this protocol.',
 'Type': 'The type of object for which this protocol is used.'}

column_annotations = \
{}



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
