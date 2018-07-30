import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'dataset_anatomy'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset_id', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('anatomy', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['anatomy', 'dataset_id'],
                   constraint_names=[('isa', 'dataset_anatomy_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'dataset_anatomy_RID_key')],
    ),
]


fkey_defs = [
]


visible_columns = {}
visible_foreign_keys = {}
table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:misd.isi.edu,2015:display":
{'name': 'Anatomy'}
,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}



table_def = em.Table.define('dataset_anatomy',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
