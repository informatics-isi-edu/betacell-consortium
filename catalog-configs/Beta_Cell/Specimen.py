import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Specimen'
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
                '{{{$fkeys.Beta_Cell.Specimen_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Description': {},
    'Collection_Date': {},
    'Cell_Line': {},
    'Protocol': {
        tags.column_display: {
            'compact': {
                'markdown_pattern':
                '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'
            }
        }
    }
}

column_comment = {
    'Description': 'Description of the specimen.',
    'Collection_Date': 'Date the specimen was obtained',
    'Cell_Line': 'Cell line used for the specimen.'
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
        em.builtin_types['text'],
        comment=column_comment['Description'],
    ),
    em.Column.define(
        'Collection_Date',
        em.builtin_types['date'],
        comment=column_comment['Collection_Date'],
    ),
    em.Column.define(
        'Cell_Line',
        em.builtin_types['text'],
        comment=column_comment['Cell_Line'],
    ),
    em.Column.define(
        'Protocol',
        em.builtin_types['text'],
        annotations=column_annotations['Protocol'],
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
            'source': [{
                'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
            }, {
                'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
            }, 'name'],
            'open':
            True,
            'markdown_name':
            'Cell Line',
            'entity':
            True
        },
         {
             'source': [{
                 'outbound':
                 ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey']
             }, 'name'],
             'markdown_name':
             'Cellular Location'
         },
         {
             'comment':
             'Additive used to treat the cell line for the experiment',
             'source':
             [{
                 'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
             }, {
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
             'Concentration of additive applied to cell line in mM',
             'markdown_name':
             'Concentration',
             'entity':
             True,
             'ux_mode':
             'choices',
             'source': [
                 {
                     'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
                 }, {
                     'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
                 },
                 {
                     'inbound': [
                         'Beta_Cell',
                         'Protocol_Step_Additive_Term_Protocol_Step_FKey'
                     ]
                 }, 'Additive_Concentration'
             ],
             'aggregate':
             'array'
         },
         {
             'comment':
             'Duration in minutes',
             'markdown_name':
             'Duration',
             'entity':
             True,
             'ux_mode':
             'choices',
             'source': [{
                 'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
             }, {
                 'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
             }, 'Duration'],
             'aggregate':
             'array'
         },
         {
             'source': [{
                 'inbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
             }, 'RID']
         }, 'Description', 'Collection_Date']
    },
    'entry': [['Beta_Cell', 'Specimen_Cell_Line_FKey'],
              ['Beta_Cell', 'Specimen_Protocol_FKey'],
              ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey'],
              'Description', 'Collection_Date'],
    '*': [
        'RID', 'Protocol',
        {
            'source': [{
                'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
            }, {
                'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
            }, 'name'],
            'open':
            True,
            'markdown_name':
            'Cell Line',
            'entity':
            True
        },
        {
            'source': [{
                'outbound':
                ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey']
            }, 'name'],
            'markdown_name':
            'Cellular Location'
        },
        {
            'comment':
            'Additive used to treat the cell line for the experiment',
            'source': [{
                'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
            }, {
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
            'Concentration of additive applied to cell line in mM',
            'markdown_name':
            'Concentration',
            'entity':
            True,
            'ux_mode':
            'choices',
            'source': [{
                'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
            }, {
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
            'comment':
            'Duration in minutes',
            'markdown_name':
            'Duration',
            'entity':
            True,
            'ux_mode':
            'choices',
            'source': [{
                'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
            }, {
                'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            }, 'Duration'],
            'aggregate':
            'array'
        }, 'Description', 'Collection_Date'
    ]
}

visible_foreign_keys = {
    '*': [{
        'source': [{
            'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
        }, {
            'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
        }, 'RID']
    },
          {
              'source': [{
                  'inbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
              }, 'RID']
          }]
}

table_display = {}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'table_display': {},
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'Table of biological speciments from which biosamples will be created.'

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
        constraint_names=[('Beta_Cell', 'Specimen_RIDkey1')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client',
        ['id'],
        constraint_names=[('Beta_Cell', 'Specimen_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Cell_Line'],
        'Beta_Cell',
        'Cell_Line',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Specimen_Cell_Line_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Specimen_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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
