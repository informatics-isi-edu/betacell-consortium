import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Dataset'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Dataset_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Dataset_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('Title', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('Project', em.builtin_types['int8'], nullok=False,
                     ),
    em.Column.define('Description', em.builtin_types['markdown'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    'filter': {
        'and': [
            {
                'source': ['RID']
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Dataset_Experiment_Type_Dataset_id_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Dataset_Experiment_Type_Experiment_type_FKey']
                    }, 'dbxref'
                ],
                'open': False,
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Dataset_project_fkey']
                    }, {
                        'inbound': ['isa', 'project_investigator_project_id_fkey']
                    }, {
                        'outbound': ['isa', 'project_investigator_person_fkey']
                    }, 'RID'
                ],
                'open': False,
                'markdown_name': 'Project Investigator',
                'entity': True
            }, {
                'source': 'Title',
                'open': False,
                'entity': False
            },
            {
                'source': [{
                    'outbound': ['Beta_Cell', 'Dataset_project_fkey']
                }, 'id'],
                'open': False,
                'entity': True
            }, {
                'source': 'release_date',
                'open': False,
                'entity': False
            },
            {
                'source': [{
                    'outbound': ['Beta_Cell', 'Dataset_status_fkey']
                }, 'name'],
                'open': False,
                'entity': True
            }
        ]
    },
    'entry': [
        'Title', 'RCB', {
            'source': [{
                'outbound': ['Beta_Cell', 'Dataset_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Dataset_Project_FKey'], 'Description'
    ],
    'detailed': [
        ['Beta_Cell', 'Dataset_RID_Key'], 'RCB', 'Owner', 'Description',
        ['Beta_Cell', 'Dataset_Project_FKey'], ['Beta_Cell', 'Dataset_Status_FKey'],
        ['Beta_Cell', 'Dataset_Experiment_type_Dataset__id_fkey'],
        ['Beta_Cell', 'Dataset_data_type_dataset_id_fkey'],
        ['Beta_Cell', 'Dataset_anatomy_Dataset_id_fkey']
    ],
    'compact': [
        ['Beta_Cell', 'Dataset_RID_Key'], 'RCB', 'Owner', 'Title',
        ['Beta_Cell', 'Dataset_Project_FKey'], 'Description'
    ]
}

visible_foreign_keys = {
    '*': [
        ['viz', 'model_Dataset_fkey'], ['Beta_Cell', 'Experiment_Dataset_FKey'],
        ['Beta_Cell', 'Biosample_Dataset_FKey'], ['Beta_Cell', 'File_Dataset_FKey']
    ]
}

table_display = {
    '*': {
        'row_order': [{
            'column': 'accession',
            'descending': True
        }]
    },
    'row_name': {
        'row_markdown_pattern': '{{Title}}'
    }
}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
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

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Dataset_RID_key')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Dataset_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Project'],
        'isa',
        'project', ['id'],
        constraint_names=[('Beta_Cell', 'Dataset_Project_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Dataset_RCB_Fkey')],
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

