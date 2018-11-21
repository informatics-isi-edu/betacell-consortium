import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'anatomy_terms'
schema_name = 'vocab'

column_annotations = {
    'description': {},
    'id': {},
    'name': {},
    'synonyms': {},
    'uri': {}}

column_comment = {
    'description': 'A longer human-readable description of this term.',
    'id': 'The preferred Compact URI (CURIE) for this term.',
    'name': 'The preferred human-readable name for this term.',
    'synonyms': 'Alternate human-readable names for this term.',
    'uri': 'The preferred URI for this term.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
    ),
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
        'name',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['name'],
    ),
    em.Column.define(
        'description',
        em.builtin_types['markdown'],
        nullok=False,
        comment=column_comment['description'],
    ),
    em.Column.define(
        'synonyms',
        em.builtin_types['text[]'],
        comment=column_comment['synonyms'],
    ),
]

visible_columns = {
    'compact': [
        'name', 'id', 'synonyms', 'description'], 'detailed': [
            'name', 'id', 'synonyms', 'uri', 'description'], 'entry': [
                'name', 'id', 'synonyms', 'uri', 'description'], 'filter': {
                    'and': [
                        {
                            'open': True, 'source': 'name'}, {
                                'open': True, 'source': 'id'}, {
                                    'open': True, 'source': 'synonyms'}]}}

table_annotations = {
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns, }

table_comment = 'Terms for anatomy'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['uri'],
                  constraint_names=[('vocab', 'anatomy_terms_urikey1')],
                  ),
    em.Key.define(['id'],
                  constraint_names=[('vocab', 'anatomy_terms_idkey1')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('vocab', 'anatomy_terms_RIDkey1')],
                  ),
]

fkey_defs = [
]

table_def = em.Table.define(table_name,
                            column_defs=column_defs,
                            key_defs=key_defs,
                            fkey_defs=fkey_defs,
                            annotations=table_annotations,
                            acls=table_acls,
                            acl_bindings=table_acl_bindings,
                            comment=table_comment,
                            provide_system=True
                            )


def main(skip_args=False, mode='annotations', replace=False, server='pbcconsortium.isrd.isi.edu', catalog_id=1):
    
    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
