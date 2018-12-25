import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'model_mesh_data'

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
    em.Column.define('model', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('mesh', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('color_r', em.builtin_types['int4'], default=255,
                     ),
    em.Column.define('color_g', em.builtin_types['int4'], default=215,
                     ),
    em.Column.define('color_b', em.builtin_types['int4'],
                     ),
    em.Column.define('opacity', em.builtin_types['float8'], default=1.0,
                     ),
]

table_annotations = {}
table_comment = None
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['mesh', 'model'], constraint_names=[('viz', 'model_mesh_data_model_mesh_key')],
    ),
    em.Key.define(['RID'], constraint_names=[('viz', 'model_mesh_data_pkey')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['mesh'],
        'isa',
        'mesh_data', ['RID'],
        constraint_names=[('viz', 'model_mesh_data_mesh_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['model'],
        'viz',
        'model', ['RID'],
        constraint_names=[('viz', 'model_mesh_data_model_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]

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

