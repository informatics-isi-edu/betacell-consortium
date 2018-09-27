import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Processed_Tomography_Data'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Dataset', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('Process', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_process_FKey.rowName}}}'}}},
    ),
    em.Column.define('URL', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'Filename', 'byte_count_column': 'Byte_Count', 'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{Filename}}}', 'md5': 'MD5'}, 'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}, 'detailed': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}}},
    ),
    em.Column.define('Filename', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}, 'detailed': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}}},
    ),
    em.Column.define('Data_Type', em.builtin_types['text'],
    ),
    em.Column.define('File_Type', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_File_Type_FKey.rowName}}}'}}},
    ),
    em.Column.define('Byte_Count', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('MD5', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('Biosample', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['URL'],
                   constraint_names=[('isa', 'Processed_Tomography_Data_URL_Key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'Processed_Tomography_Data_Key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey')],
                         annotations={'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:foreign-key': {
                             'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.Processed_Tomography_Data_Biosample_FKey.values._Dataset}}}'}},
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['Biosample'],
            'Beta_Cell', 'Biosample', ['RID'],
                         annotations={'tag:isrd.isi.edu,2016:foreign-key': {
                             'domain_filter_pattern': 'Dataset={{{_Dataset}}}'}},
            constraint_names=[('Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['Biosample', 'Dataset'],
                         'Beta_Cell', 'Biosample', ['RID', 'Dataset'],
                         constraint_names=[('isa', 'Processed_Tomography_Data_Dataset_RID_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         comment='Ensure that the dataset for the file is the same as for the biosample',
                         ),
    em.ForeignKey.define(['Process'],
            'isa', 'process', ['RID'],
            constraint_names=[('isa', 'Processed_Tomography_Data_Process_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['File_Type'],
            'vocab', 'file_type_terms', ['id'],
            constraint_names=[('isa', 'Processed_Tomography_Data_File_Type_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns = \
{'compact': [['Beta_Cell', 'Processed_Tomography_Data_Key'], 'Biosample', 'URL',
             'File_Type',  'Pipeline', 'Byte_Count',
             'submitted_on'],
 'detailed': [['Beta_Cell', 'Processed_Tomography_Data_Key'],
              ['Beta_Cell', 'Processed_Tomography_Data_Dataset_FKey'],
              ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey'],
              ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'],
              ['Beta_Cell', 'Processed_Tomography_Data_Output_Type_FKey'],
              ['Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey'], 'Byte_Count',
              'MD5', 'Submitted_On'],
 'entry': ['RID', ['isa', 'Processed_Tomography_Data_Dataset_FKey'],
           ['Beta_Cell', 'Processed_Tomography_Data_Biosample_FKey'],
           ['Beta_Cell', 'Processed_Tomography_Data_Process_FKey'],
           ['Beta_Cell', 'Processed_Tomography_Data_Output_Type_FKey'],
           ['Beta_Cell', 'Processed_Tomography_Data_File_Type_FKey'], 'URL',
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
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                {'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'aggregate': 'array',
                     'comment': 'Additives used to treat the cell line for the '
                                'experiment',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'outbound': ['Beta_Cell',
                                              'Processed_Tomography_Data_Biosample_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                'RID']},
                    {'aggregate': 'array',
                     'comment': 'Concentration of additive applied to cell '
                                'line in mM',
                     'entity': True,
                     'markdown_name': 'Concentration',
                     'source': [{'outbound': ['Beta_Cell',
                                              'Processed_Tomography_Data_Biosample_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Protocol_FKey']},
                                {'inbound': ['Beta_Cell',
                                             'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                'Additive_Concentration'],
                     'ux_mode': 'choices'},
                    {'aggregate': 'array',
                     'comment': 'Duration in minutes of additive applied to '
                                'cell line in ',
                     'entity': True,
                     'markdown_name': 'Duration',
                     'source': [{'outbound': ['Beta_Cell',
                                              'Processed_Tomography_Data_Biosample_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['isa', 'specimen_protocol_fkey']},
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
table_comment = \
'None'

table_display = \
{'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "table_display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_annotations = \
{'file_type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_file_type_FKey.rowName}}}'}}},
 'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{URL}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{URL}}})'}}},
 'process': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.Processed_Tomography_Data_process_FKey.rowName}}}'}}},
 'submitted_on': {'tag:isrd.isi.edu,2016:immutable': None},
 'URL': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{URL}}})'},
                                                  'detailed': {'markdown_pattern': '[**{{filename}}**]({{{URL}}})'}},
         'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{Gilename}}}'}}}



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
