import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_name = 'XRay_Tomography_Data'

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
                'markdown_pattern': '{{{$fkeys.Beta_Cell.XRay_Tomography_Data_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Dataset': {},
    'Description': {},
    'File_Type': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.XRay_Tomography_Data_File_Type_FKey.rowName}}}'
            }
        }
    },
    'Submitted_On': {},
    'File_Id': {},
    'Biosample': {},
    'length': {
        'tag:isrd.isi.edu,2016:collumn-display': {
            'markdown_name': 'Length'
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
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.XRay_Tomography_Data_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Dataset': 'None',
    'Description': 'None',
    'File_Type': 'None',
    'Submitted_On': 'None',
    'File_Id': 'None',
    'Biosample': 'Biosample from which this X Ray Tomography data was obtained'
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
    em.Column.define(
        'Dataset',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Dataset'],
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
        comment=column_comment['Description'],
    ),
    em.Column.define(
        'File_Type',
        em.builtin_types['text'],
        annotations=column_annotations['File_Type'],
        comment=column_comment['File_Type'],
    ),
    em.Column.define(
        'Submitted_On',
        em.builtin_types['timestamptz'],
        comment=column_comment['Submitted_On'],
    ),
    em.Column.define(
        'File_Id', em.builtin_types['int4'], comment=column_comment['File_Id'],
    ),
    em.Column.define(
        'Biosample',
        em.builtin_types['ermrest_rid'],
        comment=column_comment['Biosample'],
    ),
    em.Column.define('md5', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define(
        'length',
        em.builtin_types['int8'],
        nullok=False,
        annotations=column_annotations['length'],
    ),
    em.Column.define(
        'url',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['url'],
    ),
    em.Column.define(
        'filename',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['filename'],
    ),
    em.Column.define(
        'Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
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
                        'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Dataset_FKey']
                    }, 'RID'
                ],
                'markdown_name': 'Dataset'
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
                    }, {
                        'outbound': ['isa', 'Cell_Line_Cell_Line_Terms_FKey']
                    }, 'name'
                ],
                'markdown_name': 'Cell Line'
            },
            {
                'comment': 'Additives used to treat the cell line for the experiment',
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    },
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
                'comment': 'Concentration of additive applied to cell line in mM',
                'markdown_name': 'Concentration',
                'entity': True,
                'ux_mode': 'choices',
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    },
                    {
                        'inbound': [
                            'Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                        ]
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
                        'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                    }, {
                        'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                    }, 'Duration'
                ],
                'aggregate': 'array'
            },
            {
                'source': 'filename',
                'open': False,
                'markdown_name': 'File Name',
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Anatomy_FKey']
                    }, 'id'
                ],
                'open': True,
                'markdown_name': 'Anatomy',
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey']
                    }, 'id'
                ],
                'open': True,
                'markdown_name': 'File Type',
                'entity': True
            },
            {
                'source': 'submitted_on',
                'open': False,
                'markdown_name': 'Submitted On',
                'entity': True
            }
        ]
    },
    'entry': [
        'RID', 'RCB',
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Owner_Fkey']
                }, 'id'
            ]
        }, ['Beta_Cell', 'XRay_Tomography_Data_Dataset_FKey'],
        ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey'], 'Description', 'url',
        ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'], 'filename',
        ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'], 'length', 'md5',
        'submitted_on'
    ],
    '*': [
        ['Beta_Cell', 'XRay_Tomography_Data_Key'], 'RCB',
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Owner_Fkey']
                }, 'id'
            ]
        },
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Dataset_FKey']
                }, 'RID'
            ],
            'markdown_name': 'Dataset'
        },
        {
            'source': [
                {
                    'outbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                }, 'RID'
            ],
            'markdown_name': 'Biosample'
        }, 'filename', 'Description',
        ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'], 'length', 'submitted_on'
    ]
}

visible_foreign_keys = {
    'detailed': [['isa', 'mesh_data_derived_from_fkey']],
    'entry': [['isa', 'mesh_data_derived_from_fkey']]
}

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
table_comment = 'Table to hold X-Ray Tomography MRC files.'
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['RID', 'Dataset'],
        constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Dataset_RID_Key')],
        comment='RID and dataset must be distinct.',
    ),
    em.Key.define(
        ['RID'], constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_RIDkey1')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Dataset'],
        'Beta_Cell',
        'Dataset', ['RID'],
        constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Dataset_FKey')],
        annotations={
            'tag:misd.isi.edu,2015:display': {},
            'tag:isrd.isi.edu,2016:foreign-key': {
                'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.XRay_Tomography_Data_Biosample_FKey.values._Dataset}}}'
            }
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
        comment='Must be a valid reference to a dataset.',
    ),
    em.ForeignKey.define(
        ['Biosample'],
        'Beta_Cell',
        'Biosample', ['RID'],
        constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey')],
        annotations={
            'tag:isrd.isi.edu,2016:foreign-key': {
                'domain_filter_pattern': 'Dataset={{{_Dataset}}}'
            }
        },
    ),
    em.ForeignKey.define(
        ['Dataset', 'Biosample'],
        'Beta_Cell',
        'Biosample', ['Dataset', 'RID'],
        constraint_names=[('Beta_Cell', 'XRay_Tomography_Dataset_RID_FKey')],
        comment='Ensure that the dataset for the file is the same as for the biosample',
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

