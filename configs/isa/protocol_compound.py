import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'protocol_compound'
schema_name = 'isa'

column_defs = [
    em.Column.define('protocol', em.builtin_types['text'],
        nullok=False,
        comment='Protocol Foreign key.',
    ),
    em.Column.define('compound', em.builtin_types['text'],
        nullok=False,
        comment='Compound foreign key.',
    ),
    em.Column.define('compound_concentration', em.builtin_types['float4'],
        comment='Concentration of compound applied to a cell line in mM.',
    ),
]


key_defs = [
    em.Key.define(['compound', 'protocol'],
                   constraint_names=[('isa', 'protocol_compound_RID_key')],
       comment = 'protocol and compound must be distinct.',
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'protocol_compound_RIDkey1')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['protocol'],
            'isa', 'protocol', ['RID'],
            constraint_names=[('isa', 'protocol_compound_protocol_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(['compound'],
            'vocab', 'compound_terms', ['id'],
            constraint_names=[('isa', 'protocol_compound_compound_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Must be a valid reference to a compound.',
    ),
]


visible_columns = \
{'compact': ['RID', ['isa', 'protocol_compound_protocol_fkey'],
             ['isa', 'protocol_compound_compound_fkey'],
             'compound_concentration'],
 'detailed': ['RID', 'RMT', ['isa', 'protocol_compound_protocol_fkey'],
              ['isa', 'protocol_compound_compound_fkey'],
              'compound_concentration'],
 'entry': ['RID', ['isa', 'protocol_compound_protocol_fkey'],
           ['isa', 'protocol_compound_compound_fkey'],
           'compound_concentration'],
 'filter': {'and': [{'open': True,
                     'source': [{'outbound': ['isa',
                                              'protocol_compound_compound_fkey']},
                                'name']},
                    {'open': True, 'source': ['compound_concentration']}]}}

visible_foreign_keys = {}
table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'compound': 'Compound foreign key.',
 'compound_concentration': 'Concentration of compound applied to a cell line '
                           'in mM.',
 'protocol': 'Protocol Foreign key.'}



table_def = em.Table.define('protocol_compound',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
