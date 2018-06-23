import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
visible_columns = \
{   'compact': [   ['isa', 'specimen_pkey'],
                   'local_identifier',
                   ['isa', 'specimen_cell_line_fkey']],
    'detailed': [   ['isa', 'specimen_pkey'],
                    'local_identifier',
                    ['isa', 'specimen_dataset_fkey'],
                    ['isa', 'specimen_cell_line_fkey'],
                    ['isa', 'specimen_species_fkey'],
                    ['isa', 'specimen_anatomy_fkey'],
                    'description',
                    'collection_date'],
    'entry': [   ['isa', 'local_identifier'],
                 ['isa', 'specimen_dataset_fkey'],
                 ['isa', 'specimen_cell_line_fkey'],
                 ['isa', 'specimen_species_fkey'],
                 ['isa', 'specimen_anatomy_fkey'],
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
                                                     'RID']}]}}
visible_foreign_keys = \
{   'detailed': [   ['isa', 'xray_tomography_data_replicate_fkey'],
                    ['isa', 'mesh_data_replicate_fkey'],
                    ['isa', 'processed_data_replicate_fkey'],
                    ['isa', 'imaging_data_replicate_fkey']],
    'entry': [   ['isa', 'xray_tomography_data_replicate_fkey'],
                 ['isa', 'mesh_data_replicate_fkey'],
                 ['isa', 'processed_data_replicate_fkey'],
                 ['isa', 'imaging_data_replicate_fkey']]}
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
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

        if len(visible_columns) > 0:
            for k, v in visible_columns.items():
                table.visible_columns[k] = v

        if len(visible_foreign_keys) > 0:
            for k, v in visible_foreign_keys.items():
                table.visible_foreign_keys[k] = v
        table.annotations['table_display'] = table_display

        table.apply(catalog)


if __name__ == "__main__":
        main()
