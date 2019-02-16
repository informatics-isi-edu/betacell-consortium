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

table_name = 'anatomy_terms'

schema_name = 'vocab'

column_annotations = {'id': {}, 'uri': {}, 'name': {}, 'description': {}, 'synonyms': {}}

column_comment = {
    'id': 'The preferred Compact URI (CURIE) for this term.',
    'uri': 'The preferred URI for this term.',
    'name': 'The preferred human-readable name for this term.',
    'description': 'A longer human-readable description of this term.',
    'synonyms': 'Alternate human-readable names for this term.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'id',
        em.builtin_types['ermrest_curie'],
        nullok=False,
        default='PBCCONSORTIUM:{RID}',
        comment=column_comment['id'],
    ),
    em.Column.define(
        'uri',
        em.builtin_types['ermrest_uri'],
        nullok=False,
        default='/id/{RID}',
        comment=column_comment['uri'],
    ),
    em.Column.define(
        'name', em.builtin_types['text'], nullok=False, comment=column_comment['name'],
    ),
    em.Column.define(
        'description',
        em.builtin_types['markdown'],
        nullok=False,
        comment=column_comment['description'],
    ),
    em.Column.define('synonyms', em.builtin_types['text[]'], comment=column_comment['synonyms'],
                     ),
]

visible_columns = {
    'entry': ['name', 'id', 'synonyms', 'uri', 'description'],
    'filter': {
        'and': [
            {
                'open': True,
                'source': 'name'
            }, {
                'open': True,
                'source': 'id'
            }, {
                'open': True,
                'source': 'synonyms'
            }
        ]
    },
    'compact': ['name', 'id', 'synonyms', 'description'],
    'detailed': ['name', 'id', 'synonyms', 'uri', 'description']
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Terms for anatomy'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('vocab', 'anatomy_terms_RIDkey1')],
                  ),
    em.Key.define(['id'], constraint_names=[('vocab', 'anatomy_terms_idkey1')],
                  ),
    em.Key.define(['uri'], constraint_names=[('vocab', 'anatomy_terms_urikey1')],
                  ),
]

fkey_defs = []

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

