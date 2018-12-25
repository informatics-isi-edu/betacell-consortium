import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'group_lists'

schema_name = '_acl_admin'

column_annotations = {'name': {}, 'groups': {}, 'RMT': {}, 'RCT': {}, 'RMB': {}, 'RCB': {}}

column_comment = {
    'name': 'Name of grouplist, used in foreign keys. This table is maintained by the rbk_acls program and should not be updated by hand.',
    'groups': 'List of groups. This table is maintained by the rbk_acls program and should not be updated by hand.',
    'RMT': 'System-generated row modification timestamp',
    'RCT': 'System-generated row creation timestamp.',
    'RMB': 'System-generated row modified by user provenance.',
    'RCB': 'System-generated row created by user provenance.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'name', em.builtin_types['text'], nullok=False, comment=column_comment['name'],
    ),
    em.Column.define('groups', em.builtin_types['text[]'], comment=column_comment['groups'],
                     ),
]

generated = None

table_annotations = {chaise_tags.generated: generated, }
table_comment = 'Named lists of groups used in ACLs. Maintained by the rbk_acls program. Do not update this table manually.'
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('_acl_admin', 'group_lists_RID_key')],
                  ),
    em.Key.define(['name'], constraint_names=[('_acl_admin', 'group_lists_name_u')],
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

