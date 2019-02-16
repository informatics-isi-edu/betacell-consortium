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

table_name = 'Page_Asset'

schema_name = 'WWW'

column_annotations = {
    'RCT': {
        chaise_tags.display: {
            'name': 'Creation Time'
        }
    },
    'RMT': {
        chaise_tags.display: {
            'name': 'Modified Time'
        }
    },
    'RCB': {
        chaise_tags.display: {
            'name': 'Created By'
        }
    },
    'RMB': {
        chaise_tags.display: {
            'name': 'Modified By'
        }
    },
    'URL': {
        chaise_tags.asset: {
            'md5': 'MD5',
            'url_pattern': '/hatrac/WWW/Page_Asset/{{{MD5}}}.{{#encode}}{{{Filename}}}{{/encode}}',
            'filename_column': 'Filename',
            'byte_count_column': 'Length'
        }
    },
    'Filename': {},
    'Description': {},
    'Length': {},
    'MD5': {},
    'Page_RID': {},
    'Owner': {}
}

column_comment = {
    'URL': 'URL to the asset',
    'Filename': 'Filename of the asset that was uploaded',
    'Description': 'Description of the asset',
    'Length': 'Asset length (bytes)',
    'MD5': 'Asset content MD5 checksum',
    'Page_RID': 'The Page entry to which this asset is attached',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'URL',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['URL'],
        comment=column_comment['URL'],
    ),
    em.Column.define('Filename', em.builtin_types['text'], comment=column_comment['Filename'],
                     ),
    em.Column.define(
        'Description', em.builtin_types['markdown'], comment=column_comment['Description'],
    ),
    em.Column.define(
        'Length', em.builtin_types['int8'], nullok=False, comment=column_comment['Length'],
    ),
    em.Column.define(
        'MD5', em.builtin_types['text'], nullok=False, comment=column_comment['MD5'],
    ),
    em.Column.define(
        'Page_RID', em.builtin_types['text'], nullok=False, comment=column_comment['Page_RID'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_Asset_RCB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_Asset_RMB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_Asset_Catalog_Group_fkey']
            }, 'ID']
        }, {
            'source': 'URL'
        }, {
            'source': 'Filename'
        }, {
            'source': 'Description'
        }, {
            'source': 'Length'
        }, {
            'source': 'MD5'
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_Asset_Page_fkey']
            }, 'RID']
        }
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{Filename}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
}

table_comment = 'Asset table for Page'

table_acls = {}

table_acl_bindings = {
    'self_service_group': {
        'types': ['update', 'delete'],
        'projection': ['Owner'],
        'projection_type': 'acl',
        'scope_acl': ['*']
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'projection': ['RCB'],
        'projection_type': 'acl',
        'scope_acl': ['*']
    }
}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('WWW', 'Page_Asset_RIDkey1')],
                  ),
    em.Key.define(['URL'], constraint_names=[('WWW', 'Page_Asset_URLkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Page_RID'],
        'WWW',
        'Page', ['RID'],
        constraint_names=[('WWW', 'Page_Asset_Page_fkey')],
        acls={
            'insert': [groups['pbcconsortium-curator']],
            'update': [groups['pbcconsortium-curator']]
        },
        acl_bindings={
            'self_linkage_owner': {
                'types': ['insert', 'update'],
                'projection': ['Owner'],
                'projection_type': 'acl',
                'scope_acl': ['*']
            },
            'self_linkage_creator': {
                'types': ['insert', 'update'],
                'projection': ['RCB'],
                'projection_type': 'acl',
                'scope_acl': ['*']
            }
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('WWW', 'Page_Asset_Catalog_Group_fkey')],
        acls={
            'insert': [groups['pbcconsortium-curator']],
            'update': [groups['pbcconsortium-curator']]
        },
        acl_bindings={
            'set_owner': {
                'types': ['update', 'insert'],
                'projection': ['ID'],
                'projection_type': 'acl',
                'scope_acl': ['*']
            }
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('WWW', 'Page_Asset_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('WWW', 'Page_Asset_RMB_fkey')],
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
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

