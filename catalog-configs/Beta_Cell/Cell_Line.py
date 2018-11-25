import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_name = 'Cell_Line'

schema_name = 'Beta_Cell'

groups = AttrDict(
    {
        'admins': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
        'modelers': 'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
        'curators': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
        'writers': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'readers': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
        'isrd': 'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
    }
)

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
    em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,
                     ),
    em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,
                     ),
    em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,
                     ),
    em.Column.define(
        'RCB', em.builtin_types['ermrest_rcb'], annotations=column_annotations['RCB'],
    ),
    em.Column.define('RMB', em.builtin_types['ermrest_rmb'],
                     ),
    em.Column.define(
        'Cell_Line_Id',
        em.builtin_types['text'],
        comment=column_comment['Cell_Line_Id'],
    ),
    em.Column.define(
        'Species', em.builtin_types['text'], comment=column_comment['Species'],
    ),
    em.Column.define(
        'Anatomy', em.builtin_types['text'], comment=column_comment['Anatomy'],
    ),
    em.Column.define(
        'Description', em.builtin_types['text'], comment=column_comment['Description'],
    ),
    em.Column.define(
        'Protocol', em.builtin_types['text'], comment=column_comment['Protocol'],
    ),
    em.Column.define('Collection_Date', em.builtin_types['date'],
                     ),
    em.Column.define(
        'Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
    ),
]

visible_columns = {
    'filter': {
        'and': [
            {
                'source': [
                    {
                        'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
                    }, 'name'
                ],
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
        }, ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey'],
        ['Beta_Cell', 'Cell_Line_Species_FKey'], ['Beta_Cell', 'Cell_Line_Anatomy_FKey'],
        ['Beta_Cell', 'Cell_Line_Protocol_FKey'], 'Description', 'Collection_Date'
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
table_acl_bindings = {}

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'Cell_Line_Key')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol', ['RID'],
        constraint_names=[('Beta_Cell', 'Cell_Line_Protocol_FKey')],
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


def main(
    skip_args=False,
    mode='annotations',
    replace=False,
    server='pbcconsortium.isrd.isi.edu',
    catalog_id=1
):

    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(
            server, catalog_id, is_table=True
        )
    update_catalog.update_table(
        mode, replace, server, catalog_id, schema_name, table_name, table_def,
        column_defs, key_defs, fkey_defs, table_annotations, table_acls,
        table_acl_bindings, table_comment, column_annotations, column_acls,
        column_acl_bindings, column_comment
    )


if __name__ == "__main__":
    main()

