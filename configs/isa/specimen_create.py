import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'dataset',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Cell line used for the speciman.'),
    
    em.Column.define(
            'cell_line',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Cell line used for the speciman.'),
    
    em.Column.define(
            'species',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Species of the specimen'),
    
    em.Column.define(
            'anatomy',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Anatomical region speciment was obtained from.'),
    
    em.Column.define(
            'description',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Description of the specimen.'),
    
    em.Column.define(
            'collection_date',em.builtin_types.{'typename': 'date', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Date the specimen was obtained'),
    
key_defs = [
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'specimen_RIDkey1')],
                annotation={},
                comment=None),
    em.Key.define(
                ['dataset', 'RID'],
                constraint_names=[('isa', 'specimen_RID_key')],
                annotation={},
                comment='RID and dataset must be distinct.'),
]

fkey_defs = [
    em.ForeignKey.define(
            ['anatomy'],
            'vocab', 'anatomy_terms', ['id'],
            constraint_names = [('isa', 'specimen_anatomy_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(
            ['cell_line'],
            'vocab', 'cell_line_terms', ['id'],
            constraint_names = [('isa', 'specimen_cell_line_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        comment = 'Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(
            ['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names = [('isa', 'specimen_dataset_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(
            ['species'],
            'vocab', 'species_terms', ['id'],
            constraint_names = [('isa', 'specimen_species_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
]

table_annotations =
{   'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'specimen_pkey'],
                                                                'local_identifier',
                                                                [   'isa',
                                                                    'specimen_cell_line_fkey']],
                                                 'detailed': [   [   'isa',
                                                                     'specimen_pkey'],
                                                                 'local_identifier',
                                                                 [   'isa',
                                                                     'specimen_dataset_fkey'],
                                                                 [   'isa',
                                                                     'specimen_cell_line_fkey'],
                                                                 [   'isa',
                                                                     'specimen_species_fkey'],
                                                                 [   'isa',
                                                                     'specimen_anatomy_fkey'],
                                                                 'description',
                                                                 'collection_date'],
                                                 'entry': [   [   'isa',
                                                                  'local_identifier'],
                                                              [   'isa',
                                                                  'specimen_dataset_fkey'],
                                                              [   'isa',
                                                                  'specimen_cell_line_fkey'],
                                                              [   'isa',
                                                                  'specimen_species_fkey'],
                                                              [   'isa',
                                                                  'specimen_anatomy_fkey'],
                                                              'description',
                                                              'collection_date'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'specimen_cell_line_fkey']},
                                                                                            'name']},
                                                                          {   'entity': True,
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'specimen_species_fkey']},
                                                                                            'name']},
                                                                          {   'entity': True,
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'specimen_anatomy_fkey']},
                                                                                            'name']}]},
                                                 'filterfilter': {   'and': [   {   'entity': True,
                                                                                    'open': True,
                                                                                    'source': [   {   'outbound': [   'isa',
                                                                                                                      'specimen_cell_line_fkey']},
                                                                                                  'RID']},
                                                                                {   'entity': True,
                                                                                    'open': True,
                                                                                    'source': [   {   'outbound': [   'isa',
                                                                                                                      'specimen_species_fkey']},
                                                                                                  'RID']},
                                                                                {   'entity': True,
                                                                                    'open': True,
                                                                                    'source': [   {   'outbound': [   'isa',
                                                                                                                      'specimen_anatomy_fkey']},
                                                                                                  'RID']}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'xray_tomography_data_replicate_fkey'],
                                                                      [   'isa',
                                                                          'mesh_data_replicate_fkey'],
                                                                      [   'isa',
                                                                          'processed_data_replicate_fkey'],
                                                                      [   'isa',
                                                                          'imaging_data_replicate_fkey']],
                                                      'entry': [   [   'isa',
                                                                       'xray_tomography_data_replicate_fkey'],
                                                                   [   'isa',
                                                                       'mesh_data_replicate_fkey'],
                                                                   [   'isa',
                                                                       'processed_data_replicate_fkey'],
                                                                   [   'isa',
                                                                       'imaging_data_replicate_fkey']]}}

table_def = em.Table.define(
    specimen,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment='Table of biological speciments from which biosamples will be created.',
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:specimen')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'specimen'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
