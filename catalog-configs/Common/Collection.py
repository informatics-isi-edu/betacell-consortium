import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pbcconsortium-reader': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'pbcconsortium-curator': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'pbcconsortium-writer': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'pbcconsortium-admin': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'isrd-testers': 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
}

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
                    'format': '%t',
                    'bool_true_value': 'Yes',
                    'bool_false_value': 'No'
                }
            }
        }
    },
    'Persistend_ID': {
        chaise_tags.generated: 'null',
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '[{{{Persistent_ID}}}]({{{Persistent_ID}}})'
            }
        }
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
    '*': [
        'RID', 'RCB', {
            'source': [{
                'outbound': ['Beta_Cell', 'Collection_Owner_Fkey']
            }, 'id']
        }, 'Title', 'Description', 'RCT', 'RMT'
    ],
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
    }
}

visible_foreign_keys = None

table_display = {}

export = {
    'templates': [
        {
            'type': 'BAG',
            'outputs': [
                {
                    'source': {
                        'api': 'entity'
                    },
                    'destination': {
                        'name': 'Collection',
                        'type': 'csv'
                    }
                },
                {
                    'source': {
                        'api': 'attributegroup',
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/CollectionRID:=M:RID,Dataset:=BS:Dataset,BiosampleRID:=RID,Container_Id,Sample_Position'
                    },
                    'destination': {
                        'name': 'Biosample',
                        'type': 'csv'
                    }
                },
                {
                    'source': {
                        'api': 'attributegroup',
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length'
                    },
                    'destination': {
                        'name': 'Processed_Tomography_Data',
                        'type': 'csv'
                    }
                },
                {
                    'source': {
                        'api': 'attributegroup',
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length'
                    },
                    'destination': {
                        'name': 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/Processed_Tomography_Data',
                        'type': 'fetch'
                    }
                },
                {
                    'source': {
                        'api': 'attributegroup',
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length'
                    },
                    'destination': {
                        'name': 'XRay_Tomography_Data',
                        'type': 'csv'
                    }
                },
                {
                    'source': {
                        'api': 'attributegroup',
                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(XRay_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length'
                    },
                    'destination': {
                        'name': 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/XRay_Tomography_Data',
                        'type': 'fetch'
                    }
                }
            ],
            'displayname': 'BDBag (Holey)'
        }
    ]
}

table_annotations = {
    chaise_tags.export: export,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'a collection of data'

table_acls = {}

table_acl_bindings = {
    'self_service_owner': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('Common', 'Collection_RID_key')],
                  ),
    em.Key.define(['Title'], constraint_names=[('Common', 'Collection_Title_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Common', 'Collection_RCB_Fkey')],
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Common', 'Collection_Owner_Fkey')],
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
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

