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

table_name = 'mesh_data'

schema_name = 'isa'

column_annotations = {
    'RID': {},
    'url': {
        chaise_tags.asset: {
            'md5': 'md5',
            'url_pattern': '/hatrac/commons/previews/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}',
            'filename_column': 'filename',
            'byte_count_column': 'byte_count'
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
        'url', em.builtin_types['text'], nullok=False, annotations=column_annotations['url'],
    ),
    em.Column.define(
        'filename',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['filename'],
    ),
    em.Column.define('byte_count', em.builtin_types['int8'], nullok=False,
                     ),
    em.Column.define('md5', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('dataset', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('derived_from', em.builtin_types['text'],
                     ),
    em.Column.define('anatomy', em.builtin_types['text'],
                     ),
    em.Column.define('label', em.builtin_types['text'],
                     ),
    em.Column.define('description', em.builtin_types['markdown'],
                     ),
    em.Column.define('biosample', em.builtin_types['text'],
                     ),
]

visible_columns = {
    'entry': [
        'RID', ['isa', 'mesh_data_biosample_fkey'], ['isa', 'mesh_data_derived_from_fkey'], 'url',
        'filename', 'byte_count', 'md5', ['isa', 'mesh_data_anatomy_fkey'], 'label', 'description'
    ],
    'filter': {
        'and': [
            {
                'open': False,
                'entity': True,
                'source': 'filename',
                'markdown_name': 'File Name'
            },
            {
                'open': True,
                'entity': True,
                'source': [{
                    'outbound': ['isa', 'mesh_data_dataset_fkey']
                }, 'RID'],
                'markdown_name': 'Dataset'
            },
            {
                'open': True,
                'entity': True,
                'source': [{
                    'outbound': ['isa', 'mesh_data_biosample_fkey']
                }, 'RID'],
                'markdown_name': 'Biosample'
            },
            {
                'open': True,
                'entity': True,
                'source': [{
                    'outbound': ['isa', 'mesh_data_derived_from_fkey']
                }, 'RID'],
                'markdown_name': 'Derived From File'
            }
        ]
    },
    'compact': [
        ['isa', 'mesh_data_pkey'], 'biosample', ['isa', 'mesh_data_derived_from_fkey'], 'url',
        'byte_count', 'md5'
    ],
    'detailed': [
        ['isa', 'mesh_data_pkey'], ['isa', 'mesh_data_dataset_fkey'],
        ['isa', 'mesh_data_biosample_fkey'], ['isa', 'mesh_data_derived_from_fkey'], 'filename',
        'byte_count', 'md5', ['isa', 'mesh_data_anatomy_fkey'], 'label', 'description'
    ]
}

visible_foreign_keys = {}

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

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['url'], constraint_names=[('isa', 'mesh_data_url_key')],
                  ),
    em.Key.define(['RID'], constraint_names=[('isa', 'mesh_data_pkey')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['biosample'],
        'Beta_Cell',
        'Biosample', ['RID'],
        constraint_names=[('isa', 'mesh_data_biosample_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['dataset'],
        'Beta_Cell',
        'Dataset', ['RID'],
        constraint_names=[('isa', 'mesh_data_dataset_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['derived_from'],
        'Beta_Cell',
        'XRay_Tomography_Data', ['RID'],
        constraint_names=[('isa', 'mesh_data_derived_from_fkey')],
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
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

