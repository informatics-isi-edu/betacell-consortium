import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pbcconsortium-reader': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'pbcconsortium-curator': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'pbcconsortium-writer': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'pbcconsortium-admin': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'isrd-testers': 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
}

table_name = 'Protocol_Step'

schema_name = 'Beta_Cell'

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
    em.Column.define('Description', em.builtin_types['markdown'],
                     ),
    em.Column.define('Step_Number', em.builtin_types['int4'], nullok=False,
                     ),
    em.Column.define('Protocol', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define(
        'Start_Time', em.builtin_types['int4'], comment=column_comment['Start_Time'],
    ),
    em.Column.define('Duration', em.builtin_types['int4'], comment=column_comment['Duration'],
                     ),
    em.Column.define(
        'Cellular_Location',
        em.builtin_types['text'],
        comment=column_comment['Cellular_Location'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, 'RCB', {
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
                    'outbound': ['Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey']
                }, 'id'
            ]
        },
        {
            'entity': True,
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey']
                }, 'RID'
            ],
            'comment': 'Additive used in protocol step',
            'aggregate': 'array',
            'markdown_name': 'Additive'
        },
        {
            'entity': True,
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, 'Additive_Concentration'
            ],
            'comment': 'Additive concentration used in protocol step',
            'aggregate': 'array',
            'markdown_name': 'Concentration'
        }, {
            'source': 'Description'
        }
    ],
    'filter': {
        'and': [
            {
                'source': 'RID'
            }, {
                'source': 'Name'
            }, {
                'source': [{
                    'outbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, 'RID']
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
                        'outbound': ['Beta_Cell, Protocol_Step_Cellular_Location_Term_FKey']
                    }, 'id'
                ]
            },
            {
                'entity': True,
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey']
                    }, 'RID'
                ],
                'comment': 'Additive used in protocol step',
                'aggregate': 'array',
                'markdown_name': 'Additive'
            },
            {
                'entity': True,
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, 'Additive_Concentration'
                ],
                'comment': 'Concentration in mM of additive used in protocol step',
                'ux_mode': 'choices',
                'aggregate': 'array',
                'markdown_name': 'Concentration'
            }, {
                'source': ['Duration'],
                'ux_mode': 'choices'
            }, {
                'entity': False,
                'source': 'Step_Number',
                'ux_mode': 'choices'
            }, {
                'source': 'Description'
            }
        ]
    }
}

visible_foreign_keys = {
    '*': [
        ['Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey'],
        {
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
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
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Defines a single step in a protocol'

table_acls = {}

table_acl_bindings = {
    'self_service_owner': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Protocol_Step_RIDkey1')],
                  ),
    em.Key.define(
        ['Step_Number', 'Protocol'], constraint_names=[('Beta_Cell', 'Protocol_Step_Key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol', ['RID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Cellular_Location'],
        'vocab',
        'cellular_location_terms', ['id'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Owner_Fkey')],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_RCB_Fkey')],
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


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_table(mode, schema_name, table_def, replace=replace)


if __name__ == "__main__":
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

