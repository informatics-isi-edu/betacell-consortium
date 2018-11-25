import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_name = 'File'

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
        'URL', em.builtin_types['text'], annotations=column_annotations['URL'],
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
    em.Column.define(
        'Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
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
        }, 'url', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'],
        ['isa', 'file_dataset_fkey'], 'submitted_on', 'description'
    ],
    'detailed': [
        'RCB', 'Owner', 'filename', 'byte_count', 'md5', ['isa', 'file_thumbnail_fkey'],
        ['isa', 'file_dataset_fkey'], 'submitted_on', 'description'
    ],
    'compact': [['isa', 'file_RID_key'], 'url', 'byte_count', 'md5', 'description']
}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_alternatives = {
    'compact': ['isa', 'file_compact'],
    'compact/brief': ['isa', 'file_compact']
}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.display: display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.table_alternatives: table_alternatives,
}
table_comment = None
table_acls = {}
table_acl_bindings = {}

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
        on_update='CASCADE',
        on_delete='SET NULL',
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

