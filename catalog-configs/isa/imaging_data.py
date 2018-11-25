import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_name = 'imaging_data'

schema_name = 'isa'

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
    'RID': {},
    'url': {
        chaise_tags.asset: {
            'filename_column': 'filename',
            'byte_count_column': 'byte_count',
            'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}',
            'md5': 'md5'
        }
    },
    'filename': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            },
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            }
        }
    },
    'file_type': {
        chaise_tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{$fkeys.isa.imaging_data_file_type_fkey.rowName}}}'
            }
        }
    },
    'submitted_on': {
        chaise_tags.immutable: None
    },
    'RCB': {},
    'RMB': {},
    'RCT': {},
    'RMT': {}
}

column_comment = {
    'RID': 'System-generated unique row ID.',
    'RCB': 'System-generated row created by user provenance.',
    'RMB': 'System-generated row modified by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RMT': 'System-generated row modification timestamp'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
        comment=column_comment['RID'],
    ),
    em.Column.define('dataset', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('anatomy', em.builtin_types['text'],
                     ),
    em.Column.define('description', em.builtin_types['markdown'],
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
        'file_type',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['file_type'],
    ),
    em.Column.define('byte_count', em.builtin_types['int8'], nullok=False,
                     ),
    em.Column.define(
        'submitted_on',
        em.builtin_types['timestamptz'],
        default='now()',
        annotations=column_annotations['submitted_on'],
    ),
    em.Column.define('md5', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define(
        'RCB', em.builtin_types['ermrest_rcb'], comment=column_comment['RCB'],
    ),
    em.Column.define(
        'RMB', em.builtin_types['ermrest_rmb'], comment=column_comment['RMB'],
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
        comment=column_comment['RCT'],
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
        comment=column_comment['RMT'],
    ),
    em.Column.define('file_id', em.builtin_types['int4'],
                     ),
    em.Column.define('replicate', em.builtin_types['text'],
                     ),
]

visible_columns = {
    'filter': {
        'and': [
            {
                'source': 'filename',
                'open': False,
                'markdown_name': 'File Name',
                'entity': True
            },
            {
                'source': [{
                    'outbound': ['isa', 'imaging_data_replicate_fkey']
                }, 'RID'],
                'open': True,
                'markdown_name': 'Replicate',
                'entity': True
            },
            {
                'source': [{
                    'outbound': ['isa', 'imaging_data_anatomy_fkey']
                }, 'id'],
                'open': True,
                'markdown_name': 'Anatomy',
                'entity': True
            },
            {
                'source': [{
                    'outbound': ['isa', 'imaging_data_device_fkey']
                }, 'id'],
                'open': True,
                'markdown_name': 'Imaging Device',
                'entity': True
            },
            {
                'source': [
                    {
                        'outbound': ['isa', 'imaging_data_equipment_model_fkey']
                    }, 'id'
                ],
                'open': True,
                'markdown_name': 'Equipment Model',
                'entity': True
            },
            {
                'source': [{
                    'outbound': ['isa', 'imaging_data_file_type_fkey']
                }, 'id'],
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
        'RID', ['isa', 'imaging_data_replicate_fkey'],
        ['isa', 'imaging_data_anatomy_fkey'], ['isa', 'imaging_data_device_fkey'],
        ['isa', 'imaging_data_equipment_model_fkey'], 'description', 'url', 'filename',
        ['isa', 'imaging_data_file_type_fkey'], 'byte_count', 'md5', 'submitted_on'
    ],
    'detailed': [
        ['isa', 'imaging_data_pkey'], ['isa', 'imaging_data_dataset_fkey'],
        ['isa', 'imaging_data_replicate_fkey'], ['isa',
                                                 'imaging_data_device_fkey'], 'filename',
        ['isa', 'imaging_data_file_type_fkey'], 'byte_count', 'md5', 'submitted_on'
    ],
    'compact': [
        ['isa', 'imaging_data_pkey'], 'replicate_fkey', 'url', 'file_type', 'byte_count',
        'md5', 'submitted_on'
    ]
}

visible_foreign_keys = {
    'detailed': [
        ['isa', 'thumbnail_thumbnail_of_fkey'], ['isa', 'mesh_data_derived_from_fkey']
    ],
    'entry': [
        ['isa', 'thumbnail_thumbnail_of_fkey'], ['isa', 'mesh_data_derived_from_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_alternatives = {
    'compact': ['isa', 'imaging_compact'],
    'compact/brief': ['isa', 'imaging_compact']
}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.table_alternatives: table_alternatives,
}
table_comment = None
table_acls = {}
table_acl_bindings = {}

key_defs = []

fkey_defs = []

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

