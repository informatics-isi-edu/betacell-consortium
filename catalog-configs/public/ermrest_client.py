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

table_name = 'ERMrest_Client'

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
    }
}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('ID', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('Display_Name', em.builtin_types['text'],
                     ),
    em.Column.define('Full_Name', em.builtin_types['text'],
                     ),
    em.Column.define('Email', em.builtin_types['text'],
                     ),
    em.Column.define('Client_Object', em.builtin_types['jsonb'], nullok=False,
                     ),
]

display = {'name': 'Users'}

visible_columns = {'compact': ['ID', 'Full_Name', 'Display_Name', 'Email']}

table_display = {'row_name': {'row_markdown_pattern': '{{{Full_Name}}}'}}

table_annotations = {
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
}

table_comment = None

table_acls = {'select': ['*']}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['ID'], constraint_names=[('public', 'ermrest_client_id_key')],
                  ),
    em.Key.define(['RID'], constraint_names=[('public', 'ermrest_client_pkey')],
                  ),
]

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

