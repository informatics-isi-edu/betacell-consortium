import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Protocol_Step_Additive_Term'
schema_name = 'Beta_Cell'

column_annotations = {
    'Additive_Concentration': {},
    'Additive_Term': {},
    'Protocol_Step': {}}

column_comment = {
    'Additive_Concentration': 'Concentration of additive used in protocol step '
    'in mM.',
    'Additive_Term': 'Additive_Term foreign key.',
    'Protocol_Step': 'Protocol_Step foreign key.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
    ),
    em.Column.define(
        'Protocol_Step',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Protocol_Step'],
    ),
    em.Column.define(
        'Additive_Term',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Additive_Term'],
    ),
    em.Column.define(
        'Additive_Concentration',
        em.builtin_types['float4'],
        comment=column_comment['Additive_Concentration'],
    ),
]

visible_columns = {'*': ['RID',
                         ['Beta_Cell',
                          'Protocol_Step_Additive_Term_Protocol_Step_FKey'],
                         ['Beta_Cell',
                             'Protocol_Step_Additive_Term_Additive_Term_FKey'],
                         'Additive_Concentration']}

visible_foreign_keys = {}

table_display = {}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['Protocol_Step', 'Additive_Term'],
                  constraint_names=[
                      ('Beta_Cell', 'Protocol_Step_Additive_Term_Key')],
                  comment='protocol and compound must be distinct.',
                  ),
    em.Key.define(['RID'],
                  constraint_names=[
                      ('Beta_Cell', 'Protocol_Step_Additive_Term_RIDkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Additive_Term'],
                         'Vocab', 'Additive_Terms', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         comment='Must be a valid reference to an additive.',
                         ),
    em.ForeignKey.define(['Protocol_Step'],
                         'Beta_Cell', 'Protocol_Step', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
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
