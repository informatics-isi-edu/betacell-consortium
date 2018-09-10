import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'external_reference'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('url', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:isrd.isi.edu,2016:column-display': {'detailed': {'markdown_pattern': '[{{url}}]({{url}})'}}},
        comment='asset/reference',
    ),
    em.Column.define('link_text', em.builtin_types['text'],
    ),
    em.Column.define('description', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[{{description}}]({{url}})'}}},
    ),
]


key_defs = [
    em.Key.define(['url', 'id'],
                   constraint_names=[('isa', 'external_reference_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'external_reference_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['id'],
            'isa', 'dataset', ['id'],
            constraint_names=[('isa', 'external_reference_id_fkey')],
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
]


visible_columns = \
{'compact': ['description'],
 'detailed': ['description', 'url'],
 'entry': ['description', 'url']}

visible_foreign_keys = {}
table_comment = \
None

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:misd.isi.edu,2015:display":
{'name': 'Additional Information'}
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
 'RMT': 'System-generated row modification timestamp',
 'url': 'asset/reference'}

column_annotations = \
{'description': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[{{description}}]({{url}})'}}},
 'url': {'tag:isrd.isi.edu,2016:column-display': {'detailed': {'markdown_pattern': '[{{url}}]({{url}})'}}}}



table_def = em.Table.define('external_reference',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
