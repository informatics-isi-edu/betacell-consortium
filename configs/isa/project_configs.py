import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
visible_columns = \
{   'compact': ['name', 'abstract'],
    'detailed': [   'name',
                    'funding',
                    'url',
                    'abstract',
                    'group_membership_url',
                    ['isa', 'project_publication_project_id_fkey']],
    'entry': [   'name',
                 'funding',
                 'url',
                 'abstract',
                 'pis',
                 ['isa', 'project_groups_fkey'],
                 'group_membership_url'],
    'filter': {   'and': [   {   'entity': True,
                                 'markdown_name': 'Investigator',
                                 'open': True,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'project_investigator_project_id_fkey']},
                                               'username']},
                             {   'entity': False,
                                 'open': False,
                                 'source': 'funding'},
                             {   'entity': True,
                                 'markdown_name': 'Publication',
                                 'open': False,
                                 'source': [   {   'inbound': [   'isa',
                                                                  'project_publication_project_id_fkey']},
                                               'pmid']}]}}
visible_foreign_keys = \
{   'detailed': [   ['isa', 'project_investigator_project_id_fkey'],
                    ['isa', 'project_member_project_id_fkey'],
                    ['isa', 'dataset_project_fkey']]}
table_display = \
{   'compact': {'row_order': [{'column': 'pis', 'descending': False}]},
    'row_name': {'row_markdown_pattern': '{{{pis}}}: {{{name}}}'}}
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {   'compact': {   'row_order': [   {   'column': 'pis',
                                                                                   'descending': False}]},
                                               'row_name': {   'row_markdown_pattern': '{{{pis}}}: '
                                                                                       '{{{name}}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   'name',
                                                                'abstract'],
                                                 'detailed': [   'name',
                                                                 'funding',
                                                                 'url',
                                                                 'abstract',
                                                                 'group_membership_url',
                                                                 [   'isa',
                                                                     'project_publication_project_id_fkey']],
                                                 'entry': [   'name',
                                                              'funding',
                                                              'url',
                                                              'abstract',
                                                              'pis',
                                                              [   'isa',
                                                                  'project_groups_fkey'],
                                                              'group_membership_url'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'markdown_name': 'Investigator',
                                                                              'open': True,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'project_investigator_project_id_fkey']},
                                                                                            'username']},
                                                                          {   'entity': False,
                                                                              'open': False,
                                                                              'source': 'funding'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Publication',
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'project_publication_project_id_fkey']},
                                                                                            'pmid']}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'project_investigator_project_id_fkey'],
                                                                      [   'isa',
                                                                          'project_member_project_id_fkey'],
                                                                      [   'isa',
                                                                          'dataset_project_fkey']]}}
table_acl_bindings = \
{   'project_edit_guard': {   'projection': [   {   'outbound': [   'isa',
                                                                    'project_groups_fkey']},
                                                'groups'],
                              'projection_type': 'acl',
                              'scope_acl': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                               'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                               'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                              'types': ['update', 'delete']}}
column_annotations = \
{   'name': {   'tag:isrd.isi.edu,2016:column-display': {   'compact': {   'markdown_pattern': '{{{pis}}}: '
                                                                                               '{{{name}}}'}}},
    'pis': {'tag:misd.isi.edu,2015:display': {'name': 'List of PI Last Names'}},
    'url': {   'tag:isrd.isi.edu,2016:column-display': {   '*': {   'markdown_pattern': '[{{{url}}}]({{{url}}})'}}}}
column_acls = \
{   'group_membership_url': {   'enumerate': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                                 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                                                 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                                 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                                'select': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                              'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                                              'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                              'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d']},
    'groups': {   'enumerate': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                   'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                                   'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                   'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                  'select': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                                'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d']}}
column_acl_bindings = \
{'group_membership_url': {'project_edit_guard': False},
 'groups': {'project_edit_guard': False}}

def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:project')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = 'isa'
        table_name = 'project'

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
