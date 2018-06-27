import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'dataset'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('accession', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('title', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('project', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('funding', em.builtin_types['text'],
    ),
    em.Column.define('summary', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('mouse_genetic', em.builtin_types['text'],
    ),
    em.Column.define('human_anatomic', em.builtin_types['text'],
    ),
    em.Column.define('study_design', em.builtin_types['markdown'],
    ),
    em.Column.define('release_date', em.builtin_types['date'],
    ),
    em.Column.define('status', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{ $fkeys.isa.dataset_status_fkey.rowName }}}'}}},
        acl_bindings={'dataset_edit_guard': False},
    ),
    em.Column.define('show_in_jbrowse', em.builtin_types['boolean'],
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Genome Browser'}, 'tag:isrd.isi.edu,2016:column-display': {'detailed': {'markdown_pattern': '{{#_show_in_jbrowse}}Use the embedded browser here or [view in a new window](/jbrowse/latest/?dataset={{{_RID}}}){target=_blank}.\n :::iframe [](/jbrowse/latest/?dataset={{{_RID}}}){width=800 height=600 .iframe} \n:::{{/_show_in_jbrowse}}'}}},
    ),
    em.Column.define('_keywords', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'dataset_RID_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('isa', 'dataset_pkey')],
    ),
    em.Key.define(['accession'],
                   constraint_names=[('isa', 'accession_unique')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['project'],
            'isa', 'project', ['id'],
            constraint_names=[('isa', 'dataset_project_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['status'],
            'vocab', 'dataset_status_terms', ['dbxref'],
            constraint_names=[('isa', 'dataset_status_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Status'}},
    ),
]


visible_columns=\
{'compact': [['isa', 'dataset_RID_key'], ['isa', 'accession_unique'], 'title',
             ['isa', 'dataset_project_fkey'], 'status', 'release_date'],
 'detailed': [['isa', 'dataset_RID_key'], 'accession', 'description',
              'study_design', ['isa', 'dataset_project_fkey'],
              ['isa', 'dataset_status_fkey'], 'funding', 'release_date',
              'show_in_jbrowse', ['isa', 'publication_dataset_fkey'],
              ['isa', 'dataset_experiment_type_dataset_id_fkey'],
              ['isa', 'dataset_data_type_dataset_id_fkey'],
              ['isa', 'dataset_phenotype_dataset_fkey'],
              ['isa', 'dataset_organism_dataset_id_fkey'],
              ['isa', 'dataset_anatomy_dataset_id_fkey'],
              ['isa', 'dataset_gender_dataset_id_fkey'],
              ['isa', 'dataset_instrument_dataset_id_fkey']],
 'entry': ['accession', 'title', ['isa', 'dataset_project_fkey'], 'description',
           'study_design', 'release_date', ['isa', 'dataset_status_fkey'],
           'show_in_jbrowse'],
 'filter': {'and': [{'entity': True,
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'dataset_organism_dataset_id_fkey']},
                                {'outbound': ['isa',
                                              'dataset_organism_organism_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'dataset_experiment_type_dataset_id_fkey']},
                                {'outbound': ['isa',
                                              'dataset_experiment_type_experiment_type_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'dataset_data_type_data_type_fkey']},
                                {'outbound': ['isa',
                                              'dataset_data_type_dataset_id_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'dataset_anatomy_dataset_id_fkey']},
                                {'outbound': ['isa',
                                              'dataset_anatomy_anatomy_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'dataset_phenotype_dataset_fkey']},
                                {'outbound': ['isa',
                                              'dataset_phenotype_phenotype_fkey']},
                                'dbxref']},
                    {'entity': True,
                     'markdown_name': 'Pubmed ID',
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'publication_dataset_fkey']},
                                'pmid']},
                    {'entity': True,
                     'markdown_name': 'Project Investigator',
                     'open': False,
                     'source': [{'outbound': ['isa', 'dataset_project_fkey']},
                                {'inbound': ['isa',
                                             'project_investigator_project_id_fkey']},
                                {'outbound': ['isa',
                                              'project_investigator_person_fkey']},
                                'RID']},
                    {'entity': False, 'open': False, 'source': 'accession'},
                    {'entity': False, 'open': False, 'source': 'title'},
                    {'entity': True,
                     'open': False,
                     'source': [{'outbound': ['isa', 'dataset_project_fkey']},
                                'id']},
                    {'entity': False, 'open': False, 'source': 'release_date'},
                    {'entity': True,
                     'open': False,
                     'source': [{'outbound': ['isa', 'dataset_status_fkey']},
                                'name']}]}}

visible_foreign_keys=\
{'*': [['isa', 'thumbnail_dataset_fkey'], ['viz', 'model_dataset_fkey'],
       ['isa', 'previews_dataset_id_fkey'], ['isa', 'experiment_dataset_fkey'],
       ['isa', 'biosample_dataset_fkey'], ['isa', 'enhancer_dataset_fkey'],
       ['isa', 'clinical_assay_dataset_fkey'], ['isa', 'file_dataset_fkey'],
       ['isa', 'external_reference_id_fkey']]}

table_display=\
{'*': {'row_order': [{'column': 'accession', 'descending': True}]},
 'row_name': {'row_markdown_pattern': '{{title}}'}}

table_acls={}
table_acl_bindings=\
{'dataset_edit_guard': {'projection': [{'outbound': ['isa',
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
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
}
column_annotations = \
{'accession': {'tag:isrd.isi.edu,2016:generated': None},
 'show_in_jbrowse': {'tag:isrd.isi.edu,2016:column-display': {'detailed': {'markdown_pattern': '{{#_show_in_jbrowse}}Use '
                                                                                               'the '
                                                                                               'embedded '
                                                                                               'browser '
                                                                                               'here '
                                                                                               'or '
                                                                                               '[view '
                                                                                               'in '
                                                                                               'a '
                                                                                               'new '
                                                                                               'window](/jbrowse/latest/?dataset={{{_RID}}}){target=_blank}.\n'
                                                                                               ' '
                                                                                               ':::iframe '
                                                                                               '[](/jbrowse/latest/?dataset={{{_RID}}}){width=800 '
                                                                                               'height=600 '
                                                                                               '.iframe} \n'
                                                                                               ':::{{/_show_in_jbrowse}}'}},
                     'tag:misd.isi.edu,2015:display': {'name': 'Genome '
                                                               'Browser'}},
 'status': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{ '
                                                                                     '$fkeys.isa.dataset_status_fkey.rowName '
                                                                                     '}}}'}}}}

column_acl_bindings = \
{'status': {'dataset_edit_guard': False}}



table_def = em.Table.define('dataset',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
