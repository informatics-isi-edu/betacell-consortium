import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'model_json'
schema_name = 'viz'

column_defs = [
    em.Column.define('id', em.builtin_types['text'],
    ),
    em.Column.define('label', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('bgcolor', em.builtin_types['jsonb'],
    ),
    em.Column.define('bboxcolor', em.builtin_types['jsonb'],
    ),
    em.Column.define('volume', em.builtin_types['jsonb'],
    ),
    em.Column.define('mesh', em.builtin_types['jsonb'],
    ),
    em.Column.define('landmark', em.builtin_types['jsonb'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('', 'viz_model_json_RID_pkey')],
    ),
]


fkey_defs = [
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


table_def = em.Table.define('model_json',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
