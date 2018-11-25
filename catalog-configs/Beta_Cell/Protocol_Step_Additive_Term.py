import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_name = 'Protocol_Step_Additive_Term'

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
    em.Column.define(
        'Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
    ),
]

visible_columns = {
    '*': [
        'RID', ['Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey'],
        ['Beta_Cell', 'Protocol_Step_Additive_Term_Additive_Term_FKey'],
        'Additive_Concentration'
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
table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['Protocol_Step', 'Additive_Term'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_Key')],
        comment='protocol and compound must be distinct.',
    ),
    em.Key.define(
        ['RID'],
        constraint_names=[('Beta_Cell', 'Protocol_Step_Additive_Term_RIDkey1')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Protocol_Step'],
        'Beta_Cell',
        'Protocol_Step', ['RID'],
        constraint_names=[
            ('Beta_Cell', 'Protocol_Step_Additive_Term_Protocol_Step_FKey')
        ],
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

