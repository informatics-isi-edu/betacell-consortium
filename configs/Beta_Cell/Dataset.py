import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Dataset'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Title', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('Project', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('Summary', em.builtin_types['text'],
    ),
    em.Column.define('Description', em.builtin_types['markdown'],
    ),
    em.Column.define('Human_anatomic', em.builtin_types['text'],
    ),
    em.Column.define('Study_design', em.builtin_types['markdown'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'dataset_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['RCB'],
            'public', 'ermrest_client', ['id'],
            constraint_names=[('Beta_Cell', 'dataset_rcb_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['Project'],
            'Beta_Cell', 'project', ['id'],
            constraint_names=[('Beta_Cell', 'dataset_project_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns = \
{'compact': [['Beta_Cell', 'dataset_RID_key'],
             {'source': [{'outbound': ['Beta_Cell', 'dataset_rcb_fkey']},
                         'display_name']},
             'title', ['Beta_Cell', 'dataset_project_fkey'], 'status',
             'release_date'],
 'detailed': [['Beta_Cell', 'dataset_RID_key'], 'description', 'study_design',
              ['Beta_Cell', 'dataset_project_fkey'], ['Beta_Cell', 'dataset_status_fkey'],
              'funding', 'release_date', ['Beta_Cell', 'publication_dataset_fkey'],
              ['Beta_Cell', 'dataset_experiment_type_dataset_id_fkey'],
              ['Beta_Cell', 'dataset_data_type_dataset_id_fkey'],
              ['Beta_Cell', 'dataset_anatomy_dataset_id_fkey'],
              ['Beta_Cell', 'dataset_instrument_dataset_id_fkey']],
 'entry': ['accession', 'RCB', 'title', ['Beta_Cell', 'dataset_project_fkey'],
           'description', 'study_design', 'release_date',
           ['Beta_Cell', 'dataset_status_fkey']],
 'filter': {'and': [{'entity': True,
                     'open': False,
                     'source': [{'inbound': ['Beta_Cell',
                                             'dataset_experiment_type_dataset_id_fkey']},
                                {'outbound': ['Beta_Cell',
                                              'dataset_experiment_type_experiment_type_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'open': False,
                     'source': [{'inbound': ['Beta_Cell',
                                             'dataset_data_type_data_type_fkey']},
                                {'outbound': ['Beta_Cell',
                                              'dataset_data_type_dataset_id_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'open': False,
                     'source': [{'inbound': ['Beta_Cell',
                                             'dataset_anatomy_dataset_id_fkey']},
                                {'outbound': ['Beta_Cell',
                                              'dataset_anatomy_anatomy_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'markdown_name': 'Project Investigator',
                     'open': False,
                     'source': [{'outbound': ['Beta_Cell', 'dataset_project_fkey']},
                                {'inbound': ['isa',
                                             'project_investigator_project_id_fkey']},
                                {'outbound': ['isa',
                                              'project_investigator_person_fkey']},
                                'RID']},
                    {'entity': False, 'open': False, 'source': 'title'},
                    {'entity': True,
                     'open': False,
                     'source': [{'outbound': ['Beta_Cell', 'dataset_project_fkey']},
                                'id']},
                    {'entity': False, 'open': False, 'source': 'release_date'},
                    {'entity': True,
                     'open': False,
                     'source': [{'outbound': ['Beta_Cell', 'dataset_status_fkey']},
                                'name']}]}}

visible_foreign_keys = \
{'*': [['viz', 'model_dataset_fkey'], ['Beta_Cell', 'experiment_dataset_fkey'],
       ['Beta_Cell', 'Biosample_Dataset_FKey'], ['Beta_Cell', 'file_dataset_fkey']]}

table_comment = \
None

table_display = \
{'*': {'row_order': [{'column': 'accession', 'descending': True}]},
 'row_name': {'row_markdown_pattern': '{{title}}'}}

table_acls = {}
table_acl_bindings = \
{'dataset_edit_guard': {'projection': [{'outbound': ['Beta_Cell',
                                                     'dataset_project_fkey']},
                                       {'outbound': ['isa',
                                                     'project_groups_fkey']},
                                       'groups'],
                        'projection_type': 'acl',
                        'scope_acl': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                      'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                      'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                        'types': ['update', 'delete']}}

table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}

column_annotations = \
{}



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
