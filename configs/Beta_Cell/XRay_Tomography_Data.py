import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'XRay_Tomography_Data'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Dataset', em.builtin_types['text'],
        nullok=False,
        comment='None',
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
        comment='None',
    ),
    em.Column.define('URL', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'Filename', 'byte_count_column': 'Byte_Count', 'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{Filename}}}', 'md5': 'MD5'}},
        comment='None',
    ),
    em.Column.define('Filename', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}, 'detailed': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}}},
        comment='None',
    ),
    em.Column.define('File_Type', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.XRay_Tomography_Data_File_Type_FKey.rowName}}}'}}},
        comment='None',
    ),
    em.Column.define('Byte_Count', em.builtin_types['int8'],
        comment='None',
    ),
    em.Column.define('Submitted_On', em.builtin_types['timestamptz'],
        comment='None',
    ),
    em.Column.define('MD5', em.builtin_types['text'],
        comment='None',
    ),
    em.Column.define('File_Id', em.builtin_types['int4'],
        comment='None',
    ),
    em.Column.define('Biosample', em.builtin_types['ermrest_rid'],
        comment='Biosample from which this X Ray Tomography data was obtained',
    ),
]


key_defs = [
    em.Key.define(['URL'],
                   constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Url_Key')],
       comment = 'Unique URL must be provided.',
    ),
    em.Key.define(['RID', 'Dataset'],
                   constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Dataset_RID_Key')],
       comment = 'RID and dataset must be distinct.',
    ),
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_RIDkey1')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Dataset', 'Biosample'],
            'Beta_Cell', 'Biosample', ['Dataset', 'RID'],
            constraint_names=[('Beta_Cell', 'XRay_Tomography_Dataset_RID_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Ensure that the dataset for the file is the same as for the biosample',
    ),
    em.ForeignKey.define(['Biosample'],
            'Beta_Cell', 'Biosample', ['RID'],
            constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'domain_filter_pattern': 'Dataset={{{_Dataset}}}'}},
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['Dataset'],
            'Beta_Cell', 'Dataset', ['RID'],
            constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Dataset_FKey')],
        annotations={'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:foreign-key': {'domain_filter_pattern': 'RID={{{$fkeys.Beta_Cell.XRay_Tomography_Data_Biosample_FKey.values._Dataset}}}'}},
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
        comment='Must be a valid reference to a dataset.',
    ),
]


visible_columns = \
{'*': [['Beta_Cell', 'XRay_Tomography_Data_Key'],
       {'markdown_name': 'Dataset',
        'source': [{'outbound': ['Beta_Cell',
                                 'XRay_Tomography_Data_Dataset_FKey']},
                   'RID']},
       {'markdown_name': 'Biosample',
        'source': [{'outbound': ['Beta_Cell',
                                 'XRay_Tomography_Data_Biosample_FKey']},
                   'RID']},
       'Filename', 'Description',
       ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'], 'Byte_Count',
       'submitted_on'],
 'entry': ['RID',
           {'markdown_name': 'Dataset',
            'source': [{'outbound': ['Beta_Cell',
                                     'XRay_Tomography_Data_Dataset_FKey']},
                       'RID']},
           {'markdown_name': 'Biosample',
            'source': [{'outbound': ['Beta_Cell',
                                     'XRay_Tomography_Data_Biosample_FKey']},
                       'RID']},

           'Description',

           'URL', ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'],
           'Filename', ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'],
           'Byte_Count', 'MD5', 'submitted_on'],
 'filter': {'and': [{'entity': True, 'source': 'RID'},
                    {'markdown_name': 'Dataset',
                     'source': [{'outbound': ['Beta_Cell',
                                              'XRay_Tomography_Data_Dataset_FKey']},
                                'RID']},
                    {'markdown_name': 'Cell Line',
                     'source': [{'outbound': ['Beta_Cell',
                                              'XRay_Tomography_Data_Biosample_FKey']},
                                {'outbound': ['Beta_Cell',
                                              'Biosample_Specimen_FKey']},
                                {'outbound': ['isa',
                                              'Specimen_Cell_Line_FKey']},
                                {'outbound': ['isa',
                                              'Cell_Line_Cell_Line_Terms_FKey']},
                                'name']},
                    {'aggregate': 'array',
                     'comment': 'Additives used to treat the cell line for the '
                                'experiment',
                     'entity': True,
                     'markdown_name': 'Additive',
                     'source': [{'outbound': ['Beta_Cell',
                                              'XRay_Tomography_Data_Biosample_FKey']},
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
                     'comment': 'Concentration of additive applied to cell '
                                'line in mM',
                     'entity': True,
                     'markdown_name': 'Concentration',
                     'source': [{'outbound': ['Beta_Cell',
                                              'XRay_Tomography_Data_Biosample_FKey']},
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
                     'comment': 'Duration in minutes of additive applied to '
                                'cell line in ',
                     'entity': True,
                     'markdown_name': 'Duration',
                     'source': [{'outbound': ['Beta_Cell',
                                              'XRay_Tomography_Data_Biosample_FKey']},
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
                     'source': 'Filename'},
                    {'entity': True,
                     'markdown_name': 'Anatomy',
                     'open': True,
                     'source': [{'outbound': ['Beta_Cell',
                                              'XRay_Tomography_Data_Anatomy_FKey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'File Type',
                     'open': True,
                     'source': [{'outbound': ['Beta_Cell',
                                              'XRay_Tomography_Data_File_Type_FKey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Submitted On',
                     'open': False,
                     'source': 'submitted_on'}]}}

visible_foreign_keys = \
{'detailed': [['isa', 'mesh_data_derived_from_fkey']],
 'entry': [['isa', 'mesh_data_derived_from_fkey']]}

table_comment = \
'Table to hold X-Ray Tomography MRC files.'

table_display = \
{'row_name': {'row_markdown_pattern': '{{{Filename}}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "table_display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Biosample': 'Biosample from which this X Ray Tomography data was obtained',
 'Byte_Count': 'None',
 'Dataset': 'None',
 'Description': 'None',
 'File_Id': 'None',
 'File_Type': 'None',
 'Filename': 'None',
 'MD5': 'None',
 'Submitted_On': 'None',
 'URL': 'None'}

column_annotations = \
{'File_Type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.XRay_Tomography_Data_File_Type_FKey.rowName}}}'}}},
 'Filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}}},
 'URL': {'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'Byte_Count',
                                         'filename_column': 'Filename',
                                         'md5': 'MD5',
                                         'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{Filename}}}'}}}



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
