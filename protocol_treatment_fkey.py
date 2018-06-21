
fkey_defs = [
    em.ForeignKey.define(
            ['treatment'],
            'vocab', 'treatment_terms', ['RID'],
            constraint_names=[('isa', 'protocol_treatment_treatment_fkey')],
            annotations={},
            acls={'insert': ['*'], 'update': ['*']},
            acl_bindings={},
            on_update='NO ACTION', on_delete='NO ACTION',
            comment='Must be a valid reference to a treatment.'),
    em.ForeignKey.define(
            ['protocol'],
            'isa', 'protocol', ['RID'],
            constraint_names=[('isa', 'protocol_treatment_protocol_fkey')],
            annotations={},
            acls={'insert': ['*'], 'update': ['*']},
            acl_bindings={},
            on_update='NO ACTION', on_delete='NO ACTION',
            comment=None),
]
