import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'landmark'

schema_name = 'viz'

column_annotations = {'RID': {}, 'RCB': {}, 'RMB': {}, 'RCT': {}, 'RMT': {}}

column_comment = {
    'RID': 'System-generated unique row ID.',
    'RCB': 'System-generated row created by user provenance.',
    'RMB': 'System-generated row modified by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RMT': 'System-generated row modification timestamp'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'], nullok=False,
                     ),
    em.Column.define('mesh', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('label', em.builtin_types['text'],
                     ),
    em.Column.define('description', em.builtin_types['markdown'],
                     ),
    em.Column.define('point_x', em.builtin_types['int4'], nullok=False,
                     ),
    em.Column.define('point_y', em.builtin_types['int4'], nullok=False,
                     ),
    em.Column.define('point_z', em.builtin_types['int4'], nullok=False,
                     ),
    em.Column.define('radius', em.builtin_types['float8'], nullok=False, default=0.1,
                     ),
    em.Column.define('color_r', em.builtin_types['int4'], default=255,
                     ),
    em.Column.define('color_g', em.builtin_types['int4'],
                     ),
    em.Column.define('color_b', em.builtin_types['int4'],
                     ),
    em.Column.define('anatomy', em.builtin_types['text'],
                     ),
]

table_annotations = {}
table_comment = None
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['point_x', 'mesh', 'point_y', 'point_z'],
        constraint_names=[('viz', 'landmark_mesh_point_x_point_y_point_z_key')],
    ),
    em.Key.define(['id'], constraint_names=[('viz', 'landmark_pkey')],
                  ),
    em.Key.define(['RID'], constraint_names=[('viz', 'landmark_RID_key')],
                  ),
]

fkey_defs = []

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True
)


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_table(mode, schema_name, table_def, replace=replace)


if __name__ == "__main__":
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_table=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)

