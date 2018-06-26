import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'protocol_treatment'
schema_name = 'isa'

column_defs = [
    em.Column.define('protocol', em.builtin_types['text'],
        nullok = False,
        comment = 'Protocol Foreign key.',
    ),
    em.Column.define('treatment', em.builtin_types['text'],
        nullok = False,
        comment = 'Treatment foreign key.',
    ),
    em.Column.define('treatment_concentration', em.builtin_types['float4'],
        nullok = True,
        comment = 'Concentration of treatment applied to a cell line in mM.',
    ),
]


key_defs = [
    em.Key.define(['protocol', 'treatment'],
                   constraint_names=[('isa', 'protocol_treatment_RID_key')],
        comment = protocol and treatment must be distinct.,
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'protocol_treatment_RIDkey1')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['treatment'],
            'vocab', 'treatment_terms', ['id'],
            constraint_names = [('isa', 'protocol_treatment_treatment_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        comment = 'Must be a valid reference to a treatment.',
    ),
    em.ForeignKey.define(['protocol'],
            'isa', 'protocol', ['RID'],
            constraint_names = [('isa', 'protocol_treatment_protocol_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_delete = 'CASCADE',
    ),
]


visible_columns=\
{   'compact': [   'RID',
                   ['isa', 'protocol_treatment_protocol_fkey'],
                   ['isa', 'protocol_treatment_treatment_fkey'],
                   'treatment_concentration'],
    'detailed': [   'RID',
                    'RMT',
                    ['isa', 'protocol_treatment_protocol_fkey'],
                    ['isa', 'protocol_treatment_treatment_fkey'],
                    'treatment_concentration'],
    'entry': [   'RID',
                 ['isa', 'protocol_treatment_protocol_fkey'],
                 ['isa', 'protocol_treatment_treatment_fkey'],
                 'treatment_concentration'],
    'filter': {   'and': [   {   'open': True,
                                 'source': [   {   'outbound': [   'isa',
                                                                   'protocol_treatment_treatment_fkey']},
                                               'name']},
                             {   'open': True,
                                 'source': ['treatment_concentration']}]}}

visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns" : visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys" : visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display": table_display,
}


table_def = em.Table.define('protocol_treatment',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='Table of biological speciments from which biosamples will be created.',
    provide_system = True
)
