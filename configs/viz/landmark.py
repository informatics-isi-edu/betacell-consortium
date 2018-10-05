import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'landmark'
schema_name = 'viz'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('mesh', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('label', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('point_x', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('point_y', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('point_z', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('radius', em.builtin_types['float8'],
        nullok=False,
    ),
    em.Column.define('color_r', em.builtin_types['int4'],
    ),
    em.Column.define('color_g', em.builtin_types['int4'],
    ),
    em.Column.define('color_b', em.builtin_types['int4'],
    ),
    em.Column.define('anatomy', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('viz', 'landmark_RID_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('viz', 'landmark_pkey')],
    ),
    em.Key.define(['point_y', 'mesh', 'point_x', 'point_z'],
                   constraint_names=[('viz', 'landmark_mesh_point_x_point_y_point_z_key')],
    ),
]


fkey_defs = [
]


visible_columns = {}
visible_foreign_keys = {}
table_comment = \
None

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}

column_annotations = \
{}



table_def = em.Table.define(table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system = True
)