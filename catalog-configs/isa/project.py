import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pbcconsortium-reader': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'pbcconsortium-curator': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'pbcconsortium-writer': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'pbcconsortium-admin': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'isrd-testers': 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
}

table_name = 'project'

schema_name = 'isa'

column_annotations = {
    'url': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '[{{{url}}}]({{{url}}})'
            }
        }
    },
    'name': {
        chaise_tags.column_display: {
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
        chaise_tags.display: {
            'name': 'List of PI Last Names'
        }
    },
    'groups': {},
    'group_membership_url': {}
}

column_comment = {
    'url': 'url for more information on this project on externalre site',
    'RID': 'System-generated unique row ID.',
    'RCB': 'System-generated row created by user provenance.',
    'RMB': 'System-generated row modified by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RMT': 'System-generated row modification timestamp',
    'pis': 'List of Last Names of Principal Investigator separated by /',
    'groups': 'Users must be a member of the referenced ACL group in order to edit project records.',
    'group_membership_url': 'URL that project members will need in order to join the group'
}

column_acls = {
    'groups': {
        'select': [
            groups['pbcconsortium-writer'], groups['isrd-staff'], groups['pbcconsortium-reader'],
            groups['isrd-testers']
        ],
        'enumerate': [
            groups['pbcconsortium-writer'], groups['isrd-staff'], groups['pbcconsortium-reader'],
            groups['isrd-testers']
        ]
    },
    'group_membership_url': {
        'select': [
            groups['pbcconsortium-writer'], groups['isrd-staff'], groups['pbcconsortium-reader'],
            groups['isrd-testers']
        ],
        'enumerate': [
            groups['pbcconsortium-writer'], groups['isrd-staff'], groups['pbcconsortium-reader'],
            groups['isrd-testers']
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
    em.Column.define('id', em.builtin_types['serial4'], nullok=False,
                     ),
    em.Column.define('funding', em.builtin_types['text'],
                     ),
    em.Column.define(
        'url',
        em.builtin_types['text'],
        annotations=column_annotations['url'],
        comment=column_comment['url'],
    ),
    em.Column.define('name', em.builtin_types['text'], annotations=column_annotations['name'],
                     ),
    em.Column.define('abstract', em.builtin_types['markdown'],
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

visible_columns = {
    'entry': [
        'name', 'funding', 'url', 'abstract', 'pis', ['isa', 'project_groups_fkey'],
        'group_membership_url'
    ],
    'filter': {
        'and': [
            {
                'open': True,
                'entity': True,
                'source': [
                    {
                        'inbound': ['isa', 'project_investigator_project_id_fkey']
                    }, 'username'
                ],
                'markdown_name': 'Investigator'
            }, {
                'open': False,
                'entity': False,
                'source': 'funding'
            },
            {
                'open': False,
                'entity': True,
                'source': [{
                    'inbound': ['isa', 'project_publication_project_id_fkey']
                }, 'pmid'],
                'markdown_name': 'Publication'
            }
        ]
    },
    'compact': ['name', 'abstract'],
    'detailed': [
        'name', 'funding', 'url', 'abstract', 'group_membership_url',
        ['isa', 'project_publication_project_id_fkey']
    ]
}

visible_foreign_keys = {
    'detailed': [
        ['isa', 'project_investigator_project_id_fkey'], ['isa', 'project_member_project_id_fkey'],
        ['isa', 'dataset_project_fkey']
    ]
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
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'domain'

table_acls = {}

table_acl_bindings = {
    'project_edit_guard': {
        'types': ['update', 'delete'],
        'scope_acl': [
            groups['pbcconsortium-writer'], groups['pbcconsortium-reader'], groups['isrd-testers']
        ],
        'projection': [{
            'outbound': ['isa', 'project_groups_fkey']
        }, 'groups'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['id'], constraint_names=[('isa', 'project_pkey')],
                  ),
    em.Key.define(['name'], constraint_names=[('isa', 'project_name_key')],
                  ),
    em.Key.define(['RID'], constraint_names=[('isa', 'project_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['groups'],
        '_acl_admin',
        'group_lists', ['name'],
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
    provide_system=True
)


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_table(mode, schema_name, table_def, replace=replace)


if __name__ == "__main__":
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

