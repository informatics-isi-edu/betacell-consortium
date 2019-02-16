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

table_name = 'Catalog_Group'

schema_name = 'public'

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
        chaise_tags.display: {
            'name': 'Group Management Page'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '[**{{Display_Name}}**]({{{URL}}})'
            }
        }
    }
}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('Display_Name', em.builtin_types['text'],
                     ),
    em.Column.define('URL', em.builtin_types['text'], annotations=column_annotations['URL'],
                     ),
    em.Column.define('Description', em.builtin_types['text'],
                     ),
    em.Column.define('ID', em.builtin_types['text'], nullok=False,
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
                'outbound': ['public', 'Catalog_Group_RCB_fkey']
            }, 'ID']
        }, {
            'source': [{
                'outbound': ['public', 'Catalog_Group_RMB_fkey']
            }, 'ID']
        }, {
            'source': 'Display_Name'
        }, {
            'source': 'URL'
        }, {
            'source': [{
                'outbound': ['public', 'Catalog_Group_Description1']
            }, 'Description']
        }, {
            'source': 'ID'
        }
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{Display_Name}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
}

table_comment = None

table_acls = {
    'insert': [groups['pbcconsortium-writer'], groups['pbcconsortium-curator']],
    'select': [groups['pbcconsortium-reader']]
}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('public', 'Catalog_Group_RIDkey1')],
                  ),
    em.Key.define(
        ['ID'],
        constraint_names=[('public', 'Group_ID_key')],
        comment='Compound key to ensure that columns sync up into Catalog_Groups on update.',
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Description', 'ID', 'URL', 'Display_Name'],
        'public',
        'ERMrest_Group', ['Description', 'ID', 'URL', 'Display_Name'],
        constraint_names=[('public', 'Catalog_Group_Description1')],
        acls={
            'insert': [groups['pbcconsortium-curator']],
            'update': [groups['pbcconsortium-curator']]
        },
        acl_bindings={
            'set_owner': {
                'types': ['insert'],
                'projection': ['ID'],
                'projection_type': 'acl',
                'scope_acl': ['*']
            }
        },
        on_update='CASCADE',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('public', 'Catalog_Group_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('public', 'Catalog_Group_RMB_fkey')],
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

