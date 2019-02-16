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

table_name = 'Protocol'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Protocol_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Description': {},
    'Type': {},
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Protocol_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Description': 'A description of the protocol.',
    'Type': 'The type of object for which this protocol is used.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Description', em.builtin_types['markdown'], comment=column_comment['Description'],
    ),
    em.Column.define(
        'Type', em.builtin_types['text'], nullok=False, comment=column_comment['Type'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', 'RCB', {
            'source': [{
                'outbound': ['Beta_Cell', 'Protocol_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Protocol_Protocol_Type_FKey'],
        {
            'entity': True,
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
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
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, 'Additive_Concentration'
            ],
            'comment': 'Additive used in protocol step',
            'aggregate': 'array',
            'markdown_name': 'Concentration'
        },
        {
            'source': [{
                'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            }, 'Duration'],
            'ux_mode': 'choices',
            'aggregate': 'array'
        }, 'Description'
    ],
    'filter': {
        'and': [
            {
                'source': 'RID'
            }, {
                'source': [{
                    'outbound': ['Beta_Cell', 'Protocol_Protocol_Type_FKey']
                }, 'RID']
            },
            {
                'entity': True,
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
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
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, 'Additive_Concentration'
                ],
                'comment': 'Additive used in protocol step',
                'ux_mode': 'choices',
                'aggregate': 'array',
                'markdown_name': 'Concentration'
            },
            {
                'source': [{
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, 'Duration'],
                'ux_mode': 'choices',
                'aggregate': 'array',
                'markdown_name': 'Duration'
            }, 'Description'
        ]
    }
}

visible_foreign_keys = {
    '*': [
        ['Beta_Cell', 'Protocol_Step_Protocol_FKey'], ['Beta_Cell', 'Experiment_Protocol_FKey'],
        ['Beta_Cell', 'Biosample_Protocol_FKey'], ['Beta_Cell', 'Specimen_Protocol_FKey'],
        ['Beta_Cell', 'Cell_Line_Protocol_FKey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{#RID}}Protocol:{{Description}}{{/RID}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Table containing names of Beta Cell protocols'

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

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Protocol_RIDkey1')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['Type'],
        'Beta_Cell',
        'Protocol_Type', ['RID'],
        constraint_names=[('Beta_Cell', 'Protocol_Protocol_Type_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a protocol type.',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Protocol_RCB_Fkey')],
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Protocol_Owner_Fkey')],
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

