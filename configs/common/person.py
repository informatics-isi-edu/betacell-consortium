import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'person'
schema_name = 'common'

column_annotations = {}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('name', em.builtin_types['text'], nullok=False,),
               em.Column.define('first_name', em.builtin_types['text'], nullok=False,),
               em.Column.define('middle_name', em.builtin_types['text'],),
               em.Column.define('last_name', em.builtin_types['text'], nullok=False,),
               em.Column.define('email', em.builtin_types['text'],),
               em.Column.define('degrees', em.builtin_types['json'],),
               em.Column.define('affiliation', em.builtin_types['text'],),
               em.Column.define('website', em.builtin_types['text'],),
               ]

visible_columns = {'compact': ['name', 'email', 'affiliation'],
                   'detailed': ['name', 'email', 'affiliation']}

table_display = {'*': {'row_order': [{'column': 'last_name', 'descending': False}]},
                 'row_name': {'row_markdown_pattern': '{{{first_name}}} {{{last_name}}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'Standard definition for a person in catalog'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('common', 'person_RID_key')],
                  ),
    em.Key.define(['name'],
                  constraint_names=[('common', 'person_pkey')],
                  ),
]

fkey_defs = [
]

table_def = em.Table.define(table_name,
                            column_defs=column_defs,
                            key_defs=key_defs,
                            fkey_defs=fkey_defs,
                            annotations=table_annotations,
                            acls=table_acls,
                            acl_bindings=table_acl_bindings,
                            comment=table_comment,
                            provide_system=True
                            )


def main():
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
