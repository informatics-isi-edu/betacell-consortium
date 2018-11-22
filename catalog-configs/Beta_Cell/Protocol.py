import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Protocol'
schema_name = 'Beta_Cell'

groups = AttrDict({
    'admins':
    'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'modelers':
    'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
    'curators':
    'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'writers':
    'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'readers':
    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'isrd':
    'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
})

tags = AttrDict({
    'immutable':
    'tag:isrd.isi.edu,2016:immutable',
    'display':
    'tag:misd.isi.edu,2015:display',
    'visible_columns':
    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys':
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':
    'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':
    'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives':
    'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':
    'tag:isrd.isi.edu,2016:column-display',
    'asset':
    'tag:isrd.isi.edu,2017:asset',
    'export':
    'tag:isrd.isi.edu,2016:export',
    'generated':
    'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':
    'tag:isrd.isi.edu,2017:bulk-upload'
})

column_annotations = {
    'RCB': {
        tags.display: {
            '*': {
                'markdown_name': 'Owner'
            }
        },
        tags.column_display: {
            '*': {
                'markdown_pattern':
                '{{{$fkeys.Beta_Cell.Protocol_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Description': {},
    'Type': {}
}

column_comment = {
    'Description': 'A description of the protocol.',
    'Type': 'The type of object for which this protocol is used.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
        annotations=column_annotations['RCB'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
        comment=column_comment['Description'],
    ),
    em.Column.define(
        'Type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Type'],
    ),
]

groups = AttrDict({
    'admins':
    'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'modelers':
    'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
    'curators':
    'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'writers':
    'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'readers':
    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'isrd':
    'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
})

tags = AttrDict({
    'immutable':
    'tag:isrd.isi.edu,2016:immutable',
    'display':
    'tag:misd.isi.edu,2015:display',
    'visible_columns':
    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys':
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':
    'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':
    'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives':
    'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':
    'tag:isrd.isi.edu,2016:column-display',
    'asset':
    'tag:isrd.isi.edu,2017:asset',
    'export':
    'tag:isrd.isi.edu,2016:export',
    'generated':
    'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':
    'tag:isrd.isi.edu,2017:bulk-upload'
})

visible_columns = {
    'filter': {
        'and':
        [{
            'source': 'RID'
        },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Protocol_Protocol_Type_FKey']
             }, 'RID']
         },
         {
             'comment':
             'Additive used in protocol step',
             'source':
             [{
                 'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
             },
              {
                  'inbound': [
                      'Beta_Cell',
                      'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                  ]
              },
              {
                  'outbound': [
                      'Beta_Cell',
                      'Protocol_Step_Additive_Term_Additive_Term_FKey'
                  ]
              }, 'RID'],
             'aggregate':
             'array',
             'markdown_name':
             'Additive',
             'entity':
             True
         },
         {
             'comment':
             'Additive used in protocol step',
             'markdown_name':
             'Concentration',
             'entity':
             True,
             'ux_mode':
             'choices',
             'source':
             [{
                 'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
             },
              {
                  'inbound': [
                      'Beta_Cell',
                      'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                  ]
              }, 'Additive_Concentration'],
             'aggregate':
             'array'
         },
         {
             'ux_mode':
             'choices',
             'source': [{
                 'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
             }, 'Duration'],
             'aggregate':
             'array',
             'markdown_name':
             'Duration'
         }, 'Description']
    },
    '*': [
        'RID', ['Beta_Cell', 'Protocol_Protocol_Type_FKey'],
        {
            'comment':
            'Additive used in protocol step',
            'source': [{
                'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            },
                       {
                           'inbound': [
                               'Beta_Cell',
                               'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                           ]
                       },
                       {
                           'outbound': [
                               'Beta_Cell',
                               'Protocol_Step_Additive_Term_Additive_Term_FKey'
                           ]
                       }, 'RID'],
            'aggregate':
            'array',
            'markdown_name':
            'Additive',
            'entity':
            True
        },
        {
            'comment':
            'Additive used in protocol step',
            'source': [{
                'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            },
                       {
                           'inbound': [
                               'Beta_Cell',
                               'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                           ]
                       }, 'Additive_Concentration'],
            'aggregate':
            'array',
            'markdown_name':
            'Concentration',
            'entity':
            True
        },
        {
            'ux_mode':
            'choices',
            'source': [{
                'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            }, 'Duration'],
            'aggregate':
            'array'
        }, 'Description'
    ]
}

visible_foreign_keys = {
    '*': [['Beta_Cell', 'Protocol_Step_Protocol_FKey'],
          ['Beta_Cell', 'Experiment_Protocol_FKey'],
          ['Beta_Cell', 'Biosample_Protocol_FKey'],
          ['Beta_Cell', 'Specimen_Protocol_FKey'],
          ['Beta_Cell', 'Cell_Line_Protocol_FKey']]
}

table_display = {
    'row_name': {
        'row_markdown_pattern': '{{#RID}}Protocol:{{Description}}{{/RID}}'
    }
}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'Table containing names of Beta Cell protocols'

table_acls = {}

table_acl_bindings = {
    'self_service': {
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['RID'],
        constraint_names=[('Beta_Cell', 'Protocol_RIDkey1')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Type'],
        'Beta_Cell',
        'Protocol_Type',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Protocol_Protocol_Type_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a protocol type.',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client',
        ['id'],
        constraint_names=[('Beta_Cell', 'Protocol_RCB_Fkey')],
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
    provide_system=True)


def main(skip_args=False, mode='annotations', replace=False, server='pbcconsortium.isrd.isi.edu', catalog_id=1):
    
    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
