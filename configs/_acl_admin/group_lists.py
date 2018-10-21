import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'group_lists'
schema_name = '_acl_admin'

column_annotations = {
    'RCB': {},
    'RCT': {},
    'RMB': {},
    'RMT': {},
    'groups': {},
    'name': {}}

column_comment = {
    'RCB': 'System-generated row created by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RMB': 'System-generated row modified by user provenance.',
    'RMT': 'System-generated row modification timestamp',
    'groups': 'List of groups. This table is maintained by the rbk_acls '
    'program and should not be updated by hand.',
    'name': 'Name of grouplist, used in foreign keys. This table is maintained '
    'by the rbk_acls program and should not be updated by hand.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'name',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['name'],
    ),
    em.Column.define(
        'groups',
        em.builtin_types['text[]'],
        comment=column_comment['groups'],
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
        comment=column_comment['RMT'],
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
        comment=column_comment['RCT'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
        comment=column_comment['RMB'],
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
        comment=column_comment['RCB'],
    ),
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
    ),
]

generated = None

table_annotations = {'tag:isrd.isi.edu,2016:generated': generated, }

table_comment = (
    'Named lists of groups used in ACLs. Maintained by the rbk_acls program. Do '
    'not update this table manually.')

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['name'],
                  constraint_names=[('_acl_admin', 'group_lists_name_u')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('_acl_admin', 'group_lists_RID_key')],
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
    update_catalog.update_table(server, catalog_id, schema_name, table_name, table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
