import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'project_publication'

schema_name = 'isa'

column_annotations = {
    'pmid': {
        chaise_tags.display: {
            'name': 'PMID'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '[{{{_pmid}}}](http://www.ncbi.nlm.nih.gov/pubmed/{{{_pmid}}})'
            }
        }
    },
    'RID': {},
    'RCB': {},
    'RMB': {},
    'RCT': {},
    'RMT': {}
}

column_comment = {
    'RID': 'System-generated unique row ID.',
    'RCB': 'System-generated row created by user provenance.',
    'RMB': 'System-generated row modified by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RMT': 'System-generated row modification timestamp'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'], nullok=False,
                     ),
    em.Column.define('project_id', em.builtin_types['int4'], nullok=False,
                     ),
    em.Column.define(
        'pmid', em.builtin_types['text'], nullok=False, annotations=column_annotations['pmid'],
    ),
]

visible_columns = {'*': [['isa', 'project_publication_project_id_fkey'], 'pmid']}

table_display = {
    'compact': {
        'row_markdown_pattern': '[Link to PubMed (PMID:{{{_pmid}}})](http://www.ncbi.nlm.nih.gov/pubmed/{{{_pmid}}})'
    },
    'row_name': {
        'row_markdown_pattern': 'PMID:{{{_pmid}}}'
    }
}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
}
table_comment = None
table_acls = {}
table_acl_bindings = {
    'project_suppl_edit_guard': {
        'scope_acl': [
            'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
            'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
        ],
        'projection': [
            {
                'outbound': ['isa', 'project_publication_project_id_fkey']
            }, {
                'outbound': ['isa', 'project_groups_fkey']
            }, 'groups'
        ],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['pmid', 'project_id'],
        constraint_names=[('isa', 'project_publication_project_id_pmid_key')],
    ),
    em.Key.define(['RID'], constraint_names=[('isa', 'project_publication_RID_key')],
                  ),
    em.Key.define(['id'], constraint_names=[('isa', 'project_publication_pkey')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['project_id'],
        'isa',
        'project', ['id'],
        constraint_names=[('isa', 'project_publication_project_id_fkey')],
        on_update='CASCADE',
        on_delete='CASCADE',
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
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_table=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)

