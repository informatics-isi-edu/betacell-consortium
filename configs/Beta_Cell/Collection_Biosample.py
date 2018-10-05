import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Collection_Biosample'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Collection', em.builtin_types['text'],
        nullok=False,
        comment='Collection foreign key.',
    ),
    em.Column.define('Biosample', em.builtin_types['text'],
        nullok=False,
        comment='Biosample foreign key.',
    ),
]


key_defs = [
    em.Key.define(['Biosample', 'Collection'],
                   constraint_names=[('Beta_Cell', 'Collection_Biosample_Collection_Biosample_key')],
       comment = 'protocol and compound must be distinct.',
    ),
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'Collection_Biosample_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Collection'],
            'Common', 'Collection', ['RID'],
            constraint_names=[('Beta_Cell', 'Collection_Biosample_Collection_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Must be a valid reference to an collection.',
    ),
    em.ForeignKey.define(['Biosample'],
            'Beta_Cell', 'Biosample', ['RID'],
            constraint_names=[('Beta_Cell', 'Collection_Biosample_Biosample_fkey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns = \
{'*': ['RID', ['Common', 'Collection_Biosample_Collection_fkey'],
       ['Beta_Cell', 'Collection_Biosample_Biosample_fkey']]}

visible_foreign_keys = {}
table_comment = \
None

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Biosample': 'Biosample foreign key.', 'Collection': 'Collection foreign key.'}

column_annotations = \
{}



table_def = em.Table.define(table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system = True
)
