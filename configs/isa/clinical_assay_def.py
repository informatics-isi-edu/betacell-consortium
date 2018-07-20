import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'clinical_assay'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('dataset', em.builtin_types['int4'],
    ),
    em.Column.define('local_id', em.builtin_types['text'],
    ),
    em.Column.define('family_id', em.builtin_types['text'],
    ),
    em.Column.define('release_date', em.builtin_types['date'],
    ),
    em.Column.define('Age (yrs)', em.builtin_types['text'],
    ),
    em.Column.define('sex', em.builtin_types['text'],
    ),
    em.Column.define('race', em.builtin_types['text'],
    ),
    em.Column.define('ethnicity', em.builtin_types['text'],
    ),
    em.Column.define('OMIM Number', em.builtin_types['text'],
    ),
    em.Column.define('syndrome', em.builtin_types['text'],
    ),
    em.Column.define('Syndrome Subtype', em.builtin_types['text'],
    ),
    em.Column.define('Full Molecular Diagnosis', em.builtin_types['text'],
    ),
    em.Column.define('Height (cm)', em.builtin_types['text'],
    ),
    em.Column.define('Weight (kg)', em.builtin_types['text'],
    ),
    em.Column.define('Head Circumference (cm)', em.builtin_types['text'],
    ),
    em.Column.define('expr1015', em.builtin_types['text'],
    ),
    em.Column.define('camera', em.builtin_types['text'],
    ),
    em.Column.define('Diagnosis Status', em.builtin_types['text'],
    ),
    em.Column.define('DNA_Source', em.builtin_types['text'],
    ),
    em.Column.define('DNA Ext Method', em.builtin_types['text'],
    ),
    em.Column.define('species', em.builtin_types['text'],
    ),
    em.Column.define('specimen', em.builtin_types['text'],
    ),
    em.Column.define('gene', em.builtin_types['text'],
    ),
    em.Column.define('genotype', em.builtin_types['text'],
    ),
    em.Column.define('anatomy', em.builtin_types['text'],
    ),
    em.Column.define('phenotype', em.builtin_types['text'],
    ),
    em.Column.define('molecule_type', em.builtin_types['text'],
    ),
    em.Column.define('assay_type', em.builtin_types['text'],
    ),
    em.Column.define('sample_composition', em.builtin_types['text'],
    ),
    em.Column.define('isolation_protocol', em.builtin_types['text'],
    ),
    em.Column.define('alignment_id', em.builtin_types['int4'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'clinical_assay_RID_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('isa', 'clinical_assay_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['gene'],
            'vocab', 'gene_terms', ['dbxref'],
            constraint_names=[('isa', 'clinical_assay_gene_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Gene'}},
    ),
    em.ForeignKey.define(['genotype'],
            'vocab', 'genotype_terms', ['dbxref'],
            constraint_names=[('isa', 'clinical_assay_genotype_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Genotype'}},
    ),
    em.ForeignKey.define(['specimen'],
            'vocab', 'specimen_terms', ['dbxref'],
            constraint_names=[('isa', 'clinical_assay_specimen_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Specimen'}},
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['id'],
            constraint_names=[('isa', 'clinical_assay_dataset_fkey')],
    ),
    em.ForeignKey.define(['phenotype'],
            'vocab', 'phenotype_terms', ['dbxref'],
            constraint_names=[('isa', 'clinical_assay_phenotype_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Phenotype'}},
    ),
    em.ForeignKey.define(['alignment_id'],
            'isa', 'alignment', ['id'],
            constraint_names=[('isa', 'clinical_assay_alignment_id_fkey')],
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns=\
{'compact': ['local_id', 'Age (yrs)', 'sex',
             ['isa', 'clinical_assay_gene_fkey'], 'syndrome',
             'Syndrome Subtype', 'race', 'ethnicity'],
 'detailed': [['isa', 'clinical_assay_dataset_fkey'], 'local_id',
              'release_date', 'Age (yrs)', 'sex',
              ['isa', 'clinical_assay_gene_fkey'], 'syndrome',
              'Syndrome Subtype', 'Height (cm)', 'Weight (kg)', 'race',
              'ethnicity', 'OMIM Number', 'Full Molecular Diagnosis',
              'Head Circumference (cm)', 'expr1015', 'camera',
              'Diagnosis Status', 'DNA_Source', 'DNA Ext Method',
              ['isa', 'clinical_assay_species_fkey'],
              ['isa', 'clinical_assay_specimen_fkey'],
              ['isa', 'clinical_assay_genotype_fkey'],
              ['isa', 'clinical_assay_anatomy_fkey'],
              ['isa', 'clinical_assay_phenotype_fkey'], 'molecule_type',
              'assay_type', 'sample_composition', 'isolation_protocol',
              'alignment_id']}

visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings=\
{'curated_status_guard': {'projection': [{'outbound': ['isa',
                                                       'clinical_assay_dataset_fkey']},
                                         {'filter': 'status',
                                          'operand': 'commons:226:',
                                          'operator': '='},
                                         'RID'],
                          'projection_type': 'nonnull',
                          'scope_acl': ['*'],
                          'types': ['select']},
 'dataset_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'clinical_assay_dataset_fkey']},
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
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}


table_def = em.Table.define('clinical_assay',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
