import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'experiment_type_terms'

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
    'filter': {
        'and': [
            {
                'source': 'name',
                'open': True
            }, {
                'source': 'id',
                'open': True
            }, {
                'source': 'synonyms',
                'open': True
            }
        ]
    },
    'entry': ['name', 'id', 'synonyms', 'uri', 'description'],
    'detailed': ['name', 'id', 'synonyms', 'uri', 'description'],
    'compact': ['name', 'id', 'synonyms', 'description']
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }
table_comment = 'Terms for experiment types'
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(['id'], constraint_names=[('vocab', 'experiment_type_terms_idkey1')],
                  ),
    em.Key.define(['RID'], constraint_names=[('vocab', 'experiment_type_terms_RIDkey1')],
                  ),
    em.Key.define(['uri'], constraint_names=[('vocab', 'experiment_type_terms_urikey1')],
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
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_table=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)

