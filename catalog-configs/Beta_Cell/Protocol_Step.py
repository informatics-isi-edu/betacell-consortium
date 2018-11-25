import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_name = 'Protocol_Step'

schema_name = 'Beta_Cell'

groups = AttrDict(
    {
        'admins': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
        'modelers': 'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
        'curators': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
        'writers': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'readers': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
        'isrd': 'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
    }
)

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Protocol_Step_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Start_Time': {},
    'Duration': {},
    'Cellular_Location': {},
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Protocol_Step_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Start_Time': 'Time in minutes from the start of the protocol when this step should start',
    'Duration': 'Length in time in minutes over which this protocol step takes place',
    'Cellular_Location': 'Component of the cell that was extracted.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,
                     ),
    em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,
                     ),
    em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,
                     ),
    em.Column.define(
        'RCB', em.builtin_types['ermrest_rcb'], annotations=column_annotations['RCB'],
    ),
    em.Column.define('RMB', em.builtin_types['ermrest_rmb'],
                     ),
    em.Column.define('Description', em.builtin_types['markdown'],
                     ),
    em.Column.define('Step_Number', em.builtin_types['int4'], nullok=False,
                     ),
    em.Column.define('Protocol', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define(
        'Start_Time', em.builtin_types['int4'], comment=column_comment['Start_Time'],
    ),
    em.Column.define(
        'Duration', em.builtin_types['int4'], comment=column_comment['Duration'],
    ),
    em.Column.define(
        'Cellular_Location',
        em.builtin_types['text'],
        comment=column_comment['Cellular_Location'],
    ),
    em.Column.define(
        'Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
    ),
]

visible_columns = {
    'filter': {
        'and': [
            {
                'source': 'RID'
            }, {
                'source': 'Name'
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, 'RID'
                ]
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Protocol_Protocol_Type_FKey']
                    }, 'RID'
                ]
            },
            {
                'source': [
                    {
                        'outbound': [
                            'Beta_Cell, Protocol_Step_Cellular_Location_Term_FKey'
                        ]
                    }, 'id'
                ]
            },
            {
                'comment': 'Additive used in protocol step',
                'source': [
                    {
                        'inbound': [
                            'Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                        ]
                    },
                    {
                        'outbound': [
                            'Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey'
                        ]
                    }, 'RID'
                ],
                'aggregate': 'array',
                'markdown_name': 'Additive',
                'entity': True
            },
            {
                'comment': 'Concentration in mM of additive used in protocol step',
                'markdown_name': 'Concentration',
                'entity': True,
                'ux_mode': 'choices',
                'source': [
                    {
                        'inbound': [
                            'Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                        ]
                    }, 'Additive_Concentration'
                ],
                'aggregate': 'array'
            }, {
                'ux_mode': 'choices',
                'source': ['Duration']
            }, {
                'ux_mode': 'choices',
                'source': 'Step_Number',
                'entity': False
            }, {
                'source': 'Description'
            }
        ]
    },
    '*': [
        {
            'source': 'RID'
        }, 'RCB',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Protocol_Step_Owner_Fkey']
            }, 'id']
        }, {
            'source': 'Name'
        }, {
            'source': [{
                'outbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            }, 'RID']
        }, {
            'source': 'Step_Number'
        },
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Protocol_Protocol_Type_FKey']
                }, 'RID'
            ]
        }, 'Start_Time', 'Duration',
        {
            'source': [
                {
                    'outbound': [
                        'Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey'
                    ]
                }, 'id'
            ]
        },
        {
            'comment': 'Additive used in protocol step',
            'source': [
                {
                    'inbound': [
                        'Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                    ]
                },
                {
                    'outbound': [
                        'Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey'
                    ]
                }, 'RID'
            ],
            'aggregate': 'array',
            'markdown_name': 'Additive',
            'entity': True
        },
        {
            'comment': 'Additive concentration used in protocol step',
            'source': [
                {
                    'inbound': [
                        'Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                    ]
                }, 'Additive_Concentration'
            ],
            'aggregate': 'array',
            'markdown_name': 'Concentration',
            'entity': True
        }, {
            'source': 'Description'
        }
    ]
}

visible_foreign_keys = {
    '*': [
        ['Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey'],
        {
            'source': [
                {
                    'inbound': [
                        'Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                    ]
                }, 'RID'
            ]
        }
    ]
}

table_display = {
    'row_name': {
        'row_markdown_pattern': '{{#Protocol}}{{$fkeys.Beta_Cell.Protocol_Step_Protocol_FKey.rowName}}{{/Protocol}}{{#Step_Number}} (Step {{Step_Number}}){{/Step_Number}}'
    }
}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'Defines a single step in a protocol'
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['Protocol', 'Step_Number'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Key')],
    ),
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Protocol_Step_RIDkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol', ['RID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Protocol_FKey')],
    ),
]

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True
)


def main(
    skip_args=False,
    mode='annotations',
    replace=False,
    server='pbcconsortium.isrd.isi.edu',
    catalog_id=1
):

    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(
            server, catalog_id, is_table=True
        )
    update_catalog.update_table(
        mode, replace, server, catalog_id, schema_name, table_name, table_def,
        column_defs, key_defs, fkey_defs, table_annotations, table_acls,
        table_acl_bindings, table_comment, column_annotations, column_acls,
        column_acl_bindings, column_comment
    )


if __name__ == "__main__":
    main()

