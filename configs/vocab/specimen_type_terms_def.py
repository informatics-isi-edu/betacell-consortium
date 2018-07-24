import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'specimen_type_terms'
schema_name = 'vocab'

column_defs = [
    em.Column.define('id', em.builtin_types['ermrest_curie'],
        nullok=False,
        comment='The preferred Compact URI (CURIE) for this term.',
    ),
    em.Column.define('uri', em.builtin_types['ermrest_uri'],
        nullok=False,
        comment='The preferred URI for this term.',
    ),
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
        comment='The preferred human-readable name for this term.',
    ),
    em.Column.define('description', em.builtin_types['markdown'],
        nullok=False,
        comment='A longer human-readable description of this term.',
    ),
    em.Column.define('synonyms', em.builtin_types['text[]'],
        comment='Alternate human-readable names for this term.',
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('vocab', 'specimen_type_terms_idkey1')],
    ),
    em.Key.define(['uri'],
                   constraint_names=[('vocab', 'specimen_type_terms_urikey1')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('vocab', 'specimen_type_terms_RIDkey1')],
    ),
]


fkey_defs = [
]


visible_columns=\
{'compact': ['name', 'id', 'synonyms', 'description'],
 'detailed': ['name', 'id', 'synonyms', 'uri', 'description'],
 'entry': ['name', 'id', 'synonyms', 'uri', 'description'],
 'filter': {'and': [{'open': True, 'source': 'name'},
                    {'open': True, 'source': 'id'},
                    {'open': True, 'source': 'synonyms'}]}}

visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}


table_def = em.Table.define('specimen_type_terms',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='Terms for specimen types',
    provide_system = True
)
