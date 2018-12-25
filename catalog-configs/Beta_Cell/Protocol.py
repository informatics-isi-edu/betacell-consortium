import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

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
                'comment': 'Additive used in protocol step',
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey']
                    }, 'RID'
                ],
                'aggregate': 'array',
                'markdown_name': 'Additive',
                'entity': True
            },
            {
                'comment': 'Additive used in protocol step',
                'markdown_name': 'Concentration',
                'entity': True,
                'ux_mode': 'choices',
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, 'Additive_Concentration'
                ],
                'aggregate': 'array'
            },
            {
                'ux_mode': 'choices',
                'source': [{
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, 'Duration'],
                'aggregate': 'array',
                'markdown_name': 'Duration'
            }, 'Description'
        ]
    },
    '*': [
        'RID', 'RCB', {
            'source': [{
                'outbound': ['Beta_Cell', 'Protocol_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Protocol_Protocol_Type_FKey'],
        {
            'comment': 'Additive used in protocol step',
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey']
                }, 'RID'
            ],
            'aggregate': 'array',
            'markdown_name': 'Additive',
            'entity': True
        },
        {
            'comment': 'Additive used in protocol step',
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, 'Additive_Concentration'
            ],
            'aggregate': 'array',
            'markdown_name': 'Concentration',
            'entity': True
        },
        {
            'ux_mode': 'choices',
            'source': [{
                'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            }, 'Duration'],
            'aggregate': 'array'
        }, 'Description'
    ]
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
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'Table containing names of Beta Cell protocols'
table_acls = {}
table_acl_bindings = {
    'self_service_creator': {
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    },
    'self_service_owner': {
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    }
}

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Protocol_RIDkey1')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Protocol_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Protocol_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
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
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_table=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)

