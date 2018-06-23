import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'dataset',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}}
            comment=None),
    
    em.Column.define(
            'local_identifier',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'summary',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'collection_date',em.builtin_types.{'typename': 'date', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            '_keywords',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'capillary_number',em.builtin_types.{'typename': 'int2', 'is_array': False},
            nullok=True,
            annotations={}
            comment='ID number of the capillary constaining the biosample.'),
    
    em.Column.define(
            'sample_position',em.builtin_types.{'typename': 'int2', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Position in the capillary where the sample is located.'),
    
    em.Column.define(
            'specimen',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}}
            comment='Biological material used for the biosample.'),
    
    em.Column.define(
            'specimen_type',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Method by which specimen is prepared.'),
    
key_defs = [
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'biosample_pkey')],
                annotation={'tag:misd.isi.edu,2015:display': {}},
                comment=None),
    em.Key.define(
                ['local_identifier', 'dataset'],
                constraint_names=[('isa', 'biosample_dataset_local_identifier_key')],
                annotation={'tag:misd.isi.edu,2015:display': {}},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['specimen_type'],
            'vocab', 'specimen_type_terms', ['id'],
            constraint_names = [('isa', 'biosample_specimen_type_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        comment = 'Must be a valid reference to a specimen type.',
    ),
    em.ForeignKey.define(
            ['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names = [('isa', 'biosample_dataset_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
    em.ForeignKey.define(
            ['specimen'],
            'isa', 'specimen', ['RID'],
            constraint_names = [('isa', 'biosample_specimen_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
]

table_annotations =
{   'tag:isrd.isi.edu,2016:table-alternatives': {},
    'tag:isrd.isi.edu,2016:table-display': {   'row_name': {   'row_markdown_pattern': '{{RID}} '
                                                                                       '- '
                                                                                       '{{summary}}{{#local_identifier}} '
                                                                                       '[{{local_identifier}}] '
                                                                                       '{{/local_identifier}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   '*': [   'cell_line',
                                                          'capillary_column',
                                                          'sample_position'],
                                                 'compact': [   [   'isa',
                                                                    'biosample_pkey'],
                                                                'local_identifier',
                                                                {   'markdown_name': 'Cell '
                                                                                     'Line',
                                                                    'source': [   {   'outbound': [   'isa',
                                                                                                      'biosample_specimen_fkey']},
                                                                                  {   'outbound': [   'isa',
                                                                                                      'specimen_cell_line_fkey']},
                                                                                  'name']},
                                                                {   'markdown_name': 'Gender',
                                                                    'source': [   {   'outbound': [   'isa',
                                                                                                      'biosample_specimen_fkey']},
                                                                                  {   'outbound': [   'isa',
                                                                                                      'specimen_gender_fkey']},
                                                                                  'name']},
                                                                'species',
                                                                'capillary_number',
                                                                'sample_position'],
                                                 'detailed': [   [   'isa',
                                                                     'biosample_pkey'],
                                                                 [   'isa',
                                                                     'biosample_dataset_fkey'],
                                                                 'local_identifier',
                                                                 'summary',
                                                                 [   'isa',
                                                                     'biosample_species_fkey'],
                                                                 [   'isa',
                                                                     'biosample_specimen_fkey'],
                                                                 {   'markdown_name': 'Cell '
                                                                                      'Line',
                                                                     'source': [   {   'outbound': [   'isa',
                                                                                                       'biosample_specimen_fkey']},
                                                                                   {   'outbound': [   'isa',
                                                                                                       'specimen_cell_line_fkey']},
                                                                                   'name']},
                                                                 {   'markdown_name': 'Species',
                                                                     'source': [   {   'outbound': [   'isa',
                                                                                                       'biosample_specimen_fkey']},
                                                                                   {   'outbound': [   'isa',
                                                                                                       'specimen_species_fkey']},
                                                                                   'name']},
                                                                 {   'markdown_name': 'Gender',
                                                                     'source': [   {   'outbound': [   'isa',
                                                                                                       'biosample_specimen_fkey']},
                                                                                   {   'outbound': [   'isa',
                                                                                                       'specimen_gender_fkey']},
                                                                                   'name']},
                                                                 {   'markdown_name': 'Anatomy',
                                                                     'source': [   {   'outbound': [   'isa',
                                                                                                       'biosample_specimen_fkey']},
                                                                                   {   'outbound': [   'isa',
                                                                                                       'specimen_anatomy_fkey']},
                                                                                   'name']},
                                                                 [   [   'isa',
                                                                         'biosample_specimen_fkey'],
                                                                     [   'isa',
                                                                         'specimen_species_fkey']],
                                                                 [   'isa',
                                                                     'biosample_specimen_type_fkey'],
                                                                 'capillary_number',
                                                                 'sample_position',
                                                                 'collection_date'],
                                                 'entry': [   [   'isa',
                                                                  'biosample_dataset_fkey'],
                                                              'local_identifier',
                                                              [   'isa',
                                                                  'biosample_specimen_fkey'],
                                                              [   'isa',
                                                                  'biosample_specimen_type_fkey'],
                                                              'capillary_number',
                                                              'sample_position',
                                                              'collection_date'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'markdown_name': 'Species',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'biosample_species_fkey']},
                                                                                            'term']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Local '
                                                                                               'Identifier',
                                                                              'open': False,
                                                                              'source': 'local_identifier'},
                                                                          {   'entity': True,
                                                                              'source': 'capillary_number'},
                                                                          {   'markdown_name': 'Cell '
                                                                                               'Line',
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'biosample_specimen_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'specimen_cell_line_fkey']},
                                                                                            'name']},
                                                                          {   'markdown_name': 'Species',
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'biosample_specimen_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'specimen_species_fkey']},
                                                                                            'name']},
                                                                          {   'markdown_name': 'Gender',
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'biosample_specimen_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'specimen_gender_fkey']},
                                                                                            'name']},
                                                                          {   'markdown_name': 'Anatomy',
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'biosample_specimen_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'specimen_anatomy_fkey']},
                                                                                            'name']}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   '*': [   'cell_line',
                                                               'capillary_column',
                                                               'sample_position'],
                                                      'compact': [   [   'isa',
                                                                         'biosample_pkey'],
                                                                     'local_identifier',
                                                                     {   'markdown_name': 'Cell '
                                                                                          'Line',
                                                                         'source': [   {   'outbound': [   'isa',
                                                                                                           'biosample_specimen_fkey']},
                                                                                       {   'outbound': [   'isa',
                                                                                                           'specimen_cell_line_fkey']},
                                                                                       'name']},
                                                                     {   'markdown_name': 'Gender',
                                                                         'source': [   {   'outbound': [   'isa',
                                                                                                           'biosample_specimen_fkey']},
                                                                                       {   'outbound': [   'isa',
                                                                                                           'specimen_gender_fkey']},
                                                                                       'name']},
                                                                     'species',
                                                                     'capillary_number',
                                                                     'sample_position'],
                                                      'detailed': [   [   'isa',
                                                                          'replicate_biosample_fkey']],
                                                      'entry': [   [   'isa',
                                                                       'replicate_biosample_fkey']],
                                                      'filter': {   'and': [   {   'entity': True,
                                                                                   'markdown_name': 'Species',
                                                                                   'open': True,
                                                                                   'source': [   {   'outbound': [   'isa',
                                                                                                                     'biosample_species_fkey']},
                                                                                                 'term']},
                                                                               {   'entity': True,
                                                                                   'markdown_name': 'Local '
                                                                                                    'Identifier',
                                                                                   'open': False,
                                                                                   'source': 'local_identifier'},
                                                                               {   'entity': True,
                                                                                   'source': 'capillary_number'},
                                                                               {   'markdown_name': 'Cell '
                                                                                                    'Line',
                                                                                   'source': [   {   'outbound': [   'isa',
                                                                                                                     'biosample_specimen_fkey']},
                                                                                                 {   'outbound': [   'isa',
                                                                                                                     'specimen_cell_line_fkey']},
                                                                                                 'name']},
                                                                               {   'markdown_name': 'Species',
                                                                                   'source': [   {   'outbound': [   'isa',
                                                                                                                     'biosample_specime_fkey']},
                                                                                                 {   'outbound': [   'isa',
                                                                                                                     'specimen_species_fkey']},
                                                                                                 'name']},
                                                                               {   'markdown_name': 'Gender',
                                                                                   'source': [   {   'outbound': [   'isa',
                                                                                                                     'biosample_specimen_fkey']},
                                                                                                 {   'outbound': [   'isa',
                                                                                                                     'specimen_gender_fkey']},
                                                                                                 'name']},
                                                                               {   'markdown_name': 'Anatomy',
                                                                                   'source': [   {   'outbound': [   'isa',
                                                                                                                     'biosample_specimen_fkey']},
                                                                                                 {   'outbound': [   'isa',
                                                                                                                     'specimen_anatomy_fkey']},
                                                                                                 'name']}]}},
    'tag:misd.isi.edu,2015:display': {}}

table_def = em.Table.define(
    biosample,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment=None,
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:biosample')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'biosample'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
