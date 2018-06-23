import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
visible_columns = \
{   'compact': [   ['isa', 'replicate_pkey'],
                   ['isa', 'replicate_biosample_fkey'],
                   'bioreplicate_number',
                   'technical_replicate_number'],
    'detailed': [   ['isa', 'replicate_pkey'],
                    ['isa', 'replicate_experiment_fkey'],
                    ['isa', 'replicate_biosample_fkey'],
                    'bioreplicate_number',
                    'technical_replicate_number'],
    'entry': [   ['isa', 'replicate_experiment_fkey'],
                 ['isa', 'replicate_biosample_fkey'],
                 'bioreplicate_number',
                 'technical_replicate_number'],
    'filter': {   'and': [   {   'entity': True,
                                 'markdown_name': 'Dataset',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'replicate_dataset_fkey']},
                                               'RID']},
                             {   'entity': True,
                                 'markdown_name': 'Experiment',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'replicate_experiment_fkey']},
                                               'RID']},
                             {   'entity': True,
                                 'markdown_name': 'Biosample',
                                 'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'replicate_biosample_fkey']},
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
table_display = \
{   'compact': {   'row_order': [   {   'column': 'bioreplicate_number',
                                        'descending': False}]},
    'row_name': {'row_markdown_pattern': '{{local_identifier}}'}}
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {   'compact': {   'row_order': [   {   'column': 'bioreplicate_number',
                                                                                   'descending': False}]},
                                               'row_name': {   'row_markdown_pattern': '{{local_identifier}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'replicate_pkey'],
                                                                [   'isa',
                                                                    'replicate_biosample_fkey'],
                                                                'bioreplicate_number',
                                                                'technical_replicate_number'],
                                                 'detailed': [   [   'isa',
                                                                     'replicate_pkey'],
                                                                 [   'isa',
                                                                     'replicate_experiment_fkey'],
                                                                 [   'isa',
                                                                     'replicate_biosample_fkey'],
                                                                 'bioreplicate_number',
                                                                 'technical_replicate_number'],
                                                 'entry': [   [   'isa',
                                                                  'replicate_experiment_fkey'],
                                                              [   'isa',
                                                                  'replicate_biosample_fkey'],
                                                              'bioreplicate_number',
                                                              'technical_replicate_number'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'markdown_name': 'Dataset',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'replicate_dataset_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Experiment',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'replicate_experiment_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Biosample',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'replicate_biosample_fkey']},
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
table_acls = \
{   'select': [   'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                  'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d']}
table_acl_bindings = \
{   'curated_status_guard': {   'projection': [   {   'outbound': [   'isa',
                                                                      'replicate_dataset_fkey']},
                                                  {   'filter': 'status',
                                                      'operand': 'commons:226:',
                                                      'operator': '='},
                                                  'RID'],
                                'projection_type': 'nonnull',
                                'scope_acl': ['*'],
                                'types': ['select']},
    'dataset_suppl_edit_guard': {   'projection': [   {   'outbound': [   'isa',
                                                                          'replicate_dataset_fkey']},
                                                      {   'outbound': [   'isa',
                                                                          'dataset_project_fkey']},
                                                      {   'outbound': [   'isa',
                                                                          'project_groups_fkey']},
                                                      'groups'],
                                    'projection_type': 'acl',
                                    'scope_acl': [   'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                                    'types': ['update', 'delete']}}

def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:replicate')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = 'isa'
        table_name = 'replicate'

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
