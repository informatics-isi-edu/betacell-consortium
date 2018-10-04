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
    em.Column.define('File_Type', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.XRay_Tomography_Data_File_Type_FKey.rowName}}}'}}},
        comment='None',
    ),
    em.Column.define('Submitted_On', em.builtin_types['timestamptz'],
        comment='None',
    ),
    em.Column.define('File_Id', em.builtin_types['int4'],
        comment='None',
    ),
    em.Column.define('Biosample', em.builtin_types['ermrest_rid'],
        comment='Biosample from which this X Ray Tomography data was obtained',
    ),
    em.Column.define('md5', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('length', em.builtin_types['int8'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:collumn-display': {'markdown_name': 'Length'}},
    ),
    em.Column.define('url', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'length', 'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{filename}}}', 'md5': 'md5'}, 'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'markdown_pattern': 'Filename'}},
    ),
]


key_defs = [
    em.Key.define(['Dataset', 'RID'],
                   constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Dataset_RID_Key')],
       comment = 'RID and dataset must be distinct.',
    ),
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_RIDkey1')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Biosample'],
            'Beta_Cell', 'Biosample', ['RID'],
            constraint_names=[('Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'domain_filter_pattern': 'Dataset={{{_Dataset}}}'}},
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['Dataset', 'Biosample'],
            'Beta_Cell', 'Biosample', ['Dataset', 'RID'],
            constraint_names=[('Beta_Cell', 'XRay_Tomography_Dataset_RID_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Ensure that the dataset for the file is the same as for the biosample',
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
       'filename', 'Description',
       ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'], 'length',
       'submitted_on'],
 'entry': ['RID', ['Beta_Cell', 'XRay_Tomography_Data_Dataset_FKey'],
           ['Beta_Cell', 'XRay_Tomography_Data_Biosample_FKey'], 'Description',
           'url', ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'],
           'filename', ['Beta_Cell', 'XRay_Tomography_Data_File_Type_FKey'],
           'length', 'md5', 'submitted_on'],
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
                                {'outbound': ['Beta_Cell',
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
                     'source': 'filename'},
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
{'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

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
 'Dataset': 'None',
 'Description': 'None',
 'File_Id': 'None',
 'File_Type': 'None',
 'Submitted_On': 'None'}

column_annotations = \
{'File_Type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.Beta_Cell.XRay_Tomography_Data_File_Type_FKey.rowName}}}'}}},
 'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'markdown_pattern': 'Filename'}},
 'length': {'tag:isrd.isi.edu,2016:collumn-display': {'markdown_name': 'Length'}},
 'url': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                  'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}},
         'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'length',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{_Dataset}}}/{{{_Biosample}}}/{{{filename}}}'}}}



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
