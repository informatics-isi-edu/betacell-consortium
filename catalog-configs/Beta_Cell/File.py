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

table_name = 'File'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.File_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'URL': {
        chaise_tags.asset: {
            'md5': 'md5',
            'url_pattern': '/hatrac/commons/data/{{{Dataset}}}/{{#encode}}{{{Filename}}}{{/encode}}',
            'filename_column': 'filename',
            'byte_count_column': 'byte_count'
        },
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'
            },
            'detailed': {
                'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'
            }
        }
    },
    'Filename': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            },
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            }
        }
    },
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.File_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('URL', em.builtin_types['text'], annotations=column_annotations['URL'],
                     ),
    em.Column.define(
        'Filename',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['Filename'],
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
                     ),
    em.Column.define('byte_count', em.builtin_types['int8'],
                     ),
    em.Column.define('Submitted_On', em.builtin_types['timestamptz'],
                     ),
    em.Column.define('md5', em.builtin_types['text'],
                     ),
    em.Column.define('Dataset', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

display = {'name': 'Supplementary Files'}

visible_columns = {
    'entry': [
        {
            'source': [{
                'outbound': ['Beta_Cell', 'File_Owner_Fkey']
            }, 'id']
        }, 'url', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'], ['isa', 'file_dataset_fkey'],
        'submitted_on', 'description'
    ],
    'filter': {
        'and': [
            {
                'open': False,
                'entity': True,
                'source': [{
                    'outbound': ['isa', 'file_dataset_fkey']
                }, 'accession'],
                'markdown_name': 'Dataset'
            }
        ]
    },
    'compact': [['isa', 'file_RID_key'], 'url', 'byte_count', 'md5', 'description'],
    'detailed': [
        'RCB', 'Owner', 'filename', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'],
        ['isa', 'file_dataset_fkey'], 'submitted_on', 'description'
    ]
}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_alternatives = {'compact': ['isa', 'file_compact'], 'compact/brief': ['isa', 'file_compact']}

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
    em.Key.define(['URL'], constraint_names=[('Beta_Cell', 'File_url_key')],
                  ),
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'File_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Dataset'],
        'Beta_Cell',
        'Dataset', ['RID'],
        constraint_names=[('Beta_Cell', 'File_Dataset_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'File_Owner_Fkey')],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'File_RCB_Fkey')],
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

