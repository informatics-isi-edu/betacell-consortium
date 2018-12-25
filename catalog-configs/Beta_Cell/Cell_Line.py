import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Cell_Line'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Cell_Line_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Cell_Line_Id': {},
    'Species': {},
    'Anatomy': {},
    'Description': {},
    'Protocol': {},
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Cell_Line_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Cell_Line_Id': 'ID of cell line being used.',
    'Species': 'Species of the specimen',
    'Anatomy': 'Anatomical region speciment was obtained from.',
    'Description': 'Description of the specimen.',
    'Protocol': 'Protocol used to create the cell line'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Cell_Line_Id', em.builtin_types['text'], comment=column_comment['Cell_Line_Id'],
    ),
    em.Column.define('Species', em.builtin_types['text'], comment=column_comment['Species'],
                     ),
    em.Column.define('Anatomy', em.builtin_types['text'], comment=column_comment['Anatomy'],
                     ),
    em.Column.define(
        'Description', em.builtin_types['text'], comment=column_comment['Description'],
    ),
    em.Column.define('Protocol', em.builtin_types['text'], comment=column_comment['Protocol'],
                     ),
    em.Column.define('Collection_Date', em.builtin_types['date'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    'filter': {
        'and': [
            {
                'source': [{
                    'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
                }, 'name'],
                'open': True,
                'markdown_name': 'Cell Line',
                'entity': True
            },
            {
                'source': [{
                    'outbound': ['Beta_Cell', 'Cell_Line_Species_FKey']
                }, 'name'],
                'open': True,
                'markdown_name': 'Species',
                'entity': True
            },
            {
                'source': [{
                    'outbound': ['Beta_Cell', 'Cell_Line_Anatomy_FKey']
                }, 'name'],
                'open': True,
                'markdown_name': 'Anatomy',
                'entity': True
            }
        ]
    },
    '*': [
        ['Beta_Cell', 'Cell_Line_Key'], 'RCB',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Cell_Line_Owner_Fkey']
            }, 'id']
        }, ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey'], ['Beta_Cell', 'Cell_Line_Species_FKey'],
        ['Beta_Cell', 'Cell_Line_Anatomy_FKey'], ['Beta_Cell', 'Cell_Line_Protocol_FKey'],
        'Description', 'Collection_Date'
    ]
}

visible_foreign_keys = {
    '*': [{
        'source': [{
            'inbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
        }, 'RID']
    }]
}

table_display = {}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    'table_display': {},
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'Table of cultured  from which specimens  will be created.'
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

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Cell_Line_Key')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['Species'],
        'vocab',
        'species_terms', ['id'],
        constraint_names=[('Beta_Cell', 'Cell_Line_Species_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Cell_Line_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol', ['RID'],
        constraint_names=[('Beta_Cell', 'Cell_Line_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Cell_Line_Id'],
        'vocab',
        'cell_line_terms', ['id'],
        constraint_names=[('Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'Cell_Line_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Anatomy'],
        'vocab',
        'anatomy_terms', ['id'],
        constraint_names=[('Beta_Cell', 'Cell_Line_Anatomy_FKey')],
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

