import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'sample'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('dataset', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('replicate', em.builtin_types['text'],
    ),
    em.Column.define('local_identifier', em.builtin_types['text'],
    ),
    em.Column.define('species', em.builtin_types['text'],
    ),
    em.Column.define('specimen', em.builtin_types['text'],
    ),
    em.Column.define('origin', em.builtin_types['text'],
    ),
    em.Column.define('anatomy', em.builtin_types['text'],
    ),
    em.Column.define('phenotype', em.builtin_types['text'],
    ),
    em.Column.define('gender', em.builtin_types['text'],
    ),
    em.Column.define('collection_date', em.builtin_types['date'],
    ),
    em.Column.define('_keywords', em.builtin_types['text'],
    ),
    em.Column.define('replicate_group', em.builtin_types['text'],
    ),
    em.Column.define('cell_line', em.builtin_types['text'],
        comment='Cell line used for the sample.',
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('isa', 'sample_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'sample_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['id'],
            constraint_names=[('isa', 'sample_dataset_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {}},
    ),
    em.ForeignKey.define(['replicate_group'],
            'isa', 'sample_replicate_group', ['RID'],
            constraint_names=[('isa', 'sample_replicate_group_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(['phenotype'],
            'vocab', 'phenotype_terms', ['dbxref'],
            constraint_names=[('isa', 'sample_phenotype_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Phenotype'}},
    ),
    em.ForeignKey.define(['specimen'],
            'vocab', 'specimen_terms', ['dbxref'],
            constraint_names=[('isa', 'sample_specimen_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Specimen'}},
    ),
]


visible_columns = \
{'compact': [['isa', 'sample_pkey'], 'local_identifier',
             ['isa', 'sample_species_fkey'], ['isa', 'sample_genotype_fkey'],
             ['isa', 'sample_strain_fkey'], ['isa', 'sample_stage_fkey'],
             ['isa', 'sample_anatomy_fkey'], 'origin',
             ['isa', 'sample_phenotype_fkey'],
             ['isa', 'sample_specimen_fkey']],
 'detailed': ['id', 'local_identifier', ['isa', 'sample_dataset_fkey'],
              ['isa', 'sample_species_fkey'], ['isa', 'sample_genotype_fkey'],
              ['isa', 'sample_strain_fkey'], 'gender',
              ['isa', 'sample_stage_fkey'],
              ['isa', 'sample_theiler_stage_fkey'],
              ['isa', 'sample_anatomy_fkey'], 'origin',
              ['isa', 'sample_phenotype_fkey'], ['isa', 'sample_specimen_fkey'],
              'litter', 'collection_date'],
 'entry': ['id', ['isa', 'sample_dataset_fkey'], 'local_identifier',
           ['isa', 'sample_replicate_group_fkey'],
           ['isa', 'sample_species_fkey'], ['isa', 'sample_specimen_fkey'],
           ['isa', 'sample_gene_fkey'], ['isa', 'sample_genotype_fkey'],
           ['isa', 'sample_strain_fkey'], 'mutation',
           ['isa', 'sample_stage_fkey'], ['isa', 'sample_theiler_stage_fkey'],
           ['isa', 'sample_phenotype_fkey'], ['isa', 'sample_anatomy_fkey'],
           'origin', 'litter', 'gender', 'collection_date'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Species',
                     'open': True,
                     'source': [{'outbound': ['isa', 'sample_species_fkey']},
                                'term']},
                    {'entity': True,
                     'markdown_name': 'Stage',
                     'open': False,
                     'source': [{'outbound': ['isa', 'sample_stage_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Anatomy',
                     'open': False,
                     'source': [{'outbound': ['isa', 'sample_anatomy_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Phenotype',
                     'open': False,
                     'source': [{'outbound': ['isa', 'sample_phenotype_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Genotype',
                     'open': False,
                     'source': [{'outbound': ['isa', 'sample_genotype_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Strain',
                     'open': False,
                     'source': [{'outbound': ['isa', 'sample_strain_fkey']},
                                'id']},
                    {'entity': True,
                     'markdown_name': 'Local Identifier',
                     'open': False,
                     'source': 'local_identifier'}]}}

visible_foreign_keys = \
{'detailed': [['isa', 'assay_sample_fkey'], ['isa', 'imaging_sample_fkey'],
              ['isa', 'enhancer_sample_fkey']]}

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp',
 'cell_line': 'Cell line used for the sample.'}



table_def = em.Table.define('sample',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
