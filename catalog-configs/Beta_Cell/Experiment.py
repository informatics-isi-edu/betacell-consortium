import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Experiment'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Experiment_Type': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Experiment_Type_FKey.rowName}}}'
            }
        }
    },
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
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('Dataset', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define(
        'Experiment_Type',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['Experiment_Type'],
    ),
    em.Column.define(
        'Protocol', em.builtin_types['text'], annotations=column_annotations['Protocol'],
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

display = {}

visible_columns = {
    'filter': {
        'and': [
            {
                'source': 'RID',
                'entity': True
            }, {
                'source': [{
                    'outbound': ['Beta_Cell', 'Experiment_Dataset_FKey']
                }, 'RID']
            }, {
                'source': [{
                    'outbound': ['Beta_Cell', 'Experiment_Protocol_FKey']
                }, 'RID']
            }, {
                'source': [{
                    'outbound': ['Beta_Cell', 'Experiment_Experiment_Type_FKey']
                }, 'RID']
            },
            {
                'aggregate': 'array_d',
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Cell_Line_cell_Line_Terms_fkey']
                    }, 'name'
                ],
                'open': True,
                'markdown_name': 'Cell Line',
                'entity': True
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_cellular_location_terms_fkey']
                    }, 'name'
                ],
                'markdown_name': 'Cellular Location'
            },
            {
                'comment': 'Additives used to treat the specimens for the experiment',
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey']
                    }, 'RID'
                ],
                'aggregate': 'array_d',
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
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                    }, 'Additive_Concentration'
                ],
                'aggregate': 'array_d'
            },
            {
                'comment': 'Duration in minutes of additive applied to cell line in ',
                'markdown_name': 'Duration',
                'entity': True,
                'ux_mode': 'choices',
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, 'Duration'
                ],
                'aggregate': 'array_d'
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                    }, 'RID'
                ]
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                    }, 'RID'
                ]
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
                    }, 'RID'
                ]
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                    }, {
                        'inbound': ['isa', 'mesh_data_biosample_fkey']
                    }, 'RID'
                ]
            }
        ]
    },
    'entry': [
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Experiment_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Experiment_Dataset_FKey'], ['Beta_Cell', 'Experiment_Protocol_fkey'],
        ['Beta_Cell', 'Experiment_Experiment_Type_FKey'], 'description', 'collection_date'
    ],
    '*': [
        'RID', 'RCB', 'Owner', ['Beta_Cell', 'Experiment_Dataset_FKey'],
        ['Beta_Cell', 'Experiment_Protocol_FKey'], ['Beta_Cell', 'Experiment_Experiment_Type_FKey'],
        {
            'aggregate': 'array_d',
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                }, {
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
            'comment': 'Additives used to treat the specimens for the experiment',
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey']
                }, 'RID'
            ],
            'aggregate': 'array_d',
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
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey']
                }, 'Additive_Concentration'
            ],
            'aggregate': 'array_d'
        },
        {
            'comment': 'Duration in minutes of additive applied to cell line in ',
            'markdown_name': 'Duration',
            'entity': True,
            'ux_mode': 'choices',
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, 'Duration'
            ],
            'aggregate': 'array_d'
        }, 'description'
    ]
}

visible_foreign_keys = {
    '*': [
        ['viz', 'model_experiment_fkey'],
        {
            'source': [{
                'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
            }, 'RID']
        },
        {
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                }, 'RID'
            ]
        },
        {
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                }, 'RID'
            ]
        },
        {
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
                }, 'RID'
            ]
        },
        {
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                }, {
                    'inbound': ['isa', 'mesh_data_biosample_fkey']
                }, 'RID'
            ]
        }
    ]
}

table_display = {
    'row_name': {
        'row_markdown_pattern': '{{RID}}{{#local_identifier}} - {{local_identifier}} {{/local_identifier}}{{#biosample_summary}} - {{biosample_summary}}{{/biosample_summary}}'
    }
}

table_alternatives = {}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.display: display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.table_alternatives: table_alternatives,
}
table_comment = None
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

key_defs = [
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Experiment_RID_Key')],
                  ),
    em.Key.define(
        ['RID', 'Dataset'], constraint_names=[('Beta_Cell', 'Experiment_RID_Dataset_Key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Experiment_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Experiment_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol', ['RID'],
        constraint_names=[('Beta_Cell', 'Experiment_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Dataset'],
        'Beta_Cell',
        'Dataset', ['RID'],
        constraint_names=[('Beta_Cell', 'Experiment_Dataset_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Experiment_Type'],
        'vocab',
        'experiment_type_terms', ['RID'],
        constraint_names=[('Beta_Cell', 'Experiment_Experiment_Type_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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

