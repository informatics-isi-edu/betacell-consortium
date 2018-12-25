import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'Collection'

schema_name = 'Common'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Common.Collection_RCB_Fkey.values._display_name}}}'
            }
        }
    },
    'Description': {},
    'Details': {},
    'Require_DOI?': {
        chaise_tags.column_display: {
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
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '[{{{Persistent_ID}}}]({{{Persistent_ID}}})'
            }
        },
        chaise_tags.generated: 'null'
    },
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Common.Collection_Owner_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {
    'Description': 'A short description of the collection. This value will be used for DOI metadata.',
    'Details': 'Additional details. This value will NOT be used for DOI metadata.',
    'Require_DOI?': 'True/Yes if a DOI is required (recommended if the collection will be cited in a publication). A DOI will be generated after the Collection is Released. Default is False/No.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('Title', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
        nullok=False,
        comment=column_comment['Description'],
    ),
    em.Column.define('Details', em.builtin_types['markdown'], comment=column_comment['Details'],
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
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
]

visible_columns = {
    'filter': {
        'and': [
            'RID', 'Title',
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Collection_Biosample_Collection_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'Collection_Biosample_Biosample_fkey']
                    }, {
                        'inbound': ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey']
                    }, 'RID'
                ],
                'markdown_name': 'XRay Tomography Data'
            },
            {
                'source': [
                    {
                        'inbound': ['Beta_Cell', 'Collection_Biosample_Collection_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'Collection_Biosample_Biosample_fkey']
                    }, {
                        'inbound': ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey']
                    }, 'RID'
                ]
            }
        ]
    },
    '*': [
        'RID', 'RCB', {
            'source': [{
                'outbound': ['Beta_Cell', 'Collection_Owner_Fkey']
            }, 'id']
        }, 'Title', 'Description', 'RCT', 'RMT'
    ]
}

visible_foreign_keys = None

table_display = {}

export = {
    'templates': [
        {
            'displayname': 'BDBag (Holey)',
            'outputs': [
                {
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
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/CollectionRID:=M:RID,Dataset:=BS:Dataset,BiosampleRID:=RID,Container_Id,Sample_Position',
                        'api': 'attributegroup'
                    },
                    'destination': {
                        'type': 'csv',
                        'name': 'Biosample'
                    }
                },
                {
                    'source': {
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length',
                        'api': 'attributegroup'
                    },
                    'destination': {
                        'type': 'csv',
                        'name': 'Processed_Tomography_Data'
                    }
                },
                {
                    'source': {
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length',
                        'api': 'attributegroup'
                    },
                    'destination': {
                        'type': 'fetch',
                        'name': 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/Processed_Tomography_Data'
                    }
                },
                {
                    'source': {
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length',
                        'api': 'attributegroup'
                    },
                    'destination': {
                        'type': 'csv',
                        'name': 'XRay_Tomography_Data'
                    }
                },
                {
                    'source': {
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(XRay_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length',
                        'api': 'attributegroup'
                    },
                    'destination': {
                        'type': 'fetch',
                        'name': 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/XRay_Tomography_Data'
                    }
                }
            ],
            'postprocessors': [
                {
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
                }
            ],
            'type': 'BAG'
        }
    ]
}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    chaise_tags.export: export,
    chaise_tags.visible_columns: visible_columns,
}
table_comment = 'a collection of data'
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
    em.Key.define(['Title'], constraint_names=[('Common', 'Collection_Title_key')],
                  ),
    em.Key.define(['RID'], constraint_names=[('Common', 'Collection_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Common', 'Collection_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Common', 'Collection_Owner_Fkey')],
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

