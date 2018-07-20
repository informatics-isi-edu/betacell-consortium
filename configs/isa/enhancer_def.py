import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'enhancer'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('original_species_assembly', em.builtin_types['text'],
    ),
    em.Column.define('original_species_chromosome', em.builtin_types['text'],
    ),
    em.Column.define('original_species_start', em.builtin_types['int4'],
    ),
    em.Column.define('original_species_end', em.builtin_types['int4'],
    ),
    em.Column.define('visualization_assembly', em.builtin_types['text'],
    ),
    em.Column.define('visualization_assembly_chromosome', em.builtin_types['text'],
    ),
    em.Column.define('visualization_assembly_start', em.builtin_types['int4'],
    ),
    em.Column.define('visualization_assembly_end', em.builtin_types['int4'],
    ),
    em.Column.define('other_assembly', em.builtin_types['text'],
    ),
    em.Column.define('other_assembly_chromosome', em.builtin_types['text'],
    ),
    em.Column.define('other_assembly_start', em.builtin_types['int4'],
    ),
    em.Column.define('other_assembly_end', em.builtin_types['int4'],
    ),
    em.Column.define('tested_sequence', em.builtin_types['gene_sequence'],
    ),
    em.Column.define('tested_sequence_flag', em.builtin_types['text'],
    ),
    em.Column.define('list_of_closest_genes', em.builtin_types['text'],
    ),
    em.Column.define('external_database_name', em.builtin_types['text'],
    ),
    em.Column.define('external_id', em.builtin_types['text'],
    ),
    em.Column.define('list_of_anatomical_structures', em.builtin_types['text'],
    ),
    em.Column.define('lab_internal_reference', em.builtin_types['text'],
    ),
    em.Column.define('sample', em.builtin_types['int4'],
    ),
    em.Column.define('dataset', em.builtin_types['int4'],
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('isa', 'enhancer_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'enhancer_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['id'],
            constraint_names=[('isa', 'enhancer_dataset_fkey')],
    ),
    em.ForeignKey.define(['sample'],
            'isa', 'sample', ['id'],
            constraint_names=[('isa', 'enhancer_sample_fkey')],
    ),
]


visible_columns=\
{'compact': [['isa', 'enhancer_pkey'], 'original_species_assembly',
             'original_species_chromosome', 'original_species_start',
             'original_species_end', 'list_of_closest_genes',
             'list_of_anatomical_structures'],
 'detailed': [['isa', 'enhancer_dataset_fkey'], ['isa', 'enhancer_sample_fkey'],
              'original_species_assembly', 'original_species_chromosome',
              'original_species_start', 'original_species_end',
              'visualization_assembly', 'visualization_assembly_chromosome',
              'visualization_assembly_start', 'visualization_assembly_end',
              'other_assembly', 'other_assembly_chromosome',
              'other_assembly_start', 'other_assembly_end', 'tested_sequence',
              'tested_sequence_flag', 'list_of_closest_genes',
              'external_database_name', 'external_id',
              'list_of_anatomical_structures', 'lab_internal_reference'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Species',
                     'open': True,
                     'source': [{'outbound': ['isa', 'enhancer_sample_fkey']},
                                {'outbound': ['isa', 'sample_species_fkey']},
                                'term']},
                    {'entity': True,
                     'markdown_name': 'Stage',
                     'open': False,
                     'source': [{'outbound': ['isa', 'enhancer_sample_fkey']},
                                {'outbound': ['isa', 'sample_stage_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Original Species Assembly',
                     'open': False,
                     'source': 'original_species_assembly'},
                    {'entity': True,
                     'markdown_name': 'Original Species Chromosome',
                     'open': False,
                     'source': 'original_species_chromosome'}]}}

visible_foreign_keys={}
table_display=\
{'row_name': {'row_markdown_pattern': '{{{original_species_chromosome}}}:{{{original_species_start}}}-{{{original_species_end}}}'}}

table_acls={}
table_acl_bindings=\
{'curated_status_guard': {'projection': [{'outbound': ['isa',
                                                       'enhancer_dataset_fkey']},
                                         {'filter': 'status',
                                          'operand': 'commons:226:',
                                          'operator': '='},
                                         'RID'],
                          'projection_type': 'nonnull',
                          'scope_acl': ['*'],
                          'types': ['select']},
 'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'enhancer_dataset_fkey']},
                                             {'outbound': ['isa',
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
    "tag:misd.isi.edu,2015:display":
{'name': 'Enhancer Reporter Assay'}
,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
}


table_def = em.Table.define('enhancer',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
