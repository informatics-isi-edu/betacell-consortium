import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Collection_Biosample'
schema_name = 'Beta_Cell'

column_annotations = {'Biosample': {}, 'Collection': {}}

column_comment = {
    'Biosample': 'Biosample foreign key.',
    'Collection': 'Collection foreign key.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
    ),
    em.Column.define(
        'Collection',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Collection'],
    ),
    em.Column.define(
        'Biosample',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Biosample'],
    ),
]

visible_columns = {'*': ['RID',
                         ['Common', 'Collection_Biosample_Collection_fkey'],
                         ['Beta_Cell', 'Collection_Biosample_Biosample_fkey']]}

visible_foreign_keys = {}

table_display = {}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['Collection', 'Biosample'],
                  constraint_names=[
                      ('Beta_Cell', 'Collection_Biosample_Collection_Biosample_key')],
                  comment='protocol and compound must be distinct.',
                  ),
    em.Key.define(['RID'],
                  constraint_names=[
                      ('Beta_Cell', 'Collection_Biosample_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Biosample'],
                         'Beta_Cell', 'Biosample', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Collection_Biosample_Biosample_fkey')],
                         ),
    em.ForeignKey.define(['Collection'],
                         'Common', 'Collection', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Collection_Biosample_Collection_fkey')],
                         comment='Must be a valid reference to an collection.',
                         ),
]

table_def = em.Table.define(table_name,
                            column_defs=column_defs,
                            key_defs=key_defs,
                            fkey_defs=fkey_defs,
                            annotations=table_annotations,
                            acls=table_acls,
                            acl_bindings=table_acl_bindings,
                            comment=table_comment,
                            provide_system=True
                            )



def main():
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    update_catalog.update_table(server, catalog_id, schema_name, table_name, table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
