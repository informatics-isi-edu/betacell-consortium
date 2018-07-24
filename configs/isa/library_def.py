import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'library'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('name', em.builtin_types['text'],
    ),
    em.Column.define('library_type', em.builtin_types['text'],
    ),
    em.Column.define('library_adapters', em.builtin_types['text'],
    ),
    em.Column.define('pcr_cycles', em.builtin_types['text'],
    ),
    em.Column.define('library_yield', em.builtin_types['text'],
    ),
    em.Column.define('size_selection', em.builtin_types['text'],
    ),
    em.Column.define('platform', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'library_RID_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('isa', 'library_pkey')],
    ),
]


fkey_defs = [
]


visible_columns=\
{'compact': ['name', 'library_type', 'single_paired_end_sequencing',
             'library_adapters', 'pcr_cycles', 'library_yield',
             'size_selection', 'platform'],
 'detailed': ['name', 'library_type', 'single_paired_end_sequencing',
              'library_adapters', 'pcr_cycles', 'library_yield',
              'size_selection', 'platform']}

visible_foreign_keys=\
{'detailed': [['isa', 'sequencing_data_library_fkey']],
 'entry': [['isa', 'sequencing_data_library_fkey']]}

table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}


table_def = em.Table.define('library',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
