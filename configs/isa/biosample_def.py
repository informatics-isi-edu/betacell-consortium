import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'biosample'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}},
    ),
    em.Column.define('local_identifier', em.builtin_types['text'],
    ),
    em.Column.define('summary', em.builtin_types['text'],
    ),
    em.Column.define('collection_date', em.builtin_types['date'],
    ),
    em.Column.define('_keywords', em.builtin_types['text'],
    ),
    em.Column.define('capillary_number', em.builtin_types['int2'],
        comment='ID number of the capillary constaining the biosample.',
    ),
    em.Column.define('sample_position', em.builtin_types['int2'],
        comment='Position in the capillary where the sample is located.',
    ),
    em.Column.define('specimen', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}},
        comment='Biological material used for the biosample.',
    ),
    em.Column.define('specimen_type', em.builtin_types['text'],
        comment='Method by which specimen is prepared.',
    ),
]


key_defs = [
    em.Key.define(['dataset', 'local_identifier'],
                   constraint_names=[('isa', 'biosample_dataset_local_identifier_key')],
       annotations = {'tag:misd.isi.edu,2015:display': {}},
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'biosample_pkey')],
       annotations = {'tag:misd.isi.edu,2015:display': {}},
    ),
]


fkey_defs = [
    em.ForeignKey.define(['specimen'],
            'isa', 'specimen', ['RID'],
            constraint_names=[('isa', 'biosample_specimen_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['specimen_type'],
            'vocab', 'specimen_type_terms', ['id'],
            constraint_names=[('isa', 'biosample_specimen_type_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Must be a valid reference to a specimen type.',
    ),
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'biosample_dataset_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns=\
{'*': ['cell_line', 'capillary_column', 'sample_position'],
 'compact': [['isa', 'biosample_pkey'], 'local_identifier',
             {'markdown_name': 'Cell Line',
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'outbound': ['isa', 'specimen_cell_line_fkey']},
                         'name']},
             {'markdown_name': 'Gender',
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'outbound': ['isa', 'specimen_gender_fkey']},
                         'name']},
             'species', 'capillary_number', 'sample_position'],
 'detailed': [['isa', 'biosample_pkey'], ['isa', 'biosample_dataset_fkey'],
              'local_identifier', 'summary', ['isa', 'biosample_species_fkey'],
              ['isa', 'biosample_specimen_fkey'],
              {'markdown_name': 'Cell Line',
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'outbound': ['isa', 'specimen_cell_line_fkey']},
                          'name']},
              {'markdown_name': 'Species',
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'outbound': ['isa', 'specimen_species_fkey']},
                          'name']},
              {'markdown_name': 'Gender',
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'outbound': ['isa', 'specimen_gender_fkey']},
                          'name']},
              {'markdown_name': 'Anatomy',
               'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                          {'outbound': ['isa', 'specimen_anatomy_fkey']},
                          'name']},
              [['isa', 'biosample_specimen_fkey'],
               ['isa', 'specimen_species_fkey']],
              ['isa', 'biosample_specimen_type_fkey'], 'capillary_number',
              'sample_position', 'collection_date'],
 'entry': [['isa', 'biosample_dataset_fkey'], 'local_identifier',
           ['isa', 'biosample_specimen_fkey'],
           ['isa', 'biosample_specimen_type_fkey'], 'capillary_number',
           'sample_position', 'collection_date'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Species',
                     'open': True,
                     'source': [{'outbound': ['isa', 'biosample_species_fkey']},
                                'term']},
                    {'entity': True,
                     'markdown_name': 'Local Identifier',
                     'open': False,
                     'source': 'local_identifier'},
                    {'entity': True, 'source': 'capillary_number'},
                    {'markdown_name': 'Cell Line',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                'name']},
                    {'markdown_name': 'Species',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_species_fkey']},
                                'name']},
                    {'markdown_name': 'Gender',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_gender_fkey']},
                                'name']},
                    {'markdown_name': 'Anatomy',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_anatomy_fkey']},
                                'name']}]}}

visible_foreign_keys=\
{'*': ['cell_line', 'capillary_column', 'sample_position'],
 'compact': [['isa', 'biosample_pkey'], 'local_identifier',
             {'markdown_name': 'Cell Line',
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'outbound': ['isa', 'specimen_cell_line_fkey']},
                         'name']},
             {'markdown_name': 'Gender',
              'source': [{'outbound': ['isa', 'biosample_specimen_fkey']},
                         {'outbound': ['isa', 'specimen_gender_fkey']},
                         'name']},
             'species', 'capillary_number', 'sample_position'],
 'detailed': [['isa', 'replicate_biosample_fkey']],
 'entry': [['isa', 'replicate_biosample_fkey']],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Species',
                     'open': True,
                     'source': [{'outbound': ['isa', 'biosample_species_fkey']},
                                'term']},
                    {'entity': True,
                     'markdown_name': 'Local Identifier',
                     'open': False,
                     'source': 'local_identifier'},
                    {'entity': True, 'source': 'capillary_number'},
                    {'markdown_name': 'Cell Line',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                'name']},
                    {'markdown_name': 'Species',
                     'source': [{'outbound': ['isa', 'biosample_specime_fkey']},
                                {'outbound': ['isa', 'specimen_species_fkey']},
                                'name']},
                    {'markdown_name': 'Gender',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_gender_fkey']},
                                'name']},
                    {'markdown_name': 'Anatomy',
                     'source': [{'outbound': ['isa',
                                              'biosample_specimen_fkey']},
                                {'outbound': ['isa', 'specimen_anatomy_fkey']},
                                'name']}]}}

table_display=\
{'row_name': {'row_markdown_pattern': '{{RID}} - '
                                      '{{summary}}{{#local_identifier}} '
                                      '[{{local_identifier}}] '
                                      '{{/local_identifier}}'}}

table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:misd.isi.edu,2015:display":
{}
,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:table-alternatives":
{}
,
}
column_annotations = \
{'dataset': {'tag:isrd.isi.edu,2016:column-display': {},
             'tag:isrd.isi.edu,2017:asset': {},
             'tag:misd.isi.edu,2015:display': {}},
 'specimen': {'tag:isrd.isi.edu,2016:column-display': {},
              'tag:isrd.isi.edu,2017:asset': {},
              'tag:misd.isi.edu,2015:display': {}}}



table_def = em.Table.define('biosample',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
