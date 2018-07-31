import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'specimen'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset', em.builtin_types['text'],
        comment='Cell line used for the speciman.',
    ),
    em.Column.define('description', em.builtin_types['text'],
        comment='Description of the specimen.',
    ),
    em.Column.define('collection_date', em.builtin_types['date'],
        comment='Date the specimen was obtained',
    ),
    em.Column.define('cell_line', em.builtin_types['text'],
        comment='Cell line used for the speciman.',
    ),
    em.Column.define('cellular_location', em.builtin_types['text'],
        comment='Cellular location of the specimen',
    ),
]


key_defs = [
    em.Key.define(['RID', 'dataset'],
                   constraint_names=[('isa', 'specimen_RID_key')],
       comment = 'RID and dataset must be distinct.',
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'specimen_RIDkey1')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names=[('isa', 'specimen_dataset_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['cellular_location'],
            'vocab', 'cellular_location_terms', ['id'],
            constraint_names=[('isa', 'specimen_cellular_location_terms_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['cell_line'],
            'isa', 'cell_line', ['RID'],
            constraint_names=[('isa', 'specimen_cell_line_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Must be a valid reference to a cell line.',
    ),
]


visible_columns = \
{'compact': [['isa', 'specimen_pkey'], 'local_identifier',
             {'source': [{'outbound': ['isa',
                                       'specimen_cellular_location_terms_fkey']},
                         'name']},
             {'source': [{'outbound': ['isa', 'specimen_cell_line_fkey']},
                         {'outbound': ['isa',
                                       'cell_line_cell_line_terms_fkey']},
                         'name']},
             'description'],
 'detailed': [['isa', 'specimen_pkey'], 'local_identifier',
              {'source': [{'outbound': ['isa',
                                        'specimen_cellular_location_terms_fkey']},
                          'name']},
              ['isa', 'specimen_dataset_fkey'],
              {'markdown_name': 'Cell Line',
               'source': [{'outbound': ['isa', 'specimen_cell_line_fkey']},
                          {'outbound': ['isa',
                                        'cell_line_cell_line_terms_fkey']},
                          'name']},
              'description', 'collection_date'],
 'entry': [['isa', 'local_identifier'], ['isa', 'specimen_dataset_fkey'],
           ['isa', 'specimen_cell_line_fkey'],
           ['isa', 'specimen_cellular_location_terms_fkey'], 'description',
           'collection_date'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Cell Line',
                     'open': True,
                     'source': [{'outbound': ['isa',
                                              'specimen_cell_line_fkey']},
                                {'outbound': ['isa',
                                              'cell_line_cell_line_terms_fkey']},
                                'name']},
                    {'entity': True,
                     'open': True,
                     'source': [{'outbound': ['isa', 'specimen_species_fkey']},
                                'name']},
                    {'entity': True,
                     'open': True,
                     'source': [{'outbound': ['isa', 'specimen_anatomy_fkey']},
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
{'cell_line': 'Cell line used for the speciman.',
 'cellular_location': 'Cellular location of the specimen',
 'collection_date': 'Date the specimen was obtained',
 'dataset': 'Cell line used for the speciman.',
 'description': 'Description of the specimen.'}



table_def = em.Table.define('specimen',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='Table of biological speciments from which biosamples will be created.',
    provide_system = True
)
