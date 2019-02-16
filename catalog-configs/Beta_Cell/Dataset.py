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
    'entry': [
        'Title', 'RCB', {
            'source': [{
                'outbound': ['Beta_Cell', 'Dataset_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Dataset_Project_FKey'], 'Description'
    ],
    'filter': {
        'and': [
            {
                'source': ['RID']
            },
            {
                'open': False,
                'entity': True,
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Dataset_Experiment_Type_Dataset_id_FKey']
                    }, {
                        'outbound': ['Beta_Cell', 'Dataset_Experiment_Type_Experiment_type_FKey']
                    }, 'dbxref'
                ]
            },
            {
                'open': False,
                'entity': True,
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Dataset_project_fkey']
                    }, {
                        'inbound': ['isa', 'project_investigator_project_id_fkey']
                    }, {
                        'outbound': ['isa', 'project_investigator_person_fkey']
                    }, 'RID'
                ],
                'markdown_name': 'Project Investigator'
            }, {
                'open': False,
                'entity': False,
                'source': 'Title'
            },
            {
                'open': False,
                'entity': True,
                'source': [{
                    'outbound': ['Beta_Cell', 'Dataset_project_fkey']
                }, 'id']
            }, {
                'open': False,
                'entity': False,
                'source': 'release_date'
            },
            {
                'open': False,
                'entity': True,
                'source': [{
                    'outbound': ['Beta_Cell', 'Dataset_status_fkey']
                }, 'name']
            }
        ]
    },
    'compact': [
        ['Beta_Cell', 'Dataset_RID_Key'], 'RCB', 'Owner', 'Title',
        ['Beta_Cell', 'Dataset_Project_FKey'], 'Description'
    ],
    'detailed': [
        ['Beta_Cell', 'Dataset_RID_Key'], 'RCB', 'Owner', 'Description',
        ['Beta_Cell', 'Dataset_Project_FKey'], ['Beta_Cell', 'Dataset_Status_FKey'],
        ['Beta_Cell', 'Dataset_Experiment_type_Dataset__id_fkey'],
        ['Beta_Cell', 'Dataset_data_type_dataset_id_fkey'],
        ['Beta_Cell', 'Dataset_anatomy_Dataset_id_fkey']
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
    chaise_tags.visible_columns: visible_columns,
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

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Dataset_RID_key')], ), ]

fkey_defs = [
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
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Dataset_Owner_Fkey')],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Dataset_RCB_Fkey')],
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

