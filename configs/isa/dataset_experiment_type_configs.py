import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {},
    'tag:isrd.isi.edu,2016:visible-columns': {},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {},
    'tag:misd.isi.edu,2015:display': {'name': 'Experiment_type'}}
table_acl_bindings = \
{   'dataset_tags_edit_guard': {   'projection': [   {   'outbound': [   'isa',
                                                                         'dataset_experiment_type_dataset_id_fkey']},
                                                     {   'outbound': [   'isa',
                                                                         'dataset_project_fkey']},
                                                     {   'outbound': [   'isa',
                                                                         'project_groups_fkey']},
                                                     'groups'],
                                   'projection_type': 'acl',
                                   'scope_acl': [   'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                                    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                                    'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                                   'types': ['update', 'delete']}}

def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:dataset_experiment_type')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = 'isa'
        table_name = 'dataset_experiment_type'

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
