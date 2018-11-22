import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Biosample'
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
                '{{{$fkeys.Beta_Cell.Biosample_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Sample_Position': {},
    'Specimen': {},
    'Specimen_Type': {},
    'Experiment': {},
    'Protocol': {},
    'Container_Id': {}
}

column_comment = {
    'Sample_Position':
    'Position in the capillary where the sample is located.',
    'Specimen': 'Biological material used for the biosample.',
    'Specimen_Type': 'Method by which specimen is prepared.',
    'Experiment': 'Experiment in which this biosample is used',
    'Protocol': 'Biosample protocol.',
    'Container_Id':
    'ID number of the container with the biosample. Is a number'
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
        'Dataset',
        em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define(
        'Summary',
        em.builtin_types['text'],
    ),
    em.Column.define(
        'Collection_Date',
        em.builtin_types['date'],
    ),
    em.Column.define(
        'Sample_Position',
        em.builtin_types['int2'],
        comment=column_comment['Sample_Position'],
    ),
    em.Column.define(
        'Specimen',
        em.builtin_types['text'],
        comment=column_comment['Specimen'],
    ),
    em.Column.define(
        'Specimen_Type',
        em.builtin_types['text'],
        comment=column_comment['Specimen_Type'],
    ),
    em.Column.define(
        'Experiment',
        em.builtin_types['ermrest_rid'],
        comment=column_comment['Experiment'],
    ),
    em.Column.define(
        'Protocol',
        em.builtin_types['text'],
        comment=column_comment['Protocol'],
    ),
    em.Column.define(
        'Container_Id',
        em.builtin_types['int2'],
        comment=column_comment['Container_Id'],
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
                 'outbound': ['Beta_Cell', 'Biosample_Dataset_FKey']
             }, 'RID']
         },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
             }, 'name'],
             'markdown_name':
             'Cell Line'
         },
         {
             'comment':
             'Part of the cell from which the biosample was taken',
             'source':
             [{
                 'outbound': ['Beta_Cell', 'Biosample_Protocol_FKey']
             }, {
                 'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
             },
              {
                  'outbound':
                  ['Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey']
              }, 'name'],
             'markdown_name':
             'Cellular Location',
             'entity':
             True
         },
         {
             'comment':
             'Additives used to treat the cell line for the Experiment',
             'source': [
                 {
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
             'array'
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
                 'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
             }, {
                 'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
             }, {
                 'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
             }, 'Duration'],
             'aggregate':
             'array'
         }, ['Beta_Cell', 'Biosample_Specimen_Type_FKey'],
         {
             'source': [{
                 'inbound': ['isa', 'mesh_data_biosample_fkey']
             }, 'url']
         },
         {
             'source': [{
                 'inbound':
                 ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
             }, 'RID']
         },
         {
             'source': [{
                 'inbound':
                 ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
             }, 'RID']
         },
         {
             'source': [{
                 'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
             }, 'RID']
         }, {
             'ux_mode': 'choices',
             'source': 'Container_Id',
             'entity': True
         }]
    },
    'entry': [{
        'source': [{
            'outbound': ['Beta_Cell', 'Biosample_Dataset_FKey']
        }, 'RID'],
        'markdown_name':
        'Dataset'
    },
              {
                  'source': [{
                      'outbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
                  }, 'RID'],
                  'markdown_name':
                  'Experiment'
              }, ['Beta_Cell', 'Biosample_Protocol_FKey'],
              ['Beta_Cell', 'Biosample_Specimen_FKey'],
              ['Beta_Cell', 'Biosample_Specimen_Type_FKey'], 'Container_Id',
              {
                  'source': [{
                      'outbound': ['Beta_Cell', 'Biosample_Protocol_FKey']
                  }, 'Description']
              }, 'Sample_Position', 'collection_date'],
    '*':
    [['Beta_Cell', 'Biosample_Key'], 'RCB',
     {
         'source': [{
             'outbound': ['Beta_Cell', 'Biosample_Dataset_FKey']
         }, 'RID'],
         'markdown_name': 'Dataset'
     }, 'Summary',
     {
         'source': [{
             'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
         }, 'RID']
     },
     {
         'source': [{
             'outbound': ['Beta_Cell', 'Biosample_Experiment_FKey']
         }, 'RID'],
         'markdown_name':
         'Experiment'
     },
     {
         'source': [{
             'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
         }, {
             'outbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']
         }, {
             'outbound': ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey']
         }, 'name'],
         'markdown_name':
         'Cell Line'
     },
     {
         'comment':
         'Compound used to treat the cell line for the Experiment',
         'source': [{
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
         'array',
         'markdown_name':
         'Additive',
         'entity':
         True
     },
     {
         'comment':
         'Concentration of additive applied to cell line in mM',
         'source': [{
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
         'array',
         'markdown_name':
         'Concentration',
         'entity':
         True
     },
     {
         'comment':
         'Duration in minutes of additive applied to cell line in ',
         'source': [{
             'outbound': ['Beta_Cell', 'Biosample_Specimen_FKey']
         }, {
             'outbound': ['Beta_Cell', 'Specimen_Protocol_FKey']
         }, {
             'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
         }, 'Duration'],
         'aggregate':
         'array',
         'markdown_name':
         'Duration',
         'entity':
         True
     },
     {
         'comment':
         'Part of the cell from which the biosample was taken',
         'source': [{
             'outbound': ['Beta_Cell', 'Biosample_Protocol_FKey']
         }, {
             'inbound': ['Beta_Cell', 'Protocol_Step_Protocol_FKey']
         },
                    {
                        'outbound': [
                            'Beta_Cell',
                            'Protocol_Step_Cellular_Location_Term_FKey'
                        ]
                    }, 'RID'],
         'markdown_name':
         'Cellular Location',
         'entity':
         True
     }, ['Beta_Cell', 'Biosample_Specimen_Type_FKey'], 'Container_Id',
     'Sample_Position', 'Collection_Date']
}

visible_foreign_keys = {
    '*': [{
        'source': [{
            'inbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
        }, 'RID']
    },
          {
              'source': [{
                  'inbound':
                  ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
              }, 'RID']
          },
          {
              'source': [{
                  'inbound': ['Beta_Cell', 'Mass_Spec_Data_Biosample_FKey']
              }, 'RID']
          }, ['viz', 'model_biosample_fkey']]
}

table_display = {
    'row_name': {
        'row_markdown_pattern':
        '{{RID}}{{#local_identifier}} {{Container_Id}}{{/local_identifier}}'
    }
}

table_alternatives = {}

export = {
    'templates': [{
        'outputs': [{
            'source': {
                'table': 'Beta_Cell:Biosample',
                'api': 'entity'
            },
            'destination': {
                'type': 'csv',
                'name': 'Biosample'
            }
        },
                    {
                        'source': {
                            'path': 'url:=URL,md5:=MD5,length:=Byte_Count',
                            'api': 'attribute',
                            'table': 'Beta_Cell:XRay_Tomography_Data'
                        },
                        'destination': {
                            'type': 'fetch',
                            'name': 'MRC'
                        }
                    },
                    {
                        'source': {
                            'path': 'url:=URL,md5:=MD5,length:=Byte_Count',
                            'api': 'attribute',
                            'table': 'Beta_Cell:Processed_Tomography_Data'
                        },
                        'destination': {
                            'type': 'fetch',
                            'name': 'processed_data'
                        }
                    },
                    {
                        'source': {
                            'path': 'url',
                            'api': 'attribute',
                            'table': 'isa:mesh_data'
                        },
                        'destination': {
                            'type': 'fetch',
                            'name': 'OBJS'
                        }
                    }],
        'name':
        'default',
        'format_name':
        'BDBag (Holey)',
        'format_type':
        'BAG'
    },
                  {
                      'outputs': [{
                          'source': {
                              'table': 'Beta_Cell:Biosample',
                              'api': 'entity'
                          },
                          'destination': {
                              'type': 'csv',
                              'name': 'Biosample'
                          }
                      },
                                  {
                                      'source': {
                                          'path': 'url:=URL',
                                          'api': 'attribute',
                                          'table':
                                          'Beta_Cell:XRay_Tomography_Data'
                                      },
                                      'destination': {
                                          'type': 'download',
                                          'name': 'MRC'
                                      }
                                  },
                                  {
                                      'source': {
                                          'path':
                                          'url:=URL',
                                          'api':
                                          'attribute',
                                          'table':
                                          'Beta_Cell:Processed_Tomography_Data'
                                      },
                                      'destination': {
                                          'type': 'download',
                                          'name': 'processed_data'
                                      }
                                  },
                                  {
                                      'source': {
                                          'path': 'URL',
                                          'api': 'attribute',
                                          'table': 'isa:mesh_data'
                                      },
                                      'destination': {
                                          'type': 'download',
                                          'name': 'OBJS'
                                      }
                                  }],
                      'name':
                      'default',
                      'format_name':
                      'BDBag',
                      'format_type':
                      'BAG'
                  }]
}

table_annotations = {
    'tag:isrd.isi.edu,2016:export': export,
    'tag:isrd.isi.edu,2016:table-alternatives': table_alternatives,
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:misd.isi.edu,2015:display': display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
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
        ['Dataset', 'RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Dataset_RID_Key')],
        annotations={'tag:misd.isi.edu,2015:display': {}},
    ),
    em.Key.define(
        ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Key')],
        annotations={'tag:misd.isi.edu,2015:display': {}},
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Specimen'],
        'Beta_Cell',
        'Specimen',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Specimen_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Specimen_Type'],
        'vocab',
        'specimen_type_terms',
        ['id'],
        constraint_names=[('Beta_Cell', 'Biosample_Specimen_Type_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        comment='Must be a valid reference to a specimen type.',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client',
        ['id'],
        constraint_names=[('Beta_Cell', 'Biosample_RCB_Fkey')],
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
        constraint_names=[('Beta_Cell', 'Biosample_Dataset_FKey')],
        annotations={
            'tag:misd.isi.edu,2015:display': {},
            'tag:isrd.isi.edu,2016:foreign-key': {
                'domain_filter_pattern':
                'RID={{{$fkeys.Beta_Cell.Biosample_Experiment_FKey.values._Dataset}}}'
            }
        },
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Protocol'],
        'Beta_Cell',
        'Protocol',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Protocol_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Experiment', 'Dataset'],
        'Beta_Cell',
        'Experiment',
        ['RID', 'Dataset'],
        constraint_names=[('Beta_Cell', 'Biosample_Experiment_Dataset_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Experiment'],
        'Beta_Cell',
        'Experiment',
        ['RID'],
        constraint_names=[('Beta_Cell', 'Biosample_Experiment_FKey')],
        annotations={
            'tag:misd.isi.edu,2015:display': {},
            'tag:isrd.isi.edu,2016:foreign-key': {
                'domain_filter_pattern': 'Dataset={{{_Dataset}}}'
            }
        },
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
