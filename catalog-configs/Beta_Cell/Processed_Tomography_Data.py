import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Processed_Tomography_Data'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Processed_Tomography_Data_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Process': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_process_FKey.rowName}}}'
            }
        }
    },
    'File_Type': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_File_Type_FKey.rowName}}}'
            }
        }
    },
    'filename': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            },
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            },
            'markdown_pattern': 'Filename'
        }
    },
    'url': {
        chaise_tags.asset: {
            'filename_column': 'filename',
            'byte_count_column': 'length',
            'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{filename}}}',
            'md5': 'md5'
        },
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            },
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            }
        }
    },
    'length': {
        'tag:isrd.isi.edu,2016:collumn-display': {
            'markdown_name': 'Length'
        }
    },
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Processed_Tomography_Data_Owner_Fkey.values._display_name}}}'
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
        'Process', em.builtin_types['text'], annotations=column_annotations['Process'],
    ),
    em.Column.define('Data_Type', em.builtin_types['text'],
                     ),
    em.Column.define(
        'File_Type',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['File_Type'],
    ),
    em.Column.define('Biosample', em.builtin_types['text'],
                     ),
    em.Column.define(
        'filename',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['filename'],
    ),
    em.Column.define(
        'url', em.builtin_types['text'], nullok=False, annotations=column_annotations['url'],
    ),
    em.Column.define(
        'length',
        em.builtin_types['int8'],
        nullok=False,
        annotations=column_annotations['length'],
    ),
    em.Column.define('md5', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    'filter': {
        'and': [
            {
                'source': 'RID',
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey']
                    }, 'RID'
                ],
                'markdown_name': 'Dataset'
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                    }, {
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
                'comment': 'Additives used to treat the cell line for the experiment',
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
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
                        'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
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
                'aggregate': 'array'
            },
            {
                'comment': 'Duration in minutes of additive applied to cell line in ',
                'markdown_name': 'Duration',
                'entity': True,
                'ux_mode': 'choices',
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, 'Duration'
                ],
                'aggregate': 'array'
            }, {
                'source': 'filename',
                'open': False,
                'markdown_name': 'File Name',
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Anatomy_FKey']
                    }, 'id'
                ],
                'open': True,
                'markdown_name': 'Anatomy',
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey']
                    }, 'id'
                ],
                'open': True,
                'markdown_name': 'File Type',
                'entity': True
            }
        ]
    },
    'entry': [
        'RID',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Owner_Fkey']
            }, 'id']
        },
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey']
                }, 'RID'
            ],
            'markdown_name': 'Dataset'
        }, ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey'],
        ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'],
        ['Beta_Cell', 'Processed_Tomography_Data_Output_Type_FKey'],
        ['Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey'], 'url'
    ],
    'detailed': [
        ['Beta_Cell', 'Processed_Tomography_Data_Key'], 'RCB', 'Owner',
        ['Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey'],
        ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey'],
        ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'],
        ['Beta_Cell', 'Processed_Tomography_Data_Output_Type_FKey'],
        ['Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey'], 'length', 'md5'
    ],
    'compact': [
        ['Beta_Cell', 'Processed_Tomography_Data_Key'], 'RCB', 'Owner', 'Biosample', 'url',
        'File_Type', ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'], 'length'
    ]
}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    'table_display': {
        'row_name': {
            'row_markdown_pattern': '{{{filename}}}'
        }
    },
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'None'
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
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['File_Type'],
        'vocab',
        'file_type_terms', ['id'],
        constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Dataset'],
        'Beta_Cell',
        'Dataset', ['RID'],
        constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey')],
        annotations={
            chaise_tags.display: {},
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.Processed_Tomography_Data_Biosample_FKey.values._Dataset}}}'
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
        ['Process'],
        'isa',
        'process', ['RID'],
        constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Process_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Biosample', 'Dataset'],
        'Beta_Cell',
        'Biosample', ['RID', 'Dataset'],
        constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Dataset_RID_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Ensure that the dataset for the file is the same as for the biosample',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Biosample'],
        'Beta_Cell',
        'Biosample', ['RID'],
        constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey')],
        annotations={chaise_tags.foreign_key: {
            'domain_filter_pattern': 'Dataset={{{_Dataset}}}'
        }},
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

