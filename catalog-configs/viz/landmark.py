import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pbcconsortium-reader': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'pbcconsortium-curator': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'pbcconsortium-writer': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'pbcconsortium-admin': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'isrd-testers': 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
}

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
        ['point_y', 'point_x', 'point_z', 'mesh'],
        constraint_names=[('viz', 'landmark_mesh_point_x_point_y_point_z_key')],
    ),
    em.Key.define(['RID'], constraint_names=[('viz', 'landmark_RID_key')],
                  ),
    em.Key.define(['id'], constraint_names=[('viz', 'landmark_pkey')],
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
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

