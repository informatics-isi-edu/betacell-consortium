import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'process'
schema_name = 'isa'

column_annotations = {}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('process_url', em.builtin_types['text'],),
               em.Column.define('description', em.builtin_types['markdown'],),
               em.Column.define('file_url', em.builtin_types['text'],),
               em.Column.define('filename', em.builtin_types['text'],),
               em.Column.define('byte_count', em.builtin_types['int4'],),
               em.Column.define('md5', em.builtin_types['text'],),
               ]

visible_columns = {}

visible_foreign_keys = {}

table_display = {}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'None'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['description'],
                  constraint_names=[('isa', 'process_description_key')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('isa', 'process_pkey')],
                  ),
]

fkey_defs = [
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
