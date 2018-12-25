import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'ermrest_client'

schema_name = 'public'

column_annotations = {}

column_comment = {}

column_acls = {'client_obj': {'select': []}}

column_acl_bindings = {}

column_defs = [
    em.Column.define('id', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('display_name', em.builtin_types['text'],
                     ),
    em.Column.define('full_name', em.builtin_types['text'],
                     ),
    em.Column.define('email', em.builtin_types['text'],
                     ),
    em.Column.define(
        'client_obj', em.builtin_types['jsonb'], nullok=False, acls=column_acls['client_obj'],
    ),
]

table_annotations = {}
table_comment = None
table_acls = {
    'insert': [],
    'delete': [],
    'update': [],
    'select': [
        'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a'
    ],
    'enumerate': []
}
table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('public', 'ermrest_client_pkey')],
                  ),
    em.Key.define(['id'], constraint_names=[('public', 'ermrest_client_id_key')],
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
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_table=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)

