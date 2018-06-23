import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'id',em.builtin_types.{'typename': 'serial4', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'funding',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'url',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{{url}}}]({{{url}}})'}}}
            comment='url for more information on this project on externalre site'),
    
    em.Column.define(
            'name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{pis}}}: {{{name}}}'}}}
            comment=None),
    
    em.Column.define(
            'abstract',em.builtin_types.{'typename': 'markdown', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'pis',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:misd.isi.edu,2015:display': {'name': 'List of PI Last Names'}}
            comment='List of Last Names of Principal Investigator separated by /'),
    
    em.Column.define(
            'groups',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Users must be a member of the referenced ACL group in order to edit project records.'),
    
    em.Column.define(
            'group_membership_url',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='URL that project members will need in order to join the group'),
    
key_defs = [
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'project_RID_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['name'],
                constraint_names=[('isa', 'project_name_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['id'],
                constraint_names=[('isa', 'project_pkey')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['groups'],
            '_acl_admin', 'group_lists', ['name'],
            constraint_names = [('isa', 'project_groups_fkey')],
    ),
]

table_annotations =
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

table_def = em.Table.define(
    project,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment='domain',
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

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

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
