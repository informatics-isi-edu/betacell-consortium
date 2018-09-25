import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cvtermpath'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('cvtermpath_id', em.builtin_types['serial8'],
        nullok=False,
    ),
    em.Column.define('type_dbxref', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Type'}},
    ),
    em.Column.define('subject_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('object_dbxref', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'Object'}},
    ),
    em.Column.define('cv', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('pathdistance', em.builtin_types['int4'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['cvtermpath_id'],
                   constraint_names=[('data_commons', 'cvtermpath_pkey')],
    ),
    em.Key.define(['subject_dbxref', 'type_dbxref', 'object_dbxref'],
                   constraint_names=[('data_commons', 'cvtermpath_type_dbxref_subject_dbxref_object_dbxref_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'cvtermpath_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['object_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvtermpath_object_dbxref_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'from_name': 'Relationship paths with this term as object', 'to_name': 'Object'}},
    ),
    em.ForeignKey.define(['subject_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvtermpath_subject_dbxref_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'from_name': 'Relationship paths with this term as subject', 'to_name': 'Subject'}},
    ),
    em.ForeignKey.define(['type_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvtermpath_type_dbxref_fkey')],
    ),
    em.ForeignKey.define(['cv'],
            'data_commons', 'cv', ['name'],
            constraint_names=[('data_commons', 'cvtermpath_cv_fkey')],
    ),
]


visible_columns = \
{'*': [['data_commons', 'cvtermpath_subject_dbxref_fkey'],
       ['data_commons', 'cvtermpath_type_dbxref_fkey'],
       ['data_commons', 'cvtermpath_object_dbxref_fkey'], 'pathdistance']}

visible_foreign_keys = {}
table_comment = \
None

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}
column_annotations = \
{'object_dbxref': {'tag:misd.isi.edu,2015:display': {'name': 'Object'}},
 'type_dbxref': {'tag:misd.isi.edu,2015:display': {'name': 'Type'}}}



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
