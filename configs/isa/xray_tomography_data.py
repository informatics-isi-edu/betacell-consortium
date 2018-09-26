import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'xray_tomography_data'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
        comment='None',
    ),
    em.Column.define('description', em.builtin_types['markdown'],
        comment='None',
    ),
    em.Column.define('url', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}', 'md5': 'md5'}},
        comment='None',
    ),
    em.Column.define('filename', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
        comment='None',
    ),
    em.Column.define('file_type', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.xray_tomography_data_file_type_fkey.rowName}}}'}}},
        comment='None',
    ),
    em.Column.define('byte_count', em.builtin_types['int8'],
        comment='None',
    ),
    em.Column.define('submitted_on', em.builtin_types['timestamptz'],
        comment='None',
    ),
    em.Column.define('md5', em.builtin_types['text'],
        comment='None',
    ),
    em.Column.define('file_id', em.builtin_types['int4'],
        comment='None',
    ),
    em.Column.define('biosample', em.builtin_types['ermrest_rid'],
        comment='Biosample from which this X Ray Tomography data was obtained',
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'xray_tomography_data_RIDkey1')],
    ),
    em.Key.define(['dataset', 'RID'],
                   constraint_names=[('isa', 'xray_tomography_data_dataset_RID_key')],
       comment = 'RID and dataset must be distinct.',
    ),
    em.Key.define(['url'],
                   constraint_names=[('isa', 'xray_tomography_data_url_key')],
       comment = 'Unique URL must be provided.',
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'xray_tomography_dataset_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
        comment='Must be a valid reference to a dataset.',
    ),
    em.ForeignKey.define(['biosample'],
            'isa', 'biosample', ['RID'],
            constraint_names=[('isa', 'xray_tomography_data_biosample_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['biosample', 'dataset'],
            'isa', 'biosample', ['RID', 'dataset'],
            constraint_names=[('isa', 'xray_tomography_dataset_rid_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Ensure that the dataset for the file is the same as for the biosample',
    ),
]


visible_columns = \
{'*': [['isa', 'xray_tomography_data_pkey'],
       ['isa', 'xray_tomography_data_dataset_fkey'],
       ['isa', 'xray_tomography_data_biosample_fkey'],
       ['isa', 'xray_tomography_data_device_fkey'], 'filename',
       ['isa', 'xray_tomography_data_file_type_fkey'], 'byte_count', 'md5',
       'submitted_on'],
 'entry': ['RID', ['isa', 'xray_tomography_data_biosample_fkey'],
           ['isa', 'xray_tomography_data_device_fkey'],
           ['isa', 'xray_tomography_data_equipment_model_fkey'], 'description',
           'url', ['isa', 'xray_tomography_data_file_type_fkey'], 'filename',
           ['isa', 'xray_tomography_data_file_type_fkey'], 'byte_count', 'md5',
           'submitted_on'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Cell Line',
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_biosample_fkey']},
                                {'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                {'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'entity': True,
                     'markdown_name': 'Compound',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_biosample_fkey']},
                                {'outbound': ['isa',
                                              'biosample_experiment_fkey']},
                                {'outbound': ['isa',
                                              'experiment_protocol_fkey']},
                                {'inbound': ['isa',
                                             'protocol_compound_protocol_fkey']},
                                {'outbound': ['isa',
                                              'protocol_compound_compound_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Compound Concentration',
                     'open': False,
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_biosample_fkey']},
                                {'outbound': ['isa',
                                              'biosample_experiment_fkey']},
                                {'outbound': ['isa',
                                              'experiment_protocol_fkey']},
                                {'inbound': ['isa',
                                             'protocol_compound_protocol_fkey']},
                                'compound_concentration'],
                     'ux_mode': 'choices'},
                    {'entity': True,
                     'markdown_name': 'Timepoint',
                     'open': False,
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_biosample_fkey']},
                                {'outbound': ['isa',
                                              'biosample_experiment_fkey']},
                                {'outbound': ['isa',
                                              'experiment_protocol_fkey']},
                                'timepoint'],
                     'ux_mode': 'choices'},
                    {'entity': True,
                     'markdown_name': 'File Name',
                     'open': False,
                     'source': 'filename'},
                    {'entity': True,
                     'markdown_name': 'Anatomy',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_anatomy_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Imaging Device',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_device_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Equipment Model',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_equipment_model_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'File Type',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'xray_tomography_data_file_type_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Submitted On',
                     'open': False,
                     'source': 'submitted_on'}]}}

visible_foreign_keys = \
{'detailed': [['isa', 'thumbnail_thumbnail_of_fkey'],
              ['isa', 'mesh_data_derived_from_fkey']],
 'entry': [['isa', 'thumbnail_thumbnail_of_fkey'],
           ['isa', 'mesh_data_derived_from_fkey']]}

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
{'biosample': 'Biosample from which this X Ray Tomography data was obtained',
 'byte_count': 'None',
 'dataset': 'None',
 'description': 'None',
 'file_id': 'None',
 'file_type': 'None',
 'filename': 'None',
 'md5': 'None',
 'submitted_on': 'None',
 'url': 'None'}

column_annotations = \
{'file_type': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.xray_tomography_data_file_type_fkey.rowName}}}'}}},
 'filename': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
                                                       'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
 'url': {'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                         'filename_column': 'filename',
                                         'md5': 'md5',
                                         'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}'}}}



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
