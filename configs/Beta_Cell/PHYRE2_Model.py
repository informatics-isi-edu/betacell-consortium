import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'PHYRE2_Model'
schema_name = 'Beta_Cell'

column_annotations = {}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Ingredient_ID', em.builtin_types['text'],),
               em.Column.define('PHYRE2_PDB_Final', em.builtin_types['text'],),
               em.Column.define('BU', em.builtin_types['text'],),
               em.Column.define('PHYRE2_Intensive_Model', em.builtin_types['text'],),
               em.Column.define('#_Description', em.builtin_types['text'],),
               em.Column.define('Job_Id', em.builtin_types['text'],),
               em.Column.define('Hit', em.builtin_types['text'],),
               em.Column.define('Confidence_(Percent)', em.builtin_types['float8'],),
               em.Column.define('Sequence_Identity_(Percent)', em.builtin_types['int4'],),
               em.Column.define('Alignment_Coverage_(Percent)', em.builtin_types['float8'],),
               em.Column.define('Hit_Info_1', em.builtin_types['text'],),
               em.Column.define('Hit_Info_2', em.builtin_types['text'],),
               em.Column.define('Hit_Info_3', em.builtin_types['text'],),
               ]

table_annotations = {}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'PHYRE2_Model_RID_Key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Ingredient_ID'],
                         'Beta_Cell', 'Ingredient', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'PHYRE2_Model_Ingredient_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         on_update='CASCADE',
                         on_delete='RESTRICT',
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
