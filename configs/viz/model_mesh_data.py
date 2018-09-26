import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'model_mesh_data'
schema_name = 'viz'

column_defs = [
    em.Column.define('model', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('mesh', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('color_r', em.builtin_types['int4'],
    ),
    em.Column.define('color_g', em.builtin_types['int4'],
    ),
    em.Column.define('color_b', em.builtin_types['int4'],
    ),
    em.Column.define('opacity', em.builtin_types['float8'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('viz', 'model_mesh_data_pkey')],
    ),
    em.Key.define(['mesh', 'model'],
                   constraint_names=[('viz', 'model_mesh_data_model_mesh_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['mesh'],
            'isa', 'mesh_data', ['RID'],
            constraint_names=[('viz', 'model_mesh_data_mesh_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['model'],
            'viz', 'model', ['RID'],
            constraint_names=[('viz', 'model_mesh_data_model_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
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
