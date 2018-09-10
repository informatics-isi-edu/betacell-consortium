import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'cvterm_relationship'
schema_name = 'data_commons'

column_defs = [
    em.Column.define('cvterm_relationship_id', em.builtin_types['serial8'],
        nullok=False,
    ),
    em.Column.define('type_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('subject_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('object_dbxref', em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define('cv', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['cvterm_relationship_id'],
                   constraint_names=[('data_commons', 'cvterm_relationship_pkey')],
    ),
    em.Key.define(['object_dbxref', 'type_dbxref', 'subject_dbxref'],
                   constraint_names=[('data_commons', 'cvterm_relationship_type_dbxref_subject_dbxref_object_dbxre_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('data_commons', 'cvterm_relationship_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['subject_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvterm_relationship_subject_dbxref_fkey')],
    ),
    em.ForeignKey.define(['type_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvterm_relationship_type_dbxref_fkey')],
    ),
    em.ForeignKey.define(['cv'],
            'data_commons', 'cv', ['name'],
            constraint_names=[('data_commons', 'cvterm_relationship_cv_fkey')],
    ),
    em.ForeignKey.define(['object_dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names=[('data_commons', 'cvterm_relationship_object_dbxref_fkey')],
    ),
]


visible_columns = {}
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


table_def = em.Table.define('cvterm_relationship',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
