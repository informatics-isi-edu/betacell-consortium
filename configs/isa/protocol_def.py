import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'protocol'
schema_name = 'isa'

column_defs = [
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
        comment='Provide a name that uniquely identifies the protocol',
    ),
    em.Column.define('protocol_url', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('file_url', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/documents/protocol/{{{md5}}}', 'md5': 'md5'}},
    ),
    em.Column.define('filename', em.builtin_types['text'],
    ),
    em.Column.define('byte_count', em.builtin_types['int4'],
    ),
    em.Column.define('md5', em.builtin_types['text'],
    ),
    em.Column.define('assay_ids', em.builtin_types['int4[]'],
    ),
    em.Column.define('timepoint', em.builtin_types['int2'],
        comment='Measured in minutes.',
    ),
]


key_defs = [
    em.Key.define(['description'],
                   constraint_names=[('isa', 'protocol_description_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'protocol_pkey')],
    ),
    em.Key.define(['name'],
                   constraint_names=[('isa', 'protocol_name_key')],
    ),
]


fkey_defs = [
]


visible_columns=\
{'compact': [['isa', 'protocol_pkey'], 'name',
             {'aggregate': 'array',
              'entity': True,
              'markdown_name': 'Treatment',
              'source': [{'inbound': ['isa',
                                      'protocol_treatment_protocol_fkey']},
                         {'outbound': ['isa',
                                       'protocol_treatment_treatment_fkey']},
                         'RID']},
             {'aggregate': 'array',
              'entity': True,
              'markdown_name': 'Concentration',
              'source': [{'inbound': ['isa',
                                      'protocol_treatment_protocol_fkey']},
                         'treatment_concentration']},
             {'aggregate': 'array', 'entity': True, 'source': ['timepoint']},
             'description'],
 'detailed': [['isa', 'protocol_pkey'], 'name', 'timepoint', 'description'],
 'entry': ['RID', 'name', 'treatment', 'treatment_concentration', 'timepoint',
           'protocol_url', 'description', 'file_url', 'filename'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Protocol Name',
                     'open': False,
                     'source': 'name'},
                    {'entity': True,
                     'markdown_name': 'Treatment',
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'protocol_treatment_protocol_fkey']},
                                {'outbound': ['isa',
                                              'protocol_treatment_treatment_fkey']},
                                'RID']},
                    {'entity': True,
                     'markdown_name': 'Treatment Concentration',
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'protocol_treatment_protocol_fkey']},
                                'treatment_concentration'],
                     'ux_mode': 'choices'},
                    {'entity': True,
                     'markdown_name': 'Timepoint',
                     'open': False,
                     'source': 'timepoint',
                     'ux_mode': 'choices'},
                    {'entity': True,
                     'markdown_name': 'Protocol Description',
                     'open': False,
                     'source': 'description'}]}}

visible_foreign_keys=\
{'detailed': [['isa', 'protocol_treatment_protocol_fkey'],
              ['isa', 'experiment_protocol_fkey']],
 'entry': [['isa', 'experiment_protocol_fkey']]}

table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:misd.isi.edu,2015:display":
{'name': 'Protocol'}
,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}
column_annotations = \
{'file_url': {'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                              'filename_column': 'filename',
                                              'md5': 'md5',
                                              'url_pattern': '/hatrac/commons/documents/protocol/{{{md5}}}'}}}



table_def = em.Table.define('protocol',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
