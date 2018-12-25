import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'PHYRE2_Model'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.PHYRE2_Model_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.PHYRE2_Model_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('Ingredient_ID', em.builtin_types['text'],
                     ),
    em.Column.define('PHYRE2_PDB_Final', em.builtin_types['text'],
                     ),
    em.Column.define('BU', em.builtin_types['text'],
                     ),
    em.Column.define('PHYRE2_Intensive_Model', em.builtin_types['text'],
                     ),
    em.Column.define('#_Description', em.builtin_types['text'],
                     ),
    em.Column.define('Job_Id', em.builtin_types['text'],
                     ),
    em.Column.define('Hit', em.builtin_types['text'],
                     ),
    em.Column.define('Confidence_(Percent)', em.builtin_types['float8'],
                     ),
    em.Column.define('Sequence_Identity_(Percent)', em.builtin_types['int4'],
                     ),
    em.Column.define('Alignment_Coverage_(Percent)', em.builtin_types['float8'],
                     ),
    em.Column.define('Hit_Info_1', em.builtin_types['text'],
                     ),
    em.Column.define('Hit_Info_2', em.builtin_types['text'],
                     ),
    em.Column.define('Hit_Info_3', em.builtin_types['text'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

table_annotations = {}
table_comment = None
table_acls = {}
table_acl_bindings = {
    'self_service_creator': {
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    },
    'self_service_owner': {
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    }
}

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'PHYRE2_Model_RID_Key')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['Ingredient_ID'],
        'Beta_Cell',
        'Ingredient', ['RID'],
        constraint_names=[('Beta_Cell', 'PHYRE2_Model_Ingredient_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'PHYRE2_Model_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'PHYRE2_Model_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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

