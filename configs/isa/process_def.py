import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'process'
schema_name = 'isa'

column_defs = [
    em.Column.define('process_url', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['markdown'],
    ),
    em.Column.define('file_url', em.builtin_types['text'],
    ),
    em.Column.define('filename', em.builtin_types['text'],
    ),
    em.Column.define('byte_count', em.builtin_types['int4'],
    ),
    em.Column.define('md5', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'process_pkey')],
    ),
    em.Key.define(['description'],
                   constraint_names=[('isa', 'process_description_key')],
    ),
]


fkey_defs = [
]


visible_columns={}
visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
}
column_comment = \
{'RCB': None,
 'RCT': None,
 'RID': None,
 'RMB': None,
 'RMT': None,
 'byte_count': None,
 'description': None,
 'file_url': None,
 'filename': None,
 'md5': None,
 'process_url': None}



table_def = em.Table.define('process',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
