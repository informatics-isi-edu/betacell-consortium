import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Specimen'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Specimen_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Description': {},
    'Collection_Date': {},
    'Cell_Line': {},
    'Protocol': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'
            }
        }
    },
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Specimen_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Description': 'Description of the specimen.',
    'Collection_Date': 'Date the specimen was obtained',
    'Cell_Line': 'Cell line used for the specimen.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Description', em.builtin_types['text'], comment=column_comment['Description'],
    ),
    em.Column.define(
        'Collection_Date', em.builtin_types['date'], comment=column_comment['Collection_Date'],
    ),
    em.Column.define('Cell_Line', em.builtin_types['text'], comment=column_comment['Cell_Line'],
                     ),
    em.Column.define(
        'Protocol', em.builtin_types['text'], annotations=column_annotations['Protocol'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    'filter': {
        'and': [
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
                    }, 'name'
                ],
                'open': True,
                'markdown_name': 'Cell Line',
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey']
                    }, 'name'
                ],
                'markdown_name': 'Cellular Location'
            },
            {
                'comment': 'Additive used to treat the cell line for the experiment',
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
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
                'comment': 'Concentration of additive applied to cell line in mM',
                'markdown_name': 'Concentration',
                'entity': True,
                'ux_mode': 'choices',
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, 'Additive_Concentration'
                ],
                'aggregate': 'array'
            },
            {
                'comment': 'Duration in minutes',
                'markdown_name': 'Duration',
                'entity': True,
                'ux_mode': 'choices',
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, 'Duration'
                ],
                'aggregate': 'array'
            }, {
                'source': [{
                    'inbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                }, 'RID']
            }, 'Description', 'Collection_Date'
        ]
    },
    'entry': [
        'RCB', {
            'source': [{
                'outbound': ['Beta_Cell', 'Specimen_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Specimen_Cell_Line_FKey'], ['Beta_Cell', 'Specimen_Protocol_FKey'],
        ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey'], 'Description', 'Collection_Date'
    ],
    '*': [
        'RID', 'RCB', 'Owner', 'Protocol',
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
                }, 'name'
            ],
            'open': True,
            'markdown_name': 'Cell Line',
            'entity': True
        },
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey']
                }, 'name'
            ],
            'markdown_name': 'Cellular Location'
        },
        {
            'comment': 'Additive used to treat the cell line for the experiment',
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
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
            'comment': 'Concentration of additive applied to cell line in mM',
            'markdown_name': 'Concentration',
            'entity': True,
            'ux_mode': 'choices',
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, 'Additive_Concentration'
            ],
            'aggregate': 'array'
        },
        {
            'comment': 'Duration in minutes',
            'markdown_name': 'Duration',
            'entity': True,
            'ux_mode': 'choices',
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, 'Duration'
            ],
            'aggregate': 'array'
        }, 'Description', 'Collection_Date'
    ]
}

visible_foreign_keys = {
    '*': [
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, 'RID'
            ]
        }, {
            'source': [{
                'inbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
            }, 'RID']
        }
    ]
}

table_display = {}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    'table_display': {},
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'Table of biological speciments from which biosamples will be created.'
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

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Specimen_RIDkey1')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Specimen_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Cell_Line'],
        'Beta_Cell',
        'Cell_Line', ['RID'],
        constraint_names=[('Beta_Cell', 'Specimen_Cell_Line_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Specimen_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol', ['RID'],
        constraint_names=[('Beta_Cell', 'Specimen_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
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

