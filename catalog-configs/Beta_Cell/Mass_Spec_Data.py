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

table_name = 'Mass_Spec_Data'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Mass_Spec_Data_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Dataset': {},
    'Description': {},
    'File_Type': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Mass_Spec_Data_File_Type_FKey.rowName}}}'
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
            'md5': 'md5',
            'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{filename}}}',
            'filename_column': 'filename',
            'byte_count_column': 'length'
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
    'Replicate_Number': {},
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Mass_Spec_Data_Owner_Fkey.values._display_name}}}'
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
    'Biosample': 'Biosample from which this X Ray Tomography data was obtained',
    'Replicate_Number': 'Number of the technical replicate.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Dataset', em.builtin_types['text'], nullok=False, comment=column_comment['Dataset'],
    ),
    em.Column.define(
        'Description', em.builtin_types['markdown'], comment=column_comment['Description'],
    ),
    em.Column.define(
        'File_Type',
        em.builtin_types['text'],
        annotations=column_annotations['File_Type'],
        comment=column_comment['File_Type'],
    ),
    em.Column.define(
        'Submitted_On', em.builtin_types['timestamptz'], comment=column_comment['Submitted_On'],
    ),
    em.Column.define('File_Id', em.builtin_types['int4'], comment=column_comment['File_Id'],
                     ),
    em.Column.define(
        'Biosample', em.builtin_types['ermrest_rid'], comment=column_comment['Biosample'],
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
        'url', em.builtin_types['text'], nullok=False, annotations=column_annotations['url'],
    ),
    em.Column.define(
        'filename',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['filename'],
    ),
    em.Column.define(
        'Replicate_Number',
        em.builtin_types['int2'],
        default=1,
        comment=column_comment['Replicate_Number'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    '*': [
        ['Beta_Cell', 'Mass_Spec_Data_Key'], 'RCB', 'Owner',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Mass_Spec_Data_Dataset_FKey']
            }, 'RID'],
            'markdown_name': 'Dataset'
        },
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
            }, 'RID'],
            'markdown_name': 'Biosample'
        }, 'filename', 'Replicate_Number', 'Description',
        ['Beta_Cell', 'Mass_Spec_Data_File_Type_FKey'], 'length', 'submitted_on'
    ],
    'entry': [
        'RID', ['Beta_Cell', 'Mass_Spec_Data_Dataset_FKey'],
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Biosample_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey'], 'Description', 'url',
        ['Beta_Cell', 'Mass_Spec_Data_File_Type_FKey'], 'filename',
        ['Beta_Cell', 'Mass_Spec_Data_File_Type_FKey'], 'length', 'md5', 'submitted_on'
    ],
    'filter': {
        'and': [
            {
                'entity': True,
                'source': 'RID'
            },
            {
                'source': [{
                    'outbound': ['Beta_Cell', 'Mass_Spec_Data_Dataset_FKey']
                }, 'RID'],
                'markdown_name': 'Dataset'
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
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
                'entity': True,
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
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
                'comment': 'Additives used to treat the cell line for the experiment',
                'aggregate': 'array',
                'markdown_name': 'Additive'
            },
            {
                'entity': True,
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
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
                'aggregate': 'array',
                'markdown_name': 'Concentration'
            },
            {
                'entity': True,
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
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
                'aggregate': 'array',
                'markdown_name': 'Duration'
            }, {
                'open': False,
                'entity': True,
                'source': 'filename',
                'markdown_name': 'File Name'
            },
            {
                'open': True,
                'entity': True,
                'source': [{
                    'outbound': ['Beta_Cell', 'Mass_Spec_Data_Anatomy_FKey']
                }, 'id'],
                'markdown_name': 'Anatomy'
            },
            {
                'open': True,
                'entity': True,
                'source': [{
                    'outbound': ['Beta_Cell', 'Mass_Spec_Data_File_Type_FKey']
                }, 'id'],
                'markdown_name': 'File Type'
            },
            {
                'open': False,
                'entity': True,
                'source': 'submitted_on',
                'markdown_name': 'Submitted On'
            }
        ]
    }
}

visible_foreign_keys = {
    'entry': [['isa', 'mesh_data_derived_from_fkey']],
    'detailed': [['isa', 'mesh_data_derived_from_fkey']]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_annotations = {
    'table_display': {
        'row_name': {
            'row_markdown_pattern': '{{{filename}}}'
        }
    },
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Table to hold X-Ray Tomography MRC files.'

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
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Mass_Spec_Data_RIDkey1')],
                  ),
    em.Key.define(
        ['Dataset', 'RID'],
        constraint_names=[('Beta_Cell', 'Mass_Spec_Data_Dataset_RID_Key')],
        comment='RID and dataset must be distinct.',
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Mass_Spec_Data_Owner_Fkey')],
    ),
    em.ForeignKey.define(
        ['Biosample', 'Dataset'],
        'Beta_Cell',
        'Biosample', ['RID', 'Dataset'],
        constraint_names=[('Beta_Cell', 'Mass_Spec_Dataset_RID_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Ensure that the dataset for the file is the same as for the biosample',
    ),
    em.ForeignKey.define(
        ['Dataset'],
        'Beta_Cell',
        'Dataset', ['RID'],
        constraint_names=[('Beta_Cell', 'Mass_Spec_Data_Dataset_FKey')],
        annotations={
            chaise_tags.display: {},
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.Mass_Spec_Data_Biosample_FKey.values._Dataset}}}'
            }
        },
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
        comment='Must be a valid reference to a dataset.',
    ),
    em.ForeignKey.define(
        ['Biosample'],
        'Beta_Cell',
        'Biosample', ['RID'],
        constraint_names=[('Beta_Cell', 'Mass_Spec_Data_Biosample_FKey')],
        annotations={chaise_tags.foreign_key: {
            'domain_filter_pattern': 'Dataset={{{_Dataset}}}'
        }},
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Mass_Spec_Data_RCB_Fkey')],
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

