import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Collection'
schema_name = 'Common'

column_defs = [
    em.Column.define('Title', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
        nullok=False,
        comment='A short description of the collection. This value will be used for DOI metadata.',
    ),
    em.Column.define('Details', em.builtin_types['markdown'],
        comment='Additional details. This value will NOT be used for DOI metadata.',
    ),
    em.Column.define('Require_DOI?', em.builtin_types['boolean'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'*': {'pre_format': {'bool_true_value': 'Yes', 'bool_false_value': 'No', 'format': '%t'}}}},
        comment='True/Yes if a DOI is required (recommended if the collection will be cited in a publication). A DOI will be generated after the Collection is Released. Default is False/No.',
    ),
    em.Column.define('Persistend_ID', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{{Persistent_ID}}}]({{{Persistent_ID}}})'}}, 'tag:isrd.isi.edu,2016:generated': 'null'},
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('Common', 'Collection_RID_key')],
    ),
    em.Key.define(['Title'],
                   constraint_names=[('Common', 'Collection_Title_key')],
    ),
]


fkey_defs = [
]


visible_columns = \
{'*': ['RID', 'Title', 'Description', 'RCT', 'RMT'],
 'filter': {'and': ['RID', 'Title',
                    {'markdown_name': 'XRay Tomography Data',
                     'source': [{'inbound': ['Beta_Cell',
                                             'Collection_Biosample_Collection_fkey']},
                                {'outbound': ['Beta_Cell',
                                              'Collection_Biosample_Biosample_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'XRay_Tomography_Data_Biosample_FKey']},
                                'RID']},
                    {'source': [{'inbound': ['Beta_Cell',
                                             'Collection_Biosample_Collection_fkey']},
                                {'outbound': ['Beta_Cell',
                                              'Collection_Biosample_Biosample_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Processed_Tomography_Data_Biosample_FKey']},
                                'RID']}]}}

visible_foreign_keys = \
None

table_comment = \
'a collection of data'

table_display = {}
table_acls = {}
table_acl_bindings = {}
export = \
{'templates': [{'format_name': 'BDBag (Holey)',
                'format_type': 'BAG',
                'name': 'default',
                'outputs': [{'destination': {'name': 'Collection',
                                             'type': 'csv'},
                             'source': {'api': 'entity',
                                        'table': 'Common:Collection'}},
                            {'destination': {'name': 'Biosample',
                                             'type': 'csv'},
                             'source': {'api': 'attributegroup',
                                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/CollectionRID:=M:RID,Dataset:=BS:Dataset,BiosampleRID:=RID,Capillary_Number,Sample_Position',
                                        'table': 'Common:Collection'}},
                            {'destination': {'name': 'Processed_Tomography_Data',
                                             'type': 'csv'},
                             'source': {'api': 'attributegroup',
                                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length',
                                        'table': 'Common:Collection'}},
                            {'destination': {'name': 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/Processed_Tomography_Data',
                                             'type': 'fetch'},
                             'source': {'api': 'attributegroup',
                                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length',
                                        'table': 'Common:Collection'}},
                            {'destination': {'name': 'XRay_Tomography_Data',
                                             'type': 'csv'},
                             'source': {'api': 'attributegroup',
                                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(Processed_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,filename,length',
                                        'table': 'Common:Collection'}},
                            {'destination': {'name': 'DS-{Dataset}/EXP-{Experiment}/BS-{Biosample}/XRay_Tomography_Data',
                                             'type': 'fetch'},
                             'source': {'api': 'attributegroup',
                                        'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/XR:=(RID)=(XRay_Tomography_Data:Biosample)/Collection:=M:RID,Dataset:=BS:Dataset,Experiment:=BS:Experiment,Biosample:=BS:RID,url,md5,length',
                                        'table': 'Common:Collection'}}],
                'postprocessors': [{'processor': 'cloud_upload',
                                    'processor_params': {'acl': 'public-read',
                                                         'target_url': 's3://pbcconsortium/test'}},
                                   {'processor': 'identifier',
                                    'processor_params': {'test': 'True'}}]}]}

table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:export": export,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Description': 'A short description of the collection. This value will be '
                'used for DOI metadata.',
 'Details': 'Additional details. This value will NOT be used for DOI metadata.',
 'Require_DOI?': 'True/Yes if a DOI is required (recommended if the collection '
                 'will be cited in a publication). A DOI will be generated '
                 'after the Collection is Released. Default is False/No.'}

column_annotations = \
{'Persistend_ID': {'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{{Persistent_ID}}}]({{{Persistent_ID}}})'}},
                   'tag:isrd.isi.edu,2016:generated': 'null'},
 'Require_DOI?': {'tag:isrd.isi.edu,2016:column-display': {'*': {'pre_format': {'bool_false_value': 'No',
                                                                                'bool_true_value': 'Yes',
                                                                                'format': '%t'}}}}}



table_def = em.Table.define(table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system = True
)
