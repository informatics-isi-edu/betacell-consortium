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
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = None

table_acls = {}

table_acl_bindings = {
    'self_service_owner': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['Additive_Term', 'Protocol_Step'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_Key')],
        comment='protocol and compound must be distinct.',
    ),
    em.Key.define(
        ['RID'], constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_RIDkey1')],
    ),
]

fkey_defs = [
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_RCB_Fkey')],
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_Owner_Fkey')],
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
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

