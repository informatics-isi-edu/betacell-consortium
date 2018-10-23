import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Collection'
schema_name = 'Common'

column_annotations = {
    'Description': {},
    'Details': {},
    'Persistend_ID': {
        'tag:isrd.isi.edu,2016:column-display': {
            '*': {
                'markdown_pattern': '[{{{Persistent_ID}}}]({{{Persistent_ID}}})'}},
        'tag:isrd.isi.edu,2016:generated': 'null'},
    'Require_DOI?': {
        'tag:isrd.isi.edu,2016:column-display': {
            '*': {
                'pre_format': {
                    'bool_false_value': 'No',
                    'bool_true_value': 'Yes',
                    'format': '%t'}}}}}

column_comment = {
    'Description': 'A short description of the collection. This value will be '
    'used for DOI metadata.',
    'Details': 'Additional details. This value will NOT be used for DOI '
    'metadata.',
    'Require_DOI?': 'True/Yes if a DOI is required (recommended if the '
    'collection will be cited in a publication). A DOI will be '
    'generated after the Collection is Released. Default is '
    'False/No.'}

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

visible_columns = {'*': ['RID', 'Title', 'Description', 'RCT', 'RMT'],
                   'filter': {'and': ['RID',
                                      'Title',
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

visible_foreign_keys = None

table_display = {}

export = {'templates': [{'format_name': 'BDBag (Holey)',
                         'format_type': 'BAG',
                         'name': 'default',
                         'outputs': [{'destination': {'name': 'Collection',
                                                      'type': 'csv'},
                                      'source': {'api': 'entity',
                                                 'table': 'Common:Collection'}},
                                     {'destination': {'name': 'Biosample',
                                                      'type': 'csv'},
                                      'source': {'api': 'attributegroup',
                                                 'path': '(RID)=(Collection_Biosample:Collection)/BS:=(Biosample)=(Biosample:RID)/CollectionRID:=M:RID,Dataset:=BS:Dataset,BiosampleRID:=RID,Container_Id,Sample_Position',
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
                                                'processor_params': {'test': 'False'}}]}]}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:export': export,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'a collection of data'

table_acls = {}

table_acl_bindings = {}

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

table_def = em.Table.define(table_name,
                            column_defs=column_defs,
                            key_defs=key_defs,
                            fkey_defs=fkey_defs,
                            annotations=table_annotations,
                            acls=table_acls,
                            acl_bindings=table_acl_bindings,
                            comment=table_comment,
                            provide_system=True
                            )


def main():
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    update_catalog.update_table(server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
