import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cell_line'
schema_name = 'isa'

column_defs = [
    em.Column.define('cell_line_id', em.builtin_types['text'],
        comment='ID of cell line being used.',
    ),
    em.Column.define('species', em.builtin_types['text'],
        comment='Species of the specimen',
    ),
    em.Column.define('anatomy', em.builtin_types['text'],
        comment='Anatomical region speciment was obtained from.',
    ),
    em.Column.define('description', em.builtin_types['text'],
        comment='Description of the specimen.',
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'cell_line_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['anatomy'],
            'vocab', 'anatomy_terms', ['id'],
            constraint_names=[('isa', 'cell_line_anatomy_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['cell_line_id'],
            'vocab', 'cell_line_terms', ['id'],
            constraint_names=[('isa', 'cell_line_cell_line_terms_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(['species'],
            'vocab', 'species_terms', ['id'],
            constraint_names=[('isa', 'cell_line_species_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns = \
{'compact': [['isa', 'cell_line_pkey'], 'local_identifier',
             ['isa', 'cell_line_cell_line_terms_fkey']],
 'detailed': [['isa', 'specimen_pkey'], 'local_identifier',
              ['isa', 'cell_line_cell_line_terms_fkey'],
              ['isa', 'cell_line_species_fkey'],
              ['isa', 'cell_line_anatomy_fkey'], 'description',
              'collection_date'],
 'entry': [['isa', 'local_identifier'],
           ['isa', 'cell_line_cell_line_terms_fkey'],
           ['isa', 'cell_line_species_fkey'], ['isa', 'cell_line_anatomy_fkey'],
           'description', 'collection_date'],
 'filter': {'and': [{'entity': True,
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'entity': True,
                     'open': True,
                     'source': [{'outbound': ['isa', 'cell_line_species_fkey']},
                                'name']},
                    {'entity': True,
                     'markdown_name': 'Cell Line',
                     'open': True,
                     'source': [{'outbound': ['isa', 'cell_line_anatomy_fkey']},
                                'name']}]}}

visible_foreign_keys = \
{'detailed': [['isa', 'xray_tomography_data_replicate_fkey'],
              ['isa', 'mesh_data_replicate_fkey'],
              ['isa', 'processed_data_replicate_fkey'],
              ['isa', 'imaging_data_replicate_fkey']],
 'entry': [['isa', 'xray_tomography_data_replicate_fkey'],
           ['isa', 'mesh_data_replicate_fkey'],
           ['isa', 'processed_data_replicate_fkey'],
           ['isa', 'imaging_data_replicate_fkey']]}

table_comment = \
'Table of cultured  from which specimens  will be created.'

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "table_display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'anatomy': 'Anatomical region speciment was obtained from.',
 'cell_line_id': 'ID of cell line being used.',
 'description': 'Description of the specimen.',
 'species': 'Species of the specimen'}

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
