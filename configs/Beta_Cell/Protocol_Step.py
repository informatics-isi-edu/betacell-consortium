import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Protocol_Step'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Description', em.builtin_types['markdown'],
    ),
    em.Column.define('Step_Number', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('Protocol', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('Start_Time', em.builtin_types['int4'],
        comment='Time in minutes from the start of the protocol when this step should start',
    ),
    em.Column.define('Duration', em.builtin_types['int4'],
        comment='Length in time in minutes over which this protocol step takes place',
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'Protocol_Step_RIDkey1')],
    ),
    em.Key.define(['Step_Number', 'Protocol'],
                   constraint_names=[('Beta_Cell', 'Protocol_Step_Key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Protocol'],
            'Beta_Cell', 'Protocol', ['RID'],
            constraint_names=[('Beta_Cell', 'Protocol_Step_Protocol_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns = \
{'*': [{'source': 'RID'}, {'source': 'Name'},
       {'source': [{'outbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   'RID']},
       {'source': 'Step_Number'},
       {'source': [{'outbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']},
                   {'outbound': ['Beta_Cell', 'Protocol_Protocol_Type_FKey']},
                   'RID']},
       'Start_Time', 'Duration',
       {'aggregate': 'array',
        'comment': 'Additive used in protocol step',
        'entity': True,
        'markdown_name': 'Additive',
        'source': [{'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   {'outbound': ['Beta_Cell',
                                 'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                   'RID']},
       {'aggregate': 'array',
        'comment': 'Additive used in protocol step',
        'entity': True,
        'markdown_name': 'Concentration',
        'source': [{'inbound': ['Beta_Cell',
                                'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                   'Additive_Concentration']},
       {'source': 'Description'}],
 'filter': {'and': [{'source': 'RID'}, {'source': 'Name'},
                    {'source': [{'outbound': ['Beta_Cell',
                                              'Protocol_Step_Protocol_FKey']},
                                'RID']},
                    {'source': [{'outbound': ['Beta_Cell',
                                              'Protocol_Step_Protocol_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Protocol_Protocol_Type_FKey']},
                                'RID']},
                    {'aggregate': 'array',
                     'comment': 'Additive used in protocol step',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                'RID']},
                    {'aggregate': 'array',
                     'comment': 'Concentration in mM of additive used in '
                                'protocol step',
                     'entity': True,
                     'markdown_name': 'Concentration',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                'Additive_Concentration'],
                     'ux_mode': 'choices'},
                    {'source': ['Duration'], 'ux_mode': 'choices'},
                    {'entity': False,
                     'source': 'Step_Number',
                     'ux_mode': 'choices'},
                    {'source': 'Description'}]}}

visible_foreign_keys = {}
table_comment = \
'Defines a single step in a protocol'

table_display = \
{'row_name': {'row_markdown_pattern': '{{#Protocol}}Pr:{{Protocol}}{{/Protocol}}{{#Step_Number}}.{{Step_Number}}{{/Step_Number}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Duration': 'Length in time in minutes over which this protocol step takes '
             'place',
 'Start_Time': 'Time in minutes from the start of the protocol when this step '
               'should start'}

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
