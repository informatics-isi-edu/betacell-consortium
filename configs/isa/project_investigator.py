import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'project_investigator'
schema_name = 'isa'

column_annotations = {'RCB': {}, 'RCT': {}, 'RID': {}, 'RMB': {}, 'RMT': {}}

column_comment = {'RCB': 'System-generated row created by user provenance.',
                  'RCT': 'System-generated row creation timestamp.',
                  'RID': 'System-generated unique row ID.',
                  'RMB': 'System-generated row modified by user provenance.',
                  'RMT': 'System-generated row modification timestamp'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'project_id',
        em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
        comment=column_comment['RID'],
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
        comment=column_comment['RCB'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
        comment=column_comment['RMB'],
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
        comment=column_comment['RCT'],
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
        comment=column_comment['RMT'],
    ),
    em.Column.define(
        'person',
        em.builtin_types['text'],
        nullok=False,
    ),
]

table_annotations = {}

table_comment = None

table_acls = {}

table_acl_bindings = {
    'project_suppl_edit_guard': {
        'projection': [
            {
                'outbound': [
                    'isa',
                    'project_investigator_project_id_fkey']},
            {
                'outbound': [
                    'isa',
                    'project_groups_fkey']},
            'groups'],
        'projection_type': 'acl',
        'scope_acl': [
            'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
            'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
        'types': [
            'update',
            'delete']}}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('isa', 'project_investigator_RID_key')],
                  ),
    em.Key.define(['project_id', 'person'],
                  constraint_names=[('isa', 'project_investigator_pkey')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['person'],
                         'isa', 'person', ['RID'],
                         constraint_names=[
                             ('isa', 'project_investigator_person_fkey')],
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['project_id'],
                         'isa', 'project', ['id'],
                         constraint_names=[
                             ('isa', 'project_investigator_project_id_fkey')],
                         on_update='CASCADE',
                         on_delete='CASCADE',
                         ),
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


def main(skip_args=False, mode='annotations', replace=False, server='pbcconsortium.isrd.isi.edu', catalog_id=1):
    
    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
