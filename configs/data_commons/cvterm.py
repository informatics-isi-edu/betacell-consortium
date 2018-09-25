import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cvterm'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('dbxref', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Code'}},
    ),
    em.Column.define('dbxref_unversioned', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('cv', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Controlled Vocabulary'}},
    ),
    em.Column.define('name', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('definition', em.builtin_types['text'],
    ),
    em.Column.define('is_obsolete', em.builtin_types['boolean'],
        nullok=False,
    ),
    em.Column.define('is_relationshiptype', em.builtin_types['boolean'],
        nullok=False,
    ),
    em.Column.define('synonyms', em.builtin_types['text[]'],
        annotations={'tag:isrd.isi.edu,2016:generated': None},
    ),
    em.Column.define('alternate_dbxrefs', em.builtin_types['text[]'],
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Alternate Codes'}, 'tag:isrd.isi.edu,2016:generated': None},
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'cvterm_RID_key')],
    ),
    em.Key.define(['cv', 'name', 'is_obsolete'],
                   constraint_names=[('data_commons', 'cvterm_cv_name_is_obsolete_key')],
    ),
    em.Key.define(['dbxref'],
                   constraint_names=[('data_commons', 'cvterm_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dbxref'],
            'data_commons', 'dbxref', ['name'],
            constraint_names=[('data_commons', 'cvterm_dbxref_fkey')],
    ),
    em.ForeignKey.define(['cv'],
            'data_commons', 'cv', ['name'],
            constraint_names=[('data_commons', 'cvterm_cv_fkey')],
    ),
]


visible_columns = \
{'*': ['name', ['data_commons', 'cvterm_dbxref_fkey'], 'definition',
       ['data_commons', 'cvterm_cv_fkey'], 'is_obsolete', 'is_relationshiptype',
       'synonyms', 'alternate_dbxrefs'],
 'entry/create': ['name', ['data_commons', 'cvterm_cv_fkey'], 'definition',
                  'is_obsolete', 'is_relationshiptype'],
 'filter': {'and': [{'source': 'name'}, {'source': 'dbxref'},
                    {'source': 'definition'}, {'source': 'cv'},
                    {'source': 'is_obsolete'},
                    {'source': 'is_relationshiptype'}]}}

visible_foreign_keys = {}
table_comment = \
None

table_display = \
{'*': {'row_order': [{'column': 'name'}]},
 'row_name': {'row_markdown_pattern': '{{name}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
}
column_annotations = \
{'alternate_dbxrefs': {'tag:isrd.isi.edu,2016:generated': None,
                       'tag:misd.isi.edu,2015:display': {'name': 'Alternate '
                                                                 'Codes'}},
 'cv': {'tag:misd.isi.edu,2015:display': {'name': 'Controlled Vocabulary'}},
 'dbxref': {'tag:misd.isi.edu,2015:display': {'name': 'Code'}},
 'synonyms': {'tag:isrd.isi.edu,2016:generated': None}}



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
