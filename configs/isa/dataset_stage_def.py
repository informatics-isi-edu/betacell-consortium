import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'dataset_stage'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset_id', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('stage', em.builtin_types['text'],
        nullok=False,
    ),
]


key_defs = [
    em.Key.define(['stage', 'dataset_id'],
                   constraint_names=[('isa', 'dataset_stage_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'dataset_stage_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset_id'],
            'isa', 'dataset', ['id'],
            constraint_names=[('isa', 'dataset_stage_dataset_id_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Datasets'}},
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(['stage'],
            'vocab', 'stage_terms', ['dbxref'],
            constraint_names=[('isa', 'dataset_stage_stage_fkey')],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Stage'}},
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]


visible_columns={}
visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:misd.isi.edu,2015:display":
{'name': 'Stage'}
,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}


table_def = em.Table.define('dataset_stage',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)
