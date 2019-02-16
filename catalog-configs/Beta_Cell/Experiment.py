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
    '*': [
        'RID', 'RCB', 'Owner', ['Beta_Cell', 'Experiment_Dataset_FKey'],
        ['Beta_Cell', 'Experiment_Protocol_FKey'], ['Beta_Cell', 'Experiment_Experiment_Type_FKey'],
        {
            'open': True,
            'entity': True,
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
            'aggregate': 'array_d',
            'markdown_name': 'Cell Line'
        },
        {
            'entity': True,
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
            'comment': 'Additives used to treat the specimens for the experiment',
            'aggregate': 'array_d',
            'markdown_name': 'Additive'
        },
        {
            'entity': True,
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
            'comment': 'Concentration of additive applied to cell line in mM',
            'ux_mode': 'choices',
            'aggregate': 'array_d',
            'markdown_name': 'Concentration'
        },
        {
            'entity': True,
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
            'comment': 'Duration in minutes of additive applied to cell line in ',
            'ux_mode': 'choices',
            'aggregate': 'array_d',
            'markdown_name': 'Duration'
        }, 'description'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Experiment_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Experiment_Dataset_FKey'], ['Beta_Cell', 'Experiment_Protocol_fkey'],
        ['Beta_Cell', 'Experiment_Experiment_Type_FKey'], 'description', 'collection_date'
    ],
    'filter': {
        'and': [
            {
                'entity': True,
                'source': 'RID'
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
                'open': True,
                'entity': True,
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
                'aggregate': 'array_d',
                'markdown_name': 'Cell Line'
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
                'entity': True,
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
                'comment': 'Additives used to treat the specimens for the experiment',
                'aggregate': 'array_d',
                'markdown_name': 'Additive'
            },
            {
                'entity': True,
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
                'comment': 'Concentration of additive applied to cell line in mM',
                'ux_mode': 'choices',
                'aggregate': 'array_d',
                'markdown_name': 'Concentration'
            },
            {
                'entity': True,
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
                'comment': 'Duration in minutes of additive applied to cell line in ',
                'ux_mode': 'choices',
                'aggregate': 'array_d',
                'markdown_name': 'Duration'
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
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.table_alternatives: table_alternatives,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = None

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
    em.Key.define(
        ['Dataset', 'RID'], constraint_names=[('Beta_Cell', 'Experiment_RID_Dataset_Key')],
    ),
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Experiment_RID_Key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Experiment_RCB_Fkey')],
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
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Experiment_Owner_Fkey')],
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

