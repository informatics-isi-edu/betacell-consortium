import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Biosample'
schema_name = 'Beta_Cell'

column_annotations = {'Container_Id': {},
                      'Dataset': {'tag:isrd.isi.edu,2016:column-display': {},
                                  'tag:isrd.isi.edu,2017:asset': {},
                                  'tag:misd.isi.edu,2015:display': {}},
                      'Experiment': {},
                      'Protocol': {},
                      'Sample_Position': {},
                      'Specimen': {'tag:isrd.isi.edu,2016:column-display': {},
                                   'tag:isrd.isi.edu,2017:asset': {},
                                   'tag:misd.isi.edu,2015:display': {}},
                      'Specimen_Type': {}}

column_comment = {
    'Container_Id': 'ID number of the container with the biosample. Is a '
    'number',
    'Experiment': 'Experiment in which this biosample is used',
    'Protocol': 'Biosample protocol.',
    'Sample_Position': 'Position in the capillary where the sample is located.',
    'Specimen': 'Biological material used for the biosample.',
    'Specimen_Type': 'Method by which specimen is prepared.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Dataset', em.builtin_types['text'], nullok=False, annotations=column_annotations['Dataset'],),
               em.Column.define('Summary', em.builtin_types['text'],),
               em.Column.define('Collection_Date', em.builtin_types['date'],),
               em.Column.define('Sample_Position', em.builtin_types['int2'], comment=column_comment['Sample_Position'],),
               em.Column.define('Specimen', em.builtin_types['text'], annotations=column_annotations['Specimen'], comment=column_comment['Specimen'],),
               em.Column.define('Specimen_Type', em.builtin_types['text'], comment=column_comment['Specimen_Type'],),
               em.Column.define('Experiment', em.builtin_types['ermrest_rid'], comment=column_comment['Experiment'],),
               em.Column.define('Protocol', em.builtin_types['text'], comment=column_comment['Protocol'],),
               em.Column.define('Container_Id', em.builtin_types['int2'], comment=column_comment['Container_Id'],),
               ]

display = {}

visible_columns = {'*': [['Beta_Cell', 'Biosample_Key'],
                         {'markdown_name': 'Dataset',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Dataset_FKey']},
                                     'RID']},
                         'Summary',
                         {'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Specimen_FKey']},
                                     'RID']},
                         {'markdown_name': 'Experiment',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Experiment_FKey']},
                                     'RID']},
                         {'markdown_name': 'Cell Line',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Specimen_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Specimen_Cell_Line_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Cell_Line_Cell_Line_Terms_FKey']},
                                     'name']},
                         {'aggregate': 'array',
                          'comment': 'Compound used to treat the cell line for the '
                          'Experiment',
                          'entity': True,
                          'markdown_name': 'Additive',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Specimen_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Specimen_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                     'RID']},
                         {'aggregate': 'array',
                          'comment': 'Concentration of additive applied to cell line in '
                          'mM',
                          'entity': True,
                          'markdown_name': 'Concentration',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Specimen_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Specimen_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     'Additive_Concentration']},
                         {'aggregate': 'array',
                          'comment': 'Duration in minutes of additive applied to cell '
                          'line in ',
                          'entity': True,
                          'markdown_name': 'Duration',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Specimen_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Specimen_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     'Duration']},
                         {'comment': 'Part of the cell from which the biosample was '
                          'taken',
                          'entity': True,
                          'markdown_name': 'Cellular Location',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Biosample_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Cellular_Location_Term_FKey']},
                                     'RID']},
                         ['Beta_Cell', 'Biosample_Specimen_Type_FKey'],
                         'Container_Id',
                         'Sample_Position',
                         'Collection_Date'],
                   'entry': [{'markdown_name': 'Dataset',
                              'source': [{'outbound': ['Beta_Cell',
                                                       'Biosample_Dataset_FKey']},
                                         'RID']},
                             {'markdown_name': 'Experiment',
                              'source': [{'outbound': ['Beta_Cell',
                                                       'Biosample_Experiment_FKey']},
                                         'RID']},
                             ['Beta_Cell', 'Biosample_Protocol_FKey'],
                             ['Beta_Cell', 'Biosample_Specimen_FKey'],
                             ['Beta_Cell', 'Biosample_Specimen_Type_FKey'],
                             'Container_Id',
                             {'source': [{'outbound': ['Beta_Cell',
                                                       'Biosample_Protocol_FKey']},
                                         'Description']},
                             'Sample_Position',
                             'collection_date'],
                   'filter': {'and': [{'entity': True, 'source': 'RID'},
                                      {'source': [{'outbound': ['Beta_Cell',
                                                                'Biosample_Dataset_FKey']},
                                                  'RID']},
                                      {'markdown_name': 'Cell Line',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Biosample_Specimen_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Specimen_Cell_Line_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Cell_Line_Cell_Line_Terms_FKey']},
                                                  'name']},
                                      {'comment': 'Part of the cell from which the '
                                       'biosample was taken',
                                       'entity': True,
                                       'markdown_name': 'Cellular Location',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Biosample_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Protocol_Step_Cellular_Location_Term_FKey']},
                                                  'name']},
                                      {'aggregate': 'array',
                                       'comment': 'Additives used to treat the cell '
                                       'line for the Experiment',
                                       'entity': True,
                                       'markdown_name': 'Additive',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Biosample_Specimen_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Specimen_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                                  'RID']},
                                      {'aggregate': 'array',
                                       'comment': 'Concentration of additive applied '
                                       'to cell line in mM',
                                       'entity': True,
                                       'markdown_name': 'Concentration',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Biosample_Specimen_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Specimen_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  'Additive_Concentration'],
                                       'ux_mode': 'choices'},
                                      {'aggregate': 'array',
                                       'comment': 'Duration in minutes of additive '
                                       'applied to cell line in ',
                                       'entity': True,
                                       'markdown_name': 'Duration',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Biosample_Specimen_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Specimen_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  'Duration'],
                                       'ux_mode': 'choices'},
                                      ['Beta_Cell', 'Biosample_Specimen_Type_FKey'],
                                      {'source': [{'inbound': ['isa',
                                                               'mesh_data_biosample_fkey']},
                                                  'url']},
                                      {'source': [{'inbound': ['Beta_Cell',
                                                               'XRay_Tomography_Data_Biosample_FKey']},
                                                  'RID']},
                                      {'source': [{'inbound': ['Beta_Cell',
                                                               'Processed_Tomography_Data_Biosample_FKey']},
                                                  'RID']},
                                      {'source': [{'inbound': ['Beta_Cell',
                                                               'Mass_Spec_Data_Biosample_FKey']},
                                                  'RID']},
                                      {'entity': True,
                                       'source': 'Container_Id',
                                       'ux_mode': 'choices'}]}}

visible_foreign_keys = {'*': [{'source': [{'inbound': ['Beta_Cell',
                                                       'XRay_Tomography_Data_Biosample_FKey']},
                                          'RID']},
                              {'source': [{'inbound': ['Beta_Cell',
                                                       'Processed_Tomography_Data_Biosample_FKey']},
                                          'RID']},
                              {'source': [{'inbound': ['Beta_Cell',
                                                       'Mass_Spec_Data_Biosample_FKey']},
                                          'RID']},
                              ['viz', 'model_biosample_fkey']]}

table_display = {
    'row_name': {
        'row_markdown_pattern': '{{RID}}{{#local_identifier}} '
        '{{Container_Id}}{{/local_identifier}}'}
}

table_alternatives = {}

export = {'templates': [{'format_name': 'BDBag (Holey)',
                         'format_type': 'BAG',
                         'name': 'default',
                         'outputs': [{'destination': {'name': 'Biosample',
                                                      'type': 'csv'},
                                      'source': {'api': 'entity',
                                                 'table': 'Beta_Cell:Biosample'}},
                                     {'destination': {'name': 'MRC',
                                                      'type': 'fetch'},
                                      'source': {'api': 'attribute',
                                                 'path': 'url:=URL,md5:=MD5,length:=Byte_Count',
                                                 'table': 'Beta_Cell:XRay_Tomography_Data'}},
                                     {'destination': {'name': 'processed_data',
                                                      'type': 'fetch'},
                                      'source': {'api': 'attribute',
                                                 'path': 'url:=URL,md5:=MD5,length:=Byte_Count',
                                                 'table': 'Beta_Cell:Processed_Tomography_Data'}},
                                     {'destination': {'name': 'OBJS',
                                                      'type': 'fetch'},
                                      'source': {'api': 'attribute',
                                                 'path': 'url',
                                                 'table': 'isa:mesh_data'}}]},
                        {'format_name': 'BDBag',
                            'format_type': 'BAG',
                            'name': 'default',
                         'outputs': [{'destination': {'name': 'Biosample',
                                                      'type': 'csv'},
                                      'source': {'api': 'entity',
                                                 'table': 'Beta_Cell:Biosample'}},
                                     {'destination': {'name': 'MRC',
                                                      'type': 'download'},
                                      'source': {'api': 'attribute',
                                                 'path': 'url:=URL',
                                                 'table': 'Beta_Cell:XRay_Tomography_Data'}},
                                     {'destination': {'name': 'processed_data',
                                                      'type': 'download'},
                                      'source': {'api': 'attribute',
                                                 'path': 'url:=URL',
                                                 'table': 'Beta_Cell:Processed_Tomography_Data'}},
                                     {'destination': {'name': 'OBJS',
                                                      'type': 'download'},
                                      'source': {'api': 'attribute',
                                                 'path': 'URL',
                                                 'table': 'isa:mesh_data'}}]}]}

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

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID', 'Dataset'],
                  constraint_names=[
                      ('Beta_Cell', 'Biosample_Dataset_RID_Key')],
                  annotations={'tag:misd.isi.edu,2015:display': {}},
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'Biosample_Key')],
                  annotations={'tag:misd.isi.edu,2015:display': {}},
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Dataset', 'Experiment'],
                         'Beta_Cell', 'Experiment', ['Dataset', 'RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Biosample_Experiment_Dataset_FKey')],
                         ),
    em.ForeignKey.define(['Specimen'],
                         'Beta_Cell', 'Specimen', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Biosample_Specimen_FKey')],
                         ),
    em.ForeignKey.define(['Specimen_Type'],
                         'vocab', 'specimen_type_terms', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Biosample_Specimen_Type_FKey')],
                         comment='Must be a valid reference to a specimen type.',
                         ),
    em.ForeignKey.define(['Protocol'],
                         'Beta_Cell', 'Protocol', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Biosample_Protocol_FKey')],
                         ),
    em.ForeignKey.define(['Dataset'],
                         'Beta_Cell', 'Dataset', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Biosample_Dataset_FKey')],
                         annotations={'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:foreign-key': {
                             'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.Biosample_Experiment_FKey.values._Dataset}}}'}},
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['Experiment'],
                         'Beta_Cell', 'Experiment', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Biosample_Experiment_FKey')],
                         annotations={'tag:misd.isi.edu,2015:display': {
                         }, 'tag:isrd.isi.edu,2016:foreign-key': {'domain_filter_pattern': 'Dataset={{{_Dataset}}}'}},
                         ),
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
