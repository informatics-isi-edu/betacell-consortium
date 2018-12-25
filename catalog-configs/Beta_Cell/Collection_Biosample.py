import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Collection_Biosample'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Collection_Biosample_Owner_Fkey.values._display_name}}}'
            }
        }
    },
    'Collection': {},
    'Biosample': {},
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Collection_Biosample_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {'Collection': 'Collection foreign key.', 'Biosample': 'Biosample foreign key.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Collection',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Collection'],
    ),
    em.Column.define(
        'Biosample', em.builtin_types['text'], nullok=False, comment=column_comment['Biosample'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', 'RCB',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Collection_Biosample_Owner_Fkey']
            }, 'id']
        }, ['Common', 'Collection_Biosample_Collection_fkey'],
        ['Beta_Cell', 'Collection_Biosample_Biosample_fkey']
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
        ['Collection', 'Biosample'],
        constraint_names=[('Beta_Cell', 'Collection_Biosample_Collection_Biosample_key')],
        comment='protocol and compound must be distinct.',
    ),
    em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Collection_Biosample_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Biosample'],
        'Beta_Cell',
        'Biosample', ['RID'],
        constraint_names=[('Beta_Cell', 'Collection_Biosample_Biosample_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Collection'],
        'Common',
        'Collection', ['RID'],
        constraint_names=[('Beta_Cell', 'Collection_Biosample_Collection_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a valid reference to an collection.',
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

