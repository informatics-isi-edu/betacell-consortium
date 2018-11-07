import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Processed_Tomography_Data'
schema_name = 'Beta_Cell'

column_annotations = {
    'File_Type': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_File_Type_FKey.rowName}}}'}}},
    'Process': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_process_FKey.rowName}}}'}}},
    'filename': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
            'markdown_pattern': 'Filename'}},
    'length': {
        'tag:isrd.isi.edu,2016:collumn-display': {
            'markdown_name': 'Length'}},
    'url': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'}},
        'tag:isrd.isi.edu,2017:asset': {
            'byte_count_column': 'length',
            'filename_column': 'filename',
            'md5': 'md5',
            'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{filename}}}'}}}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Dataset', em.builtin_types['text'], nullok=False,),
               em.Column.define('Process', em.builtin_types['text'], annotations=column_annotations['Process'],),
               em.Column.define('Data_Type', em.builtin_types['text'],),
               em.Column.define('File_Type', em.builtin_types['text'], nullok=False, annotations=column_annotations['File_Type'],),
               em.Column.define('Biosample', em.builtin_types['text'],),
               em.Column.define('filename', em.builtin_types['text'], nullok=False, annotations=column_annotations['filename'],),
               em.Column.define('url', em.builtin_types['text'], nullok=False, annotations=column_annotations['url'],),
               em.Column.define('length', em.builtin_types['int8'], nullok=False, annotations=column_annotations['length'],),
               em.Column.define('md5', em.builtin_types['text'], nullok=False,),
               ]

visible_columns = {'compact': [['Beta_Cell', 'Processed_Tomography_Data_Key'],
                               'Biosample',
                               'url',
                               'File_Type',
                               ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'],
                               'length',
                               'Submitted_On'],
                   'detailed': [['Beta_Cell', 'Processed_Tomography_Data_Key'],
                                ['Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey'],
                                ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey'],
                                ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'],
                                ['Beta_Cell', 'Processed_Tomography_Data_Output_Type_FKey'],
                                ['Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey'],
                                'length',
                                'md5',
                                'Submitted_On'],
                   'entry': ['RID',
                             {'markdown_name': 'Dataset',
                              'source': [{'outbound': ['Beta_Cell',
                                                       'Processed_Tomography_Data_Dataset_FKey']},
                                         'RID']},
                             ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey'],
                             ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'],
                             ['Beta_Cell', 'Processed_Tomography_Data_Output_Type_FKey'],
                             ['Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey'],
                             'url',
                             'Submitted_On'],
                   'filter': {'and': [{'entity': True, 'source': 'RID'},
                                      {'markdown_name': 'Dataset',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Processed_Tomography_Data_Dataset_FKey']},
                                                  'RID']},
                                      {'markdown_name': 'Cell Line',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Processed_Tomography_Data_Biosample_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Biosample_Specimen_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Specimen_Cell_Line_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Cell_Line_Cell_Line_Terms_FKey']},
                                                  'name']},
                                      {'aggregate': 'array',
                                       'comment': 'Additives used to treat the cell '
                                       'line for the experiment',
                                       'entity': True,
                                       'markdown_name': 'Additive',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Processed_Tomography_Data_Biosample_FKey']},
                                                  {'outbound': ['Beta_Cell',
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
                                                                'Processed_Tomography_Data_Biosample_FKey']},
                                                  {'outbound': ['Beta_Cell',
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
                                                                'Processed_Tomography_Data_Biosample_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Biosample_Specimen_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Specimen_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  'Duration'],
                                       'ux_mode': 'choices'},
                                      {'entity': True,
                                       'markdown_name': 'File Name',
                                       'open': False,
                                       'source': 'filename'},
                                      {'entity': True,
                                       'markdown_name': 'Anatomy',
                                       'open': True,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Processed_Tomography_Data_Anatomy_FKey']},
                                                  'id']},
                                      {'entity': True,
                                       'markdown_name': 'File Type',
                                       'open': True,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Processed_Tomography_Data_File_Type_FKey']},
                                                  'id']},
                                      {'entity': True,
                                       'markdown_name': 'Submitted On',
                                       'open': False,
                                       'source': 'Submitted_On'}]}}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'table_display': {
        'row_name': {
            'row_markdown_pattern': '{{{filename}}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'None'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[
                      ('Beta_Cell', 'Processed_Tomography_Data_Key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Dataset'],
                         'Beta_Cell', 'Dataset', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey')],
                         annotations={'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:foreign-key': {
                             'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.Processed_Tomography_Data_Biosample_FKey.values._Dataset}}}'}},
                         acls={'insert': ['*'], 'update': ['*']},
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['File_Type'],
                         'vocab', 'file_type_terms', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         ),
    em.ForeignKey.define(['Biosample', 'Dataset'],
                         'Beta_Cell', 'Biosample', ['RID', 'Dataset'],
                         constraint_names=[
                             ('Beta_Cell', 'Processed_Tomography_Data_Dataset_RID_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         comment='Ensure that the dataset for the file is the same as for the biosample',
                         ),
    em.ForeignKey.define(['Process'],
                         'isa', 'process', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Processed_Tomography_Data_Process_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         ),
    em.ForeignKey.define(['Biosample'],
                         'Beta_Cell', 'Biosample', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey')],
                         annotations={
                             'tag:isrd.isi.edu,2016:foreign-key': {'domain_filter_pattern': 'Dataset={{{_Dataset}}}'}},
                         acls={'insert': ['*'], 'update': ['*']},
                         on_update='CASCADE',
                         on_delete='RESTRICT',
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
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
