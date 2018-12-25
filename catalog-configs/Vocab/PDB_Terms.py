import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

table_name = 'PDB_Terms'

schema_name = 'Vocab'

column_annotations = {'ID': {}, 'URI': {}, 'Name': {}, 'Description': {}, 'Synonyms': {}}

column_comment = {
    'ID': 'The preferred Compact URI (CURIE) for this term.',
    'URI': 'The preferred URI for this term.',
    'Name': 'The preferred human-readable name for this term.',
    'Description': 'A longer human-readable description of this term.',
    'Synonyms': 'Alternate human-readable names for this term.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'ID',
        em.builtin_types['ermrest_curie'],
        nullok=False,
        default='PBCCONSORTIUM:{RID}',
        comment=column_comment['ID'],
    ),
    em.Column.define(
        'URI',
        em.builtin_types['ermrest_uri'],
        nullok=False,
        default='/id/{RID}',
        comment=column_comment['URI'],
    ),
    em.Column.define(
        'Name', em.builtin_types['text'], nullok=False, comment=column_comment['Name'],
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
        nullok=False,
        comment=column_comment['Description'],
    ),
    em.Column.define('Synonyms', em.builtin_types['text[]'], comment=column_comment['Synonyms'],
                     ),
]

table_annotations = {}
table_comment = 'Terms from PDB Repository'
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(['URI'], constraint_names=[('Vocab', 'PDB_Terms_URIkey1')],
                  ),
    em.Key.define(['ID'], constraint_names=[('Vocab', 'PDB_Terms_IDkey1')],
                  ),
    em.Key.define(['RID'], constraint_names=[('Vocab', 'PDB_Terms_RIDkey1')],
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

