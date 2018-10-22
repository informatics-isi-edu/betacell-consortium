import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'person'
schema_name = 'isa'

column_annotations = {'RCB': {}, 'RCT': {}, 'RID': {}, 'RMB': {}, 'RMT': {}}

column_comment = {'RCB': 'System-generated row created by user provenance.',
                  'RCT': 'System-generated row creation timestamp.',
                  'RID': 'System-generated unique row ID.',
                  'RMB': 'System-generated row modified by user provenance.',
                  'RMT': 'System-generated row modification timestamp'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('name', em.builtin_types['text'], nullok=False,),
               em.Column.define('first_name', em.builtin_types['text'], nullok=False,),
               em.Column.define('middle_name', em.builtin_types['text'],),
               em.Column.define('last_name', em.builtin_types['text'], nullok=False,),
               em.Column.define('email', em.builtin_types['text'],),
               em.Column.define('degrees', em.builtin_types['json'],),
               em.Column.define('affiliation', em.builtin_types['text'],),
               em.Column.define('website', em.builtin_types['text'],),
               em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False, comment=column_comment['RID'],),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'], comment=column_comment['RCB'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'], comment=column_comment['RMB'],),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False, comment=column_comment['RCT'],),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False, comment=column_comment['RMT'],),
               ]

visible_columns = {'compact': ['name', 'email', 'affiliation'],
                   'detailed': ['name', 'email', 'affiliation']}

table_display = {'*': {'row_order': [{'column': 'last_name', 'descending': False}]},
                 'row_name': {'row_markdown_pattern': '{{{first_name}}} {{{last_name}}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'domain'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['name'],
                  constraint_names=[('isa', 'person_pkey')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('isa', 'person_RID_key')],
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
    update_catalog.update_table(server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
