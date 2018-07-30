import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'origin_terms'
schema_name = 'vocab'

column_defs = [
    em.Column.define('dbxref', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Code'}, 'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{dbxref}}](/chaise/record/#1/data_commons:cvterm/dbxref={{#encode}}{{dbxref}}{{/encode}})'}}},
    ),
    em.Column.define('dbxref_unversioned', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('cv', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Controlled Vocabulary'}, 'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('definition', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('is_obsolete', em.builtin_types['boolean'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('is_relationshiptype', em.builtin_types['boolean'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('synonyms', em.builtin_types['text[]'],
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('alternate_dbxrefs', em.builtin_types['text[]'],
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Alternate Codes'}, 'tag:isrd.isi.edu,2016:generated': None},
    ),
]


key_defs = [
    em.Key.define(['cv', 'is_obsolete', 'name'],
                   constraint_names=[('vocab', 'origin_terms_cv_name_is_obsolete_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('vocab', 'origin_terms_RID_key')],
    ),
    em.Key.define(['dbxref'],
                   constraint_names=[('vocab', 'origin_terms_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['cv'],
            'data_commons', 'cv', ['name'],
            constraint_names=[('vocab', 'origin_terms_cv_fkey')],
    ),
    em.ForeignKey.define(['dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('vocab', 'origin_terms_dbxref_fkey')],
    ),
]


visible_columns = \
{'*': ['name', 'dbxref', 'definition', ['vocab', 'origin_terms_cv_fkey'],
       'is_obsolete', 'is_relationshiptype', 'synonyms', 'alternate_dbxrefs'],
 'entry': [['vocab', 'origin_terms_dbxref_fkey']],
 'filter': {'and': [{'source': 'name'}, {'source': 'dbxref'},
                    {'source': 'definition'}, {'source': 'cv'},
                    {'source': 'is_obsolete'},
                    {'source': 'is_relationshiptype'}]}}

visible_foreign_keys = \
{'*': [{'source': [{'inbound': ['isa', 'dataset_origin_origin_fkey']},
                   {'outbound': ['isa', 'dataset_origin_dataset_id_fkey']},
                   'id']}]}

table_display = \
{'*': {'row_order': [{'column': 'name'}]},
 'row_name': {'row_markdown_pattern': '{{name}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_annotations = \
{'alternate_dbxrefs': {'tag:isrd.isi.edu,2016:generated': None,
                       'tag:misd.isi.edu,2015:display': {'name': 'Alternate '
                                                                 'Codes'}},
 'cv': {'tag:isrd.isi.edu,2016:generated': None,
        'tag:misd.isi.edu,2015:display': {'name': 'Controlled Vocabulary'}},
 'dbxref': {'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{dbxref}}](/chaise/record/#1/data_commons:cvterm/dbxref={{#encode}}{{dbxref}}{{/encode}})'}},
            'tag:misd.isi.edu,2015:display': {'name': 'Code'}},
 'dbxref_unversioned': {'tag:isrd.isi.edu,2016:generated': None},
 'definition': {'tag:isrd.isi.edu,2016:generated': None},
 'is_obsolete': {'tag:isrd.isi.edu,2016:generated': None},
 'is_relationshiptype': {'tag:isrd.isi.edu,2016:generated': None},
 'name': {'tag:isrd.isi.edu,2016:generated': None},
 'synonyms': {'tag:isrd.isi.edu,2016:generated': None}}



table_def = em.Table.define('origin_terms',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
