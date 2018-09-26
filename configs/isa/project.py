import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'project'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('funding', em.builtin_types['text'],
    ),
    em.Column.define('url', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{{url}}}]({{{url}}})'}}},
        comment='url for more information on this project on externalre site',
    ),
    em.Column.define('name', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{pis}}}: {{{name}}}'}}},
    ),
    em.Column.define('abstract', em.builtin_types['markdown'],
    ),
    em.Column.define('pis', em.builtin_types['text'],
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'List of PI Last Names'}},
        comment='List of Last Names of Principal Investigator separated by /',
    ),
    em.Column.define('groups', em.builtin_types['text'],
        acls={'select': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a', 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'], 'enumerate': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a', 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d']},
        acl_bindings={'project_edit_guard': False},
        comment='Users must be a member of the referenced ACL group in order to edit project records.',
    ),
    em.Column.define('group_membership_url', em.builtin_types['text'],
        acls={'select': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a', 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'], 'enumerate': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a', 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d']},
        acl_bindings={'project_edit_guard': False},
        comment='URL that project members will need in order to join the group',
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('isa', 'project_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'project_RID_key')],
    ),
    em.Key.define(['name'],
                   constraint_names=[('isa', 'project_name_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['groups'],
            '_acl_admin', 'group_lists', ['name'],
            constraint_names=[('isa', 'project_groups_fkey')],
    ),
]


visible_columns = \
{'compact': ['name', 'abstract'],
 'detailed': ['name', 'funding', 'url', 'abstract', 'group_membership_url',
              ['isa', 'project_publication_project_id_fkey']],
 'entry': ['name', 'funding', 'url', 'abstract', 'pis',
           ['isa', 'project_groups_fkey'], 'group_membership_url'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Investigator',
                     'open': True,
                     'source': [{'inbound': ['isa',
                                             'project_investigator_project_id_fkey']},
                                'username']},
                    {'entity': False, 'open': False, 'source': 'funding'},
                    {'entity': True,
                     'markdown_name': 'Publication',
                     'open': False,
                     'source': [{'inbound': ['isa',
                                             'project_publication_project_id_fkey']},
                                'pmid']}]}}

visible_foreign_keys = \
{'detailed': [['isa', 'project_investigator_project_id_fkey'],
              ['isa', 'project_member_project_id_fkey'],
              ['isa', 'dataset_project_fkey']]}

table_comment = \
'domain'

table_display = \
{'compact': {'row_order': [{'column': 'pis', 'descending': False}]},
 'row_name': {'row_markdown_pattern': '{{{pis}}}: {{{name}}}'}}

table_acls = {}
table_acl_bindings = \
{'project_edit_guard': {'projection': [{'outbound': ['isa',
                                                     'project_groups_fkey']},
                                       'groups'],
                        'projection_type': 'acl',
                        'scope_acl': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                      'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                      'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                        'types': ['update', 'delete']}}

table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp',
 'group_membership_url': 'URL that project members will need in order to join '
                         'the group',
 'groups': 'Users must be a member of the referenced ACL group in order to '
           'edit project records.',
 'pis': 'List of Last Names of Principal Investigator separated by /',
 'url': 'url for more information on this project on externalre site'}

column_annotations = \
{'name': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{pis}}}: '
                                                                                   '{{{name}}}'}}},
 'pis': {'tag:misd.isi.edu,2015:display': {'name': 'List of PI Last Names'}},
 'url': {'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{{url}}}]({{{url}}})'}}}}

column_acls = \
{'group_membership_url': {'enumerate': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                                        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                        'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                          'select': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                     'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                                     'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                     'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d']},
 'groups': {'enumerate': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                          'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                          'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                          'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
            'select': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                       'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
                       'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                       'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d']}}

column_acl_bindings = \
{'group_membership_url': {'project_edit_guard': False},
 'groups': {'project_edit_guard': False}}



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
