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

table_name = 'Biosample'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Biosample_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Sample_Position': {},
    'Specimen': {},
    'Specimen_Type': {},
    'Experiment': {},
    'Protocol': {},
    'Container_Id': {},
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Biosample_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Sample_Position': 'Position in the capillary where the sample is located.',
    'Specimen': 'Biological material used for the biosample.',
    'Specimen_Type': 'Method by which specimen is prepared.',
    'Experiment': 'Experiment in which this biosample is used',
    'Protocol': 'Biosample protocol.',
    'Container_Id': 'ID number of the container with the biosample. Is a number'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('Dataset', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('Summary', em.builtin_types['text'],
                     ),
    em.Column.define('Collection_Date', em.builtin_types['date'],
                     ),
    em.Column.define(
        'Sample_Position', em.builtin_types['int2'], comment=column_comment['Sample_Position'],
    ),
    em.Column.define('Specimen', em.builtin_types['text'], comment=column_comment['Specimen'],
                     ),
    em.Column.define(
        'Specimen_Type', em.builtin_types['text'], comment=column_comment['Specimen_Type'],
    ),
    em.Column.define(
        'Experiment', em.builtin_types['ermrest_rid'], comment=column_comment['Experiment'],
    ),
    em.Column.define('Protocol', em.builtin_types['text'], comment=column_comment['Protocol'],
                     ),
    em.Column.define(
        'Container_Id', em.builtin_types['int2'], comment=column_comment['Container_Id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

display = {}

visible_columns = {
    '*': [
        ['Beta_Cell', 'Biosample_Key'], 'RCB', 'Owner',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Dataset_FKey']
            }, 'RID'],
            'markdown_name': 'Dataset'
        }, 'Summary', {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
            }, 'RID']
        },
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
            }, 'RID'],
            'markdown_name': 'Experiment'
        },
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
                }, 'name'
            ],
            'markdown_name': 'Cell Line'
        },
        {
            'entity': True,
            'source': [
                {
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
            'comment': 'Compound used to treat the cell line for the Experiment',
            'aggregate': 'array',
            'markdown_name': 'Additive'
        },
        {
            'entity': True,
            'source': [
                {
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
            'aggregate': 'array',
            'markdown_name': 'Concentration'
        },
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, 'Duration'
            ],
            'comment': 'Duration in minutes of additive applied to cell line in ',
            'aggregate': 'array',
            'markdown_name': 'Duration'
        },
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Biosample_Protocol_FKey']
                }, {
                    'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                }, {
                    'outbound': ['Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey']
                }, 'RID'
            ],
            'comment': 'Part of the cell from which the biosample was taken',
            'markdown_name': 'Cellular Location'
        }, ['Beta_Cell', 'Biosample_Specimen_Type_FKey'], 'Container_Id', 'Sample_Position',
        'Collection_Date'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Owner_Fkey']
            }, 'id']
        },
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Dataset_FKey']
            }, 'RID'],
            'markdown_name': 'Dataset'
        },
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
            }, 'RID'],
            'markdown_name': 'Experiment'
        }, ['Beta_Cell', 'Biosample_Protocol_FKey'], ['Beta_Cell', 'Biosample_Specimen_FKey'],
        ['Beta_Cell', 'Biosample_Specimen_Type_FKey'], 'Container_Id',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Protocol_FKey']
            }, 'Description']
        }, 'Sample_Position', 'collection_date'
    ],
    'filter': {
        'and': [
            {
                'entity': True,
                'source': 'RID'
            }, {
                'source': [{
                    'outbound': ['Beta_Cell', 'Biosample_Dataset_FKey']
                }, 'RID']
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
                    }, 'name'
                ],
                'markdown_name': 'Cell Line'
            },
            {
                'entity': True,
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Biosample_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey']
                    }, 'name'
                ],
                'comment': 'Part of the cell from which the biosample was taken',
                'markdown_name': 'Cellular Location'
            },
            {
                'entity': True,
                'source': [
                    {
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
                'comment': 'Additives used to treat the cell line for the Experiment',
                'aggregate': 'array',
                'markdown_name': 'Additive'
            },
            {
                'entity': True,
                'source': [
                    {
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
                'aggregate': 'array',
                'markdown_name': 'Concentration'
            },
            {
                'entity': True,
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, 'Duration'
                ],
                'comment': 'Duration in minutes of additive applied to cell line in ',
                'ux_mode': 'choices',
                'aggregate': 'array',
                'markdown_name': 'Duration'
            }, ['Beta_Cell', 'Biosample_Specimen_Type_FKey'],
            {
                'source': [{
                    'inbound': ['isa', 'mesh_data_biosample_fkey']
                }, 'url']
            }, {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                    }, 'RID'
                ]
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                    }, 'RID'
                ]
            }, {
                'source': [{
                    'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
                }, 'RID']
            }, {
                'entity': True,
                'source': 'Container_Id',
                'ux_mode': 'choices'
            }
        ]
    }
}

visible_foreign_keys = {
    '*': [
        {
            'source': [{
                'inbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
            }, 'RID']
        },
        {
            'source': [
                {
                    'inbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                }, 'RID'
            ]
        }, {
            'source': [{
                'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
            }, 'RID']
        }, ['viz', 'model_biosample_fkey']
    ]
}

table_display = {
    'row_name': {
        'row_markdown_pattern': '{{RID}}{{#local_identifier}} {{Container_Id}}{{/local_identifier}}'
    }
}

table_alternatives = {}

export = {
    'templates': [
        {
            'name': 'default',
            'outputs': [
                {
                    'source': {
                        'api': 'entity',
                        'table': 'Beta_Cell:Biosample'
                    },
                    'destination': {
                        'name': 'Biosample',
                        'type': 'csv'
                    }
                },
                {
                    'source': {
                        'api': 'attribute',
                        'path': 'url:=URL,md5:=MD5,length:=Byte_Count',
                        'table': 'Beta_Cell:XRay_Tomography_Data'
                    },
                    'destination': {
                        'name': 'MRC',
                        'type': 'fetch'
                    }
                },
                {
                    'source': {
                        'api': 'attribute',
                        'path': 'url:=URL,md5:=MD5,length:=Byte_Count',
                        'table': 'Beta_Cell:Processed_Tomography_Data'
                    },
                    'destination': {
                        'name': 'processed_data',
                        'type': 'fetch'
                    }
                },
                {
                    'source': {
                        'api': 'attribute',
                        'path': 'url',
                        'table': 'isa:mesh_data'
                    },
                    'destination': {
                        'name': 'OBJS',
                        'type': 'fetch'
                    }
                }
            ],
            'format_name': 'BDBag (Holey)',
            'format_type': 'BAG'
        },
        {
            'name': 'default',
            'outputs': [
                {
                    'source': {
                        'api': 'entity',
                        'table': 'Beta_Cell:Biosample'
                    },
                    'destination': {
                        'name': 'Biosample',
                        'type': 'csv'
                    }
                },
                {
                    'source': {
                        'api': 'attribute',
                        'path': 'url:=URL',
                        'table': 'Beta_Cell:XRay_Tomography_Data'
                    },
                    'destination': {
                        'name': 'MRC',
                        'type': 'download'
                    }
                },
                {
                    'source': {
                        'api': 'attribute',
                        'path': 'url:=URL',
                        'table': 'Beta_Cell:Processed_Tomography_Data'
                    },
                    'destination': {
                        'name': 'processed_data',
                        'type': 'download'
                    }
                },
                {
                    'source': {
                        'api': 'attribute',
                        'path': 'URL',
                        'table': 'isa:mesh_data'
                    },
                    'destination': {
                        'name': 'OBJS',
                        'type': 'download'
                    }
                }
            ],
            'format_name': 'BDBag',
            'format_type': 'BAG'
        }
    ]
}

table_annotations = {
    chaise_tags.export: export,
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
        ['Dataset', 'RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Dataset_RID_Key')],
        annotations={chaise_tags.display: {}},
    ),
    em.Key.define(
        ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Key')],
        annotations={chaise_tags.display: {}},
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Experiment', 'Dataset'],
        'Beta_Cell',
        'Experiment', ['RID', 'Dataset'],
        constraint_names=[('Beta_Cell', 'Biosample_Experiment_Dataset_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Specimen_Type'],
        'vocab',
        'specimen_type_terms', ['id'],
        constraint_names=[('Beta_Cell', 'Biosample_Specimen_Type_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a valid reference to a specimen type.',
    ),
    em.ForeignKey.define(
        ['Specimen'],
        'Beta_Cell',
        'Specimen', ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Specimen_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol', ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Dataset'],
        'Beta_Cell',
        'Dataset', ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Dataset_FKey')],
        annotations={
            chaise_tags.display: {},
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.Biosample_Experiment_FKey.values._Dataset}}}'
            }
        },
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Experiment'],
        'Beta_Cell',
        'Experiment', ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Experiment_FKey')],
        annotations={
            chaise_tags.display: {},
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'Dataset={{{_Dataset}}}'
            }
        },
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Biosample_RCB_Fkey')],
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Biosample_Owner_Fkey')],
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

