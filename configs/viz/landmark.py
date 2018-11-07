import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'landmark'
schema_name = 'viz'

column_annotations = {'RCB': {}, 'RCT': {}, 'RID': {}, 'RMB': {}, 'RMT': {}}

column_comment = {'RCB': 'System-generated row created by user provenance.',
                  'RCT': 'System-generated row creation timestamp.',
                  'RID': 'System-generated unique row ID.',
                  'RMB': 'System-generated row modified by user provenance.',
                  'RMT': 'System-generated row modification timestamp'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('id', em.builtin_types['serial4'], nullok=False,),
               em.Column.define('mesh', em.builtin_types['text'], nullok=False,),
               em.Column.define('label', em.builtin_types['text'],),
               em.Column.define('description', em.builtin_types['markdown'],),
               em.Column.define('point_x', em.builtin_types['int4'], nullok=False,),
               em.Column.define('point_y', em.builtin_types['int4'], nullok=False,),
               em.Column.define('point_z', em.builtin_types['int4'], nullok=False,),
               em.Column.define('radius', em.builtin_types['float8'], nullok=False, default=0.1),
               em.Column.define('color_r', em.builtin_types['int4'], default=255),
               em.Column.define('color_g', em.builtin_types['int4'],),
               em.Column.define('color_b', em.builtin_types['int4'],),
               em.Column.define('anatomy', em.builtin_types['text'],),
               em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False, comment=column_comment['RID'],),
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
    em.Key.define(['point_x', 'mesh', 'point_y', 'point_z'],
                  constraint_names=[
                      ('viz', 'landmark_mesh_point_x_point_y_point_z_key')],
                  ),
    em.Key.define(['id'],
                  constraint_names=[('viz', 'landmark_pkey')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('viz', 'landmark_RID_key')],
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
