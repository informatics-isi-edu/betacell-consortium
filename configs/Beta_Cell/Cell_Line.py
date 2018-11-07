import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Cell_Line'
schema_name = 'Beta_Cell'

column_annotations = {'Anatomy': {},
                      'Cell_Line_Id': {},
                      'Description': {},
                      'Protocol': {},
                      'Species': {}}

column_comment = {'Anatomy': 'Anatomical region speciment was obtained from.',
                  'Cell_Line_Id': 'ID of cell line being used.',
                  'Description': 'Description of the specimen.',
                  'Protocol': 'Protocol used to create the cell line',
                  'Species': 'Species of the specimen'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Cell_Line_Id', em.builtin_types['text'], comment=column_comment['Cell_Line_Id'],),
               em.Column.define('Species', em.builtin_types['text'], comment=column_comment['Species'],),
               em.Column.define('Anatomy', em.builtin_types['text'], comment=column_comment['Anatomy'],),
               em.Column.define('Description', em.builtin_types['text'], comment=column_comment['Description'],),
               em.Column.define('Protocol', em.builtin_types['text'], comment=column_comment['Protocol'],),
               em.Column.define('Collection_Date', em.builtin_types['date'],),
               ]

visible_columns = {'*': [['Beta_Cell', 'Cell_Line_Key'],
                         ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey'],
                         ['Beta_Cell', 'Cell_Line_Species_FKey'],
                         ['Beta_Cell', 'Cell_Line_Anatomy_FKey'],
                         ['Beta_Cell', 'Cell_Line_Protocol_FKey'],
                         'Description',
                         'Collection_Date'],
                   'filter': {'and': [{'entity': True,
                                       'markdown_name': 'Cell Line',
                                       'open': True,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Cell_Line_Cell_Line_Terms_FKey']},
                                                  'name']},
                                      {'entity': True,
                                       'markdown_name': 'Species',
                                       'open': True,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Cell_Line_Species_FKey']},
                                                  'name']},
                                      {'entity': True,
                                       'markdown_name': 'Anatomy',
                                       'open': True,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Cell_Line_Anatomy_FKey']},
                                                  'name']}]}}

visible_foreign_keys = {'*': [{'source': [{'inbound': ['Beta_Cell',
                                                       'Specimen_Cell_Line_FKey']},
                                          'RID']}]}

table_display = {}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'table_display': {},
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'Table of cultured  from which specimens  will be created.'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'Cell_Line_Key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Species'],
                         'vocab', 'species_terms', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Cell_Line_Species_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         ),
    em.ForeignKey.define(['Anatomy'],
                         'vocab', 'anatomy_terms', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Cell_Line_Anatomy_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         ),
    em.ForeignKey.define(['Cell_Line_Id'],
                         'vocab', 'cell_line_terms', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         comment='Must be a valid reference to a cell line.',
                         ),
    em.ForeignKey.define(['Protocol'],
                         'Beta_Cell', 'Protocol', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Cell_Line_Protocol_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
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
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
