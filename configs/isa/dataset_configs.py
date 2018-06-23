import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
visible_columns = \
{   'compact': [   ['isa', 'dataset_RID_key'],
                   ['isa', 'accession_unique'],
                   'title',
                   ['isa', 'dataset_project_fkey'],
                   'status',
                   'release_date'],
    'detailed': [   ['isa', 'dataset_RID_key'],
                    'accession',
                    'description',
                    'study_design',
                    ['isa', 'dataset_project_fkey'],
                    ['isa', 'dataset_status_fkey'],
                    'funding',
                    'release_date',
                    'show_in_jbrowse',
                    ['isa', 'publication_dataset_fkey'],
                    ['isa', 'dataset_experiment_type_dataset_id_fkey'],
                    ['isa', 'dataset_data_type_dataset_id_fkey'],
                    ['isa', 'dataset_phenotype_dataset_fkey'],
                    ['isa', 'dataset_organism_dataset_id_fkey'],
                    ['isa', 'dataset_anatomy_dataset_id_fkey'],
                    ['isa', 'dataset_gender_dataset_id_fkey'],
                    ['isa', 'dataset_instrument_dataset_id_fkey']],
    'entry': [   'accession',
                 'title',
                 ['isa', 'dataset_project_fkey'],
                 'description',
                 'study_design',
                 'release_date',
                 ['isa', 'dataset_status_fkey'],
                 'show_in_jbrowse'],
    'filter': {   'and': [   {   'entity': True,
                                 'open': False,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'dataset_organism_dataset_id_fkey']},
                                               {   'outbound': [   'isa',
                                                                   'dataset_organism_organism_fkey']},
                                               'dbxref']},
                             {   'entity': True,
                                 'open': False,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'dataset_experiment_type_dataset_id_fkey']},
                                               {   'outbound': [   'isa',
                                                                   'dataset_experiment_type_experiment_type_fkey']},
                                               'dbxref']},
                             {   'entity': True,
                                 'open': False,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'dataset_data_type_data_type_fkey']},
                                               {   'outbound': [   'isa',
                                                                   'dataset_data_type_dataset_id_fkey']},
                                               'dbxref']},
                             {   'entity': True,
                                 'open': False,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'dataset_anatomy_dataset_id_fkey']},
                                               {   'outbound': [   'isa',
                                                                   'dataset_anatomy_anatomy_fkey']},
                                               'dbxref']},
                             {   'entity': True,
                                 'open': False,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'dataset_phenotype_dataset_fkey']},
                                               {   'outbound': [   'isa',
                                                                   'dataset_phenotype_phenotype_fkey']},
                                               'dbxref']},
                             {   'entity': True,
                                 'markdown_name': 'Pubmed ID',
                                 'open': False,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'publication_dataset_fkey']},
                                               'pmid']},
                             {   'entity': True,
                                 'markdown_name': 'Project Investigator',
                                 'open': False,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'dataset_project_fkey']},
                                               {   'inbound': [   'isa',
                                                                  'project_investigator_project_id_fkey']},
                                               {   'outbound': [   'isa',
                                                                   'project_investigator_person_fkey']},
                                               'RID']},
                             {   'entity': False,
                                 'open': False,
                                 'source': 'accession'},
                             {   'entity': False,
                                 'open': False,
                                 'source': 'title'},
                             {   'entity': True,
                                 'open': False,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'dataset_project_fkey']},
                                               'id']},
                             {   'entity': False,
                                 'open': False,
                                 'source': 'release_date'},
                             {   'entity': True,
                                 'open': False,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'dataset_status_fkey']},
                                               'name']}]}}
visible_foreign_keys = \
{   '*': [   ['isa', 'thumbnail_dataset_fkey'],
             ['viz', 'model_dataset_fkey'],
             ['isa', 'previews_dataset_id_fkey'],
             ['isa', 'experiment_dataset_fkey'],
             ['isa', 'biosample_dataset_fkey'],
             ['isa', 'enhancer_dataset_fkey'],
             ['isa', 'clinical_assay_dataset_fkey'],
             ['isa', 'file_dataset_fkey'],
             ['isa', 'external_reference_id_fkey']]}
table_display = \
{   '*': {'row_order': [{'column': 'accession', 'descending': True}]},
    'row_name': {'row_markdown_pattern': '{{title}}'}}
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {   '*': {   'row_order': [   {   'column': 'accession',
                                                                             'descending': True}]},
                                               'row_name': {   'row_markdown_pattern': '{{title}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'dataset_RID_key'],
                                                                [   'isa',
                                                                    'accession_unique'],
                                                                'title',
                                                                [   'isa',
                                                                    'dataset_project_fkey'],
                                                                'status',
                                                                'release_date'],
                                                 'detailed': [   [   'isa',
                                                                     'dataset_RID_key'],
                                                                 'accession',
                                                                 'description',
                                                                 'study_design',
                                                                 [   'isa',
                                                                     'dataset_project_fkey'],
                                                                 [   'isa',
                                                                     'dataset_status_fkey'],
                                                                 'funding',
                                                                 'release_date',
                                                                 'show_in_jbrowse',
                                                                 [   'isa',
                                                                     'publication_dataset_fkey'],
                                                                 [   'isa',
                                                                     'dataset_experiment_type_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_data_type_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_phenotype_dataset_fkey'],
                                                                 [   'isa',
                                                                     'dataset_organism_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_anatomy_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_gender_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_instrument_dataset_id_fkey']],
                                                 'entry': [   'accession',
                                                              'title',
                                                              [   'isa',
                                                                  'dataset_project_fkey'],
                                                              'description',
                                                              'study_design',
                                                              'release_date',
                                                              [   'isa',
                                                                  'dataset_status_fkey'],
                                                              'show_in_jbrowse'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_organism_dataset_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_organism_organism_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_experiment_type_dataset_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_experiment_type_experiment_type_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_data_type_data_type_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_data_type_dataset_id_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_anatomy_dataset_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_anatomy_anatomy_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_phenotype_dataset_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_phenotype_phenotype_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Pubmed '
                                                                                               'ID',
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'publication_dataset_fkey']},
                                                                                            'pmid']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Project '
                                                                                               'Investigator',
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'dataset_project_fkey']},
                                                                                            {   'inbound': [   'isa',
                                                                                                               'project_investigator_project_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'project_investigator_person_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': False,
                                                                              'open': False,
                                                                              'source': 'accession'},
                                                                          {   'entity': False,
                                                                              'open': False,
                                                                              'source': 'title'},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'dataset_project_fkey']},
                                                                                            'id']},
                                                                          {   'entity': False,
                                                                              'open': False,
                                                                              'source': 'release_date'},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'dataset_status_fkey']},
                                                                                            'name']}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   '*': [   [   'isa',
                                                                   'thumbnail_dataset_fkey'],
                                                               [   'viz',
                                                                   'model_dataset_fkey'],
                                                               [   'isa',
                                                                   'previews_dataset_id_fkey'],
                                                               [   'isa',
                                                                   'experiment_dataset_fkey'],
                                                               [   'isa',
                                                                   'biosample_dataset_fkey'],
                                                               [   'isa',
                                                                   'enhancer_dataset_fkey'],
                                                               [   'isa',
                                                                   'clinical_assay_dataset_fkey'],
                                                               [   'isa',
                                                                   'file_dataset_fkey'],
                                                               [   'isa',
                                                                   'external_reference_id_fkey']]}}
table_acl_bindings = \
{   'dataset_edit_guard': {   'projection': [   {   'outbound': [   'isa',
                                                                    'dataset_project_fkey']},
                                                {   'outbound': [   'isa',
                                                                    'project_groups_fkey']},
                                                'groups'],
                              'projection_type': 'acl',
                              'scope_acl': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                               'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                               'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                              'types': ['update', 'delete']}}
column_annotations = \
{   'accession': {'tag:isrd.isi.edu,2016:generated': None},
    'show_in_jbrowse': {   'tag:isrd.isi.edu,2016:column-display': {   'detailed': {   'markdown_pattern': '{{#_show_in_jbrowse}}Use '
                                                                                                           'the '
                                                                                                           'embedded '
                                                                                                           'browser '
                                                                                                           'here '
                                                                                                           'or '
                                                                                                           '[view '
                                                                                                           'in '
                                                                                                           'a '
                                                                                                           'new '
                                                                                                           'window](/jbrowse/latest/?dataset={{{_RID}}}){target=_blank}.\n'
                                                                                                           ' '
                                                                                                           ':::iframe '
                                                                                                           '[](/jbrowse/latest/?dataset={{{_RID}}}){width=800 '
                                                                                                           'height=600 '
                                                                                                           '.iframe} \n'
                                                                                                           ':::{{/_show_in_jbrowse}}'}},
                           'tag:misd.isi.edu,2015:display': {   'name': 'Genome '
                                                                        'Browser'}},
    'status': {   'tag:isrd.isi.edu,2016:column-display': {   'compact': {   'markdown_pattern': '{{{ '
                                                                                                 '$fkeys.isa.dataset_status_fkey.rowName '
                                                                                                 '}}}'}}}}
column_acl_bindings = \
{'status': {'dataset_edit_guard': False}}

def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:dataset')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = 'isa'
        table_name = 'dataset'

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
