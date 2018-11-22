import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Experiment'
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
                '{{{$fkeys.Beta_Cell.Experiment_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Experiment_Type': {
        tags.column_display: {
            'compact': {
                'markdown_pattern':
                '{{{$fkeys.Beta_Cell.Experiment_Experiment_Type_FKey.rowName}}}'
            }
        }
    },
    'Protocol': {
        tags.column_display: {
            'compact': {
                'markdown_pattern':
                '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'
            }
        }
    }
}

column_comment = {}

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
        'Dataset',
        em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define(
        'Experiment_Type',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['Experiment_Type'],
    ),
    em.Column.define(
        'Protocol',
        em.builtin_types['text'],
        annotations=column_annotations['Protocol'],
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
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

display = {}

visible_columns = {
    'filter': {
        'and':
        [{
            'source': 'RID',
            'entity': True
        },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Experiment_Dataset_FKey']
             }, 'RID']
         },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Experiment_Protocol_FKey']
             }, 'RID']
         },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Experiment_Experiment_Type_FKey']
             }, 'RID']
         },
         {
             'aggregate':
             'array_d',
             'source': [{
                 'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Cell_Line_cell_Line_Terms_fkey']
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
                 'inbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
             },
                        {
                            'outbound': [
                                'Beta_Cell',
                                'Specimen_cellular_location_terms_fkey'
                            ]
                        }, 'name'],
             'markdown_name':
             'Cellular Location'
         },
         {
             'comment':
             'Additives used to treat the specimens for the experiment',
             'source': [
                 {
                     'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                 }, {
                     'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                 }, {
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
                 }, 'RID'
             ],
             'aggregate':
             'array_d',
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
                     'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                 }, {
                     'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
                 }, {
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
             'array_d'
         },
         {
             'comment':
             'Duration in minutes of additive applied to cell line in ',
             'markdown_name':
             'Duration',
             'entity':
             True,
             'ux_mode':
             'choices',
             'source': [{
                 'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
             }, {
                 'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
             }, 'Duration'],
             'aggregate':
             'array_d'
         },
         {
             'source': [{
                 'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
             },
                        {
                            'inbound': [
                                'Beta_Cell',
                                'XRay_Tomography_Data_Biosample_FKey'
                            ]
                        }, 'RID']
         },
         {
             'source': [{
                 'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
             },
                        {
                            'inbound': [
                                'Beta_Cell',
                                'Processed_Tomography_Data_Biosample_FKey'
                            ]
                        }, 'RID']
         },
         {
             'source': [{
                 'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
             }, {
                 'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
             }, 'RID']
         },
         {
             'source': [{
                 'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
             }, {
                 'inbound': ['isa', 'mesh_data_biosample_fkey']
             }, 'RID']
         }]
    },
    'entry': [['Beta_Cell', 'Experiment_Dataset_FKey'],
              ['Beta_Cell', 'Experiment_Protocol_fkey'],
              ['Beta_Cell', 'Experiment_Experiment_Type_FKey'], 'description',
              'collection_date'],
    '*': [
        'RID', 'RCB', ['Beta_Cell', 'Experiment_Dataset_FKey'],
        ['Beta_Cell', 'Experiment_Protocol_FKey'],
        ['Beta_Cell', 'Experiment_Experiment_Type_FKey'],
        {
            'aggregate':
            'array_d',
            'source': [{
                'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
            }, {
                'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
            }, {
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
            'comment':
            'Additives used to treat the specimens for the experiment',
            'source': [{
                'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
            }, {
                'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
            }, {
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
            'array_d',
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
                'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
            }, {
                'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
            }, {
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
            'array_d'
        },
        {
            'comment':
            'Duration in minutes of additive applied to cell line in ',
            'markdown_name':
            'Duration',
            'entity':
            True,
            'ux_mode':
            'choices',
            'source': [{
                'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
            }, {
                'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
            }, {
                'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
            }, {
                'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
            }, 'Duration'],
            'aggregate':
            'array_d'
        }, 'description'
    ]
}

visible_foreign_keys = {
    '*':
    [['viz', 'model_experiment_fkey'],
     {
         'source': [{
             'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
         }, 'RID']
     },
     {
         'source': [{
             'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
         }, {
             'inbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
         }, 'RID']
     },
     {
         'source':
         [{
             'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
         },
          {
              'inbound':
              ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
          }, 'RID']
     },
     {
         'source': [{
             'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
         }, {
             'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
         }, 'RID']
     },
     {
         'source': [{
             'inbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
         }, {
             'inbound': ['isa', 'mesh_data_biosample_fkey']
         }, 'RID']
     }]
}

table_display = {
    'row_name': {
        'row_markdown_pattern':
        '{{RID}}{{#local_identifier}} - {{local_identifier}} {{/local_identifier}}{{#biosample_summary}} - {{biosample_summary}}{{/biosample_summary}}'
    }
}

table_alternatives = {}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:misd.isi.edu,2015:display': display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
    'tag:isrd.isi.edu,2016:table-alternatives': table_alternatives,
}

table_comment = None

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
        ['RID', 'Dataset'],
        constraint_names=[('Beta_Cell', 'Experiment_RID_Dataset_Key')],
    ),
    em.Key.define(
        ['RID'],
        constraint_names=[('Beta_Cell', 'Experiment_RID_Key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Experiment_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client',
        ['id'],
        constraint_names=[('Beta_Cell', 'Experiment_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Dataset'],
        'Beta_Cell',
        'Dataset',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Experiment_Dataset_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Experiment_Type'],
        'vocab',
        'experiment_type_terms',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Experiment_Experiment_Type_FKey')],
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
