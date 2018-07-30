import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'alignment'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('name', em.builtin_types['text'],
    ),
    em.Column.define('aligner', em.builtin_types['text'],
    ),
    em.Column.define('aligner_version', em.builtin_types['text'],
    ),
    em.Column.define('aligner_flags', em.builtin_types['text'],
    ),
    em.Column.define('reference_genome', em.builtin_types['text'],
    ),
    em.Column.define('transcriptome_model', em.builtin_types['text'],
    ),
    em.Column.define('sequence_trimming', em.builtin_types['text'],
    ),
    em.Column.define('trimmed_seqs', em.builtin_types['text'],
    ),
    em.Column.define('trimming_method', em.builtin_types['text'],
    ),
    em.Column.define('duplicate_removal', em.builtin_types['text'],
    ),
    em.Column.define('prealign_seq_removal', em.builtin_types['text'],
    ),
]


key_defs = [
    em.Key.define(['id'],
                   constraint_names=[('isa', 'alignment_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'alignment_RID_key')],
    ),
]


fkey_defs = [
]


visible_columns = \
{'compact': ['name', 'aligner', 'aligner_version', 'aligner_flags',
             'reference_genome', 'transcriptome_model', 'sequence_trimming',
             'trimmed_seqs', 'trimming_method', 'duplicate_removal',
             'prealign_seq_removal'],
 'detailed': ['name', 'aligner', 'aligner_version', 'aligner_flags',
              'reference_genome', 'transcriptome_model', 'sequence_trimming',
              'trimmed_seqs', 'trimming_method', 'duplicate_removal',
              'prealign_seq_removal']}

visible_foreign_keys = {}
table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
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



table_def = em.Table.define('alignment',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
