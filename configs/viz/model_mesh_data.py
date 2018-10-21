import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'model_mesh_data'
schema_name = 'viz'

column_annotations = {'RCB': {}, 'RCT': {}, 'RID': {}, 'RMB': {}, 'RMT': {}}

column_comment = {'RCB': 'System-generated row created by user provenance.',
                  'RCT': 'System-generated row creation timestamp.',
                  'RID': 'System-generated unique row ID.',
                  'RMB': 'System-generated row modified by user provenance.',
                  'RMT': 'System-generated row modification timestamp'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False, comment=column_comment['RID'],),
               em.Column.define('model', em.builtin_types['text'], nullok=False,),
               em.Column.define('mesh', em.builtin_types['text'], nullok=False,),
               em.Column.define('color_r', em.builtin_types['int4'],),
               em.Column.define('color_g', em.builtin_types['int4'],),
               em.Column.define('color_b', em.builtin_types['int4'],),
               em.Column.define('opacity', em.builtin_types['float8'],),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'], comment=column_comment['RCB'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'], comment=column_comment['RMB'],),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False, comment=column_comment['RCT'],),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False, comment=column_comment['RMT'],),
               ]

table_annotations = {}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['model', 'mesh'],
                  constraint_names=[('viz', 'model_mesh_data_model_mesh_key')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('viz', 'model_mesh_data_pkey')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['mesh'],
                         'isa', 'mesh_data', ['RID'],
                         constraint_names=[
                             ('viz', 'model_mesh_data_mesh_fkey')],
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['model'],
                         'viz', 'model', ['RID'],
                         constraint_names=[
                             ('viz', 'model_mesh_data_model_fkey')],
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




def main():
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    update_catalog.update_table(server, catalog_id, schema_name, table_name, table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
