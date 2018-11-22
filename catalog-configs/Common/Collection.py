import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Collection'
schema_name = 'Common'

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
                '{{{$fkeys.Common.Collection_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Description': {},
    'Details': {},
    'Require_DOI?': {
        tags.column_display: {
            '*': {
                'pre_format': {
                    'bool_true_value': 'Yes',
                    'bool_false_value': 'No',
                    'format': '%t'
                }
            }
        }
    },
    'Persistend_ID': {
        tags.column_display: {
            '*': {
                'markdown_pattern':
                '[{{{Persistent_ID}}}]({{{Persistent_ID}}})'
            }
        },
        tags.generated: 'null'
    }
}

column_comment = {
    'Description':
    'A short description of the collection. This value will be used for DOI metadata.',
    'Details':
    'Additional details. This value will NOT be used for DOI metadata.',
    'Require_DOI?':
    'True/Yes if a DOI is required (recommended if the collection will be cited in a publication). A DOI will be generated after the Collection is Released. Default is False/No.'
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
        'Title',
        em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
        nullok=False,
        comment=column_comment['Description'],
    ),
    em.Column.define(
        'Details',
        em.builtin_types['markdown'],
        comment=column_comment['Details'],
    ),
    em.Column.define(
        'Require_DOI?',
        em.builtin_types['boolean'],
        annotations=column_annotations['Require_DOI?'],
        comment=column_comment['Require_DOI?'],
    ),
    em.Column.define(
        'Persistend_ID',
        em.builtin_types['text'],
        annotations=column_annotations['Persistend_ID'],
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
        'and': [
            'RID', 'Title',
            {
                'source':
                [{
                    'inbound':
                    ['Beta_Cell', 'Collection_Biosample_Collection_fkey']
                },
                 {
                     'outbound':
                     ['Beta_Cell', 'Collection_Biosample_Biosample_fkey']
                 },
                 {
                     'inbound':
                     ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                 }, 'RID'],
                'markdown_name':
                'XRay Tomography Data'
            },
            {
                'source':
                [{
                    'inbound':
                    ['Beta_Cell', 'Collection_Biosample_Collection_fkey']
                },
                 {
                     'outbound':
                     ['Beta_Cell', 'Collection_Biosample_Biosample_fkey']
                 },
                 {
                     'inbound':
                     ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                 }, 'RID']
            }
        ]
    },
    '*': ['RID', 'RCB', 'Title', 'Description', 'RCT', 'RMT']
}

visible_foreign_keys = None

table_display = {}

export = {
    'templates': [{
        'displayname':
        'BDBag (Holey)',
        'outputs':
        [{
            'source': {
                'api': 'entity'
            },
            'destination': {
                'type': 'csv',
                'name': 'Collection'
            }
        },
         {
             'source': {
                 'path':
                 '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/CollectionRID:=M:RID,Dataset:=BS:Dataset,BiosampleRID:=RID,Container_Id,Sample_Position',
                 'api':
                 'attributegroup'
             },
             'destination': {
                 'type': 'csv',
                 'name': 'Biosample'
             }
         },
         {
             'source': {
                 'path':
                 '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length',
                 'api':
                 'attributegroup'
             },
             'destination': {
                 'type': 'csv',
                 'name': 'Processed_Tomography_Data'
             }
         },
         {
             'source': {
                 'path':
                 '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length',
                 'api':
                 'attributegroup'
             },
             'destination': {
                 'type':
                 'fetch',
                 'name':
                 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/Processed_Tomography_Data'
             }
         },
         {
             'source': {
                 'path':
                 '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length',
                 'api':
                 'attributegroup'
             },
             'destination': {
                 'type': 'csv',
                 'name': 'XRay_Tomography_Data'
             }
         },
         {
             'source': {
                 'path':
                 '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(XRay_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length',
                 'api':
                 'attributegroup'
             },
             'destination': {
                 'type':
                 'fetch',
                 'name':
                 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/XRay_Tomography_Data'
             }
         }],
        'postprocessors': [{
            'processor': 'cloud_upload',
            'processor_params': {
                'target_url': 's3://pbcconsortium/test',
                'acl': 'public-read'
            }
        }, {
            'processor': 'identifier',
            'processor_params': {
                'test': 'False'
            }
        }],
        'type':
        'BAG'
    }]
}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:export': export,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'a collection of data'

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
        ['Title'],
        constraint_names=[('Common', 'Collection_Title_key')],
    ),
    em.Key.define(
        ['RID'],
        constraint_names=[('Common', 'Collection_RID_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client',
        ['id'],
        constraint_names=[('Common', 'Collection_RCB_Fkey')],
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
