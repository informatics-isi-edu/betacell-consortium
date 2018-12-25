import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'process'

schema_name = 'isa'

column_annotations = {}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('process_url', em.builtin_types['text'],
                     ),
    em.Column.define('description', em.builtin_types['markdown'],
                     ),
    em.Column.define('file_url', em.builtin_types['text'],
                     ),
    em.Column.define('filename', em.builtin_types['text'],
                     ),
    em.Column.define('byte_count', em.builtin_types['int4'],
                     ),
    em.Column.define('md5', em.builtin_types['text'],
                     ),
]

visible_columns = {}

visible_foreign_keys = {}

table_display = {}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'None'
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(['description'], constraint_names=[('isa', 'process_description_key')],
                  ),
    em.Key.define(['RID'], constraint_names=[('isa', 'process_pkey')],
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

