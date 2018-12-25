import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

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
            'filename_column': 'filename',
            'byte_count_column': 'byte_count',
            'url_pattern': '/hatrac/commons/data/{{{Dataset}}}/{{#encode}}{{{Filename}}}{{/encode}}',
            'md5': 'md5'
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
    'filter': {
        'and': [
            {
                'source': [{
                    'outbound': ['isa', 'file_dataset_fkey']
                }, 'accession'],
                'open': False,
                'markdown_name': 'Dataset',
                'entity': True
            }
        ]
    },
    'entry': [
        {
            'source': [{
                'outbound': ['Beta_Cell', 'File_Owner_Fkey']
            }, 'id']
        }, 'url', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'], ['isa', 'file_dataset_fkey'],
        'submitted_on', 'description'
    ],
    'detailed': [
        'RCB', 'Owner', 'filename', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'],
        ['isa', 'file_dataset_fkey'], 'submitted_on', 'description'
    ],
    'compact': [['isa', 'file_RID_key'], 'url', 'byte_count', 'md5', 'description']
}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_alternatives = {'compact': ['isa', 'file_compact'], 'compact/brief': ['isa', 'file_compact']}

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
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'File_RID_key')],
                  ),
    em.Key.define(['URL'], constraint_names=[('Beta_Cell', 'File_url_key')],
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
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'File_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'File_Owner_Fkey')],
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

