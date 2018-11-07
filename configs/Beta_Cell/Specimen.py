import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Specimen'
schema_name = 'Beta_Cell'

column_annotations = {
    'Cell_Line': {},
    'Collection_Date': {},
    'Description': {},
    'Protocol': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.Experiment_Protocol_FKey.rowName}}}'}}}}

column_comment = {'Cell_Line': 'Cell line used for the specimen.',
                  'Collection_Date': 'Date the specimen was obtained',
                  'Description': 'Description of the specimen.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Description', em.builtin_types['text'], comment=column_comment['Description'],),
               em.Column.define('Collection_Date', em.builtin_types['date'], comment=column_comment['Collection_Date'],),
               em.Column.define('Cell_Line', em.builtin_types['text'], comment=column_comment['Cell_Line'],),
               em.Column.define('Protocol', em.builtin_types['text'], annotations=column_annotations['Protocol'],),
               ]

visible_columns = {'*': ['RID',
                         'Protocol',
                         {'entity': True,
                             'markdown_name': 'Cell Line',
                             'open': True,
                             'source': [{'outbound': ['Beta_Cell',
                                                      'Specimen_Cell_Line_FKey']},
                                        {'outbound': ['Beta_Cell',
                                                      'Cell_Line_Cell_Line_Terms_FKey']},
                                        'name']},
                         {'markdown_name': 'Cellular Location',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Specimen_Cellular_Location_Terms_FKey']},
                                     'name']},
                         {'aggregate': 'array',
                          'comment': 'Additive used to treat the cell line for the '
                          'experiment',
                          'entity': True,
                          'markdown_name': 'Additive',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Specimen_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                     'RID']},
                         {'aggregate': 'array',
                          'comment': 'Concentration of additive applied to cell line in '
                          'mM',
                          'entity': True,
                          'markdown_name': 'Concentration',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Specimen_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     'Additive_Concentration'],
                          'ux_mode': 'choices'},
                         {'aggregate': 'array',
                             'comment': 'Duration in minutes',
                          'entity': True,
                          'markdown_name': 'Duration',
                          'source': [{'outbound': ['Beta_Cell',
                                                   'Specimen_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     'Duration'],
                             'ux_mode': 'choices'},
                         'Description',
                         'Collection_Date'],
                   'entry': [['Beta_Cell', 'Specimen_Cell_Line_FKey'],
                             ['Beta_Cell', 'Specimen_Protocol_FKey'],
                             ['Beta_Cell', 'Specimen_Cellular_Location_Terms_FKey'],
                             'Description',
                             'Collection_Date'],
                   'filter': {'and': [{'entity': True,
                                       'markdown_name': 'Cell Line',
                                       'open': True,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Specimen_Cell_Line_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Cell_Line_Cell_Line_Terms_FKey']},
                                                  'name']},
                                      {'markdown_name': 'Cellular Location',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Specimen_Cellular_Location_Terms_FKey']},
                                                  'name']},
                                      {'aggregate': 'array',
                                       'comment': 'Additive used to treat the cell '
                                       'line for the experiment',
                                       'entity': True,
                                       'markdown_name': 'Additive',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Specimen_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                                  'RID']},
                                      {'aggregate': 'array',
                                       'comment': 'Concentration of additive applied '
                                       'to cell line in mM',
                                       'entity': True,
                                       'markdown_name': 'Concentration',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Specimen_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  'Additive_Concentration'],
                                       'ux_mode': 'choices'},
                                      {'aggregate': 'array',
                                       'comment': 'Duration in minutes',
                                       'entity': True,
                                       'markdown_name': 'Duration',
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Specimen_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  'Duration'],
                                       'ux_mode': 'choices'},
                                      {'source': [{'inbound': ['Beta_Cell',
                                                               'Biosample_Specimen_FKey']},
                                                  'RID']},
                                      'Description',
                                      'Collection_Date']}}

visible_foreign_keys = {'*': [{'source': [{'outbound': ['Beta_Cell',
                                                        'Specimen_Protocol_FKey']},
                                          {'inbound': ['Beta_Cell',
                                                       'Protocol_Step_Protocol_FKey']},
                                          'RID']},
                              {'source': [{'inbound': ['Beta_Cell',
                                                       'Biosample_Specimen_FKey']},
                                          'RID']}]}

table_display = {}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'table_display': {},
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'Table of biological speciments from which biosamples will be created.'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'Specimen_RIDkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Protocol'],
                         'Beta_Cell', 'Protocol', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Specimen_Protocol_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['Cell_Line'],
                         'Beta_Cell', 'Cell_Line', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Specimen_Cell_Line_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         comment='Must be a valid reference to a cell line.',
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
