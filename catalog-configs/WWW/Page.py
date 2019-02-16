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

table_name = 'Page'

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
    'Title': {},
    'Content': {},
    'Owner': {}
}

column_comment = {
    'Title': 'Unique title for the page',
    'Content': 'Content of the page in markdown',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Title', em.builtin_types['text'], nullok=False, comment=column_comment['Title'],
    ),
    em.Column.define('Content', em.builtin_types['markdown'], comment=column_comment['Content'],
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
                'outbound': ['WWW', 'Page_RCB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_RMB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_Catalog_Group_fkey']
            }, 'ID']
        }, {
            'source': 'Title'
        }, {
            'source': 'Content'
        }
    ],
    'detailed': ['Content']
}

visible_foreign_keys = {'detailed': {}}

table_display = {'detailed': {'collapse_toc_panel': True, 'hide_column_headers': True}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = None

table_acls = {}

table_acl_bindings = {
    'self_service_group': {
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
    em.Key.define(['RID'], constraint_names=[('WWW', 'Page_RIDkey1')],
                  ),
    em.Key.define(['Title'], constraint_names=[('WWW', 'Page_Title_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('WWW', 'Page_Catalog_Group_fkey')],
        acls={
            'insert': [groups['pbcconsortium-curator']],
            'update': [groups['pbcconsortium-curator']]
        },
        acl_bindings={
            'set_owner': {
                'types': ['update', 'insert'],
                'scope_acl': ['*'],
                'projection': ['ID'],
                'projection_type': 'acl'
            }
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('WWW', 'Page_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('WWW', 'Page_RMB_fkey')],
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

