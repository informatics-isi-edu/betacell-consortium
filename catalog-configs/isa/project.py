import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'project'
schema_name = 'isa'

groups = AttrDict({
    'admins':
    'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'modelers':
    'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
    'curators':
    'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'writers':
    'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'readers':
    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'isrd':
    'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
})

tags = AttrDict({
    'immutable':
    'tag:isrd.isi.edu,2016:immutable',
    'display':
    'tag:misd.isi.edu,2015:display',
    'visible_columns':
    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys':
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':
    'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':
    'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives':
    'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':
    'tag:isrd.isi.edu,2016:column-display',
    'asset':
    'tag:isrd.isi.edu,2017:asset',
    'export':
    'tag:isrd.isi.edu,2016:export',
    'generated':
    'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':
    'tag:isrd.isi.edu,2017:bulk-upload'
})

column_annotations = {
    'url': {
        tags.column_display: {
            '*': {
                'markdown_pattern': '[{{{url}}}]({{{url}}})'
            }
        }
    },
    'name': {
        tags.column_display: {
            'compact': {
                'markdown_pattern': '{{{pis}}}: {{{name}}}'
            }
        }
    },
    'RID': {},
    'RCB': {},
    'RMB': {},
    'RCT': {},
    'RMT': {},
    'pis': {
        tags.display: {
            'name': 'List of PI Last Names'
        }
    },
    'groups': {},
    'group_membership_url': {}
}

column_comment = {
    'url':
    'url for more information on this project on externalre site',
    'RID':
    'System-generated unique row ID.',
    'RCB':
    'System-generated row created by user provenance.',
    'RMB':
    'System-generated row modified by user provenance.',
    'RCT':
    'System-generated row creation timestamp.',
    'RMT':
    'System-generated row modification timestamp',
    'pis':
    'List of Last Names of Principal Investigator separated by /',
    'groups':
    'Users must be a member of the referenced ACL group in order to edit project records.',
    'group_membership_url':
    'URL that project members will need in order to join the group'
}

column_acls = {
    'groups': {
        'select': [
            groups.writers,
            'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
            groups.readers,
            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
        ],
        'enumerate': [
            groups.writers,
            'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
            groups.readers,
            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
        ]
    },
    'group_membership_url': {
        'select': [
            groups.writers,
            'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
            groups.readers,
            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
        ],
        'enumerate': [
            groups.writers,
            'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
            groups.readers,
            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
        ]
    }
}

column_acl_bindings = {
    'groups': {
        'project_edit_guard': False
    },
    'group_membership_url': {
        'project_edit_guard': False
    }
}

column_defs = [
    em.Column.define(
        'id',
        em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define(
        'funding',
        em.builtin_types['text'],
    ),
    em.Column.define(
        'url',
        em.builtin_types['text'],
        annotations=column_annotations['url'],
        comment=column_comment['url'],
    ),
    em.Column.define(
        'name',
        em.builtin_types['text'],
        annotations=column_annotations['name'],
    ),
    em.Column.define(
        'abstract',
        em.builtin_types['markdown'],
    ),
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
        comment=column_comment['RID'],
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
        comment=column_comment['RCB'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
        comment=column_comment['RMB'],
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
        comment=column_comment['RCT'],
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
        comment=column_comment['RMT'],
    ),
    em.Column.define(
        'pis',
        em.builtin_types['text'],
        annotations=column_annotations['pis'],
        comment=column_comment['pis'],
    ),
    em.Column.define(
        'groups',
        em.builtin_types['text'],
        default='writers',
        acls=column_acls['groups'],
        acl_bindings=column_acl_bindings['groups'],
        comment=column_comment['groups'],
    ),
    em.Column.define(
        'group_membership_url',
        em.builtin_types['text'],
        acls=column_acls['group_membership_url'],
        acl_bindings=column_acl_bindings['group_membership_url'],
        comment=column_comment['group_membership_url'],
    ),
]

groups = AttrDict({
    'admins':
    'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'modelers':
    'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
    'curators':
    'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'writers':
    'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'readers':
    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'isrd':
    'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
})

tags = AttrDict({
    'immutable':
    'tag:isrd.isi.edu,2016:immutable',
    'display':
    'tag:misd.isi.edu,2015:display',
    'visible_columns':
    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys':
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':
    'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':
    'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives':
    'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':
    'tag:isrd.isi.edu,2016:column-display',
    'asset':
    'tag:isrd.isi.edu,2017:asset',
    'export':
    'tag:isrd.isi.edu,2016:export',
    'generated':
    'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':
    'tag:isrd.isi.edu,2017:bulk-upload'
})

visible_columns = {
    'filter': {
        'and': [{
            'source': [{
                'inbound': ['isa', 'project_investigator_project_id_fkey']
            }, 'username'],
            'open':
            True,
            'markdown_name':
            'Investigator',
            'entity':
            True
        }, {
            'source': 'funding',
            'open': False,
            'entity': False
        },
                {
                    'source': [{
                        'inbound':
                        ['isa', 'project_publication_project_id_fkey']
                    }, 'pmid'],
                    'open':
                    False,
                    'markdown_name':
                    'Publication',
                    'entity':
                    True
                }]
    },
    'entry': [
        'name', 'funding', 'url', 'abstract', 'pis',
        ['isa', 'project_groups_fkey'], 'group_membership_url'
    ],
    'detailed': [
        'name', 'funding', 'url', 'abstract', 'group_membership_url',
        ['isa', 'project_publication_project_id_fkey']
    ],
    'compact': ['name', 'abstract']
}

visible_foreign_keys = {
    'detailed': [['isa', 'project_investigator_project_id_fkey'],
                 ['isa', 'project_member_project_id_fkey'],
                 ['isa', 'dataset_project_fkey']]
}

table_display = {
    'compact': {
        'row_order': [{
            'column': 'pis',
            'descending': False
        }]
    },
    'row_name': {
        'row_markdown_pattern': '{{{pis}}}: {{{name}}}'
    }
}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'domain'

table_acls = {}

table_acl_bindings = {
    'project_edit_guard': {
        'scope_acl': [
            groups.writers, groups.readers,
            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
        ],
        'projection': [{
            'outbound': ['isa', 'project_groups_fkey']
        }, 'groups'],
        'types': ['update', 'delete'],
        'projection_type':
        'acl'
    }
}

key_defs = [
    em.Key.define(
        ['RID'],
        constraint_names=[('isa', 'project_RID_key')],
    ),
    em.Key.define(
        ['name'],
        constraint_names=[('isa', 'project_name_key')],
    ),
    em.Key.define(
        ['id'],
        constraint_names=[('isa', 'project_pkey')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['groups'],
        '_acl_admin',
        'group_lists',
        ['name'],
        constraint_names=[('isa', 'project_groups_fkey')],
    ),
]

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True)


def main(skip_args=False, mode='annotations', replace=False, server='pbcconsortium.isrd.isi.edu', catalog_id=1):
    
    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
