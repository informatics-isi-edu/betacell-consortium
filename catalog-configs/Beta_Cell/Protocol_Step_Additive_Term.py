import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Protocol_Step_Additive_Term'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Protocol_Step_Additive_Term_RBC_Fkey.values._display_name}}}'
            }
        }
    },
    'Protocol_Step': {},
    'Additive_Term': {},
    'Additive_Concentration': {},
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Protocol_Step_Additive_Term_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Protocol_Step': 'Protocol_Step foreign key.',
    'Additive_Term': 'Additive_Term foreign key.',
    'Additive_Concentration': 'Concentration of additive used in protocol step in mM.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
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
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'],
        ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey'], 'Additive_Concentration'
    ]
}

visible_foreign_keys = {}

table_display = {}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.visible_columns: visible_columns,
}
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

key_defs = [
    em.Key.define(
        ['Protocol_Step', 'Additive_Term'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_Key')],
        comment='protocol and compound must be distinct.',
    ),
    em.Key.define(
        ['RID'], constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_RIDkey1')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Additive_Term'],
        'Vocab',
        'Additive_Terms', ['id'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a valid reference to an additive.',
    ),
    em.ForeignKey.define(
        ['Protocol_Step'],
        'Beta_Cell',
        'Protocol_Step', ['RID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey')],
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

