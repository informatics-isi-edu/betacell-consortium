import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'person'

schema_name = 'common'

column_annotations = {}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('name', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('first_name', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('middle_name', em.builtin_types['text'],
                     ),
    em.Column.define('last_name', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('email', em.builtin_types['text'],
                     ),
    em.Column.define('degrees', em.builtin_types['json'],
                     ),
    em.Column.define('affiliation', em.builtin_types['text'],
                     ),
    em.Column.define('website', em.builtin_types['text'],
                     ),
]

visible_columns = {
    'compact': ['name', 'email', 'affiliation'],
    'detailed': ['name', 'email', 'affiliation']
}

table_display = {
    '*': {
        'row_order': [{
            'column': 'last_name',
            'descending': False
        }]
    },
    'row_name': {
        'row_markdown_pattern': '{{{first_name}}} {{{last_name}}}'
    }
}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'Standard definition for a person in catalog'
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(['name'], constraint_names=[('common', 'person_pkey')],
                  ),
    em.Key.define(['RID'], constraint_names=[('common', 'person_RID_key')],
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

