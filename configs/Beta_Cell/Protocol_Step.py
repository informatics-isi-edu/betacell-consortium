import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Protocol_Step'
schema_name = 'Beta_Cell'

column_annotations = {
    'Cellular_Location': {},
    'Duration': {},
    'Start_Time': {}}

column_comment = {
    'Cellular_Location': 'Component of the cell that was extracted.',
    'Duration': 'Length in time in minutes over which this protocol step takes '
    'place',
    'Start_Time': 'Time in minutes from the start of the protocol when this '
    'step should start'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Description', em.builtin_types['markdown'],),
               em.Column.define('Step_Number', em.builtin_types['int4'], nullok=False,),
               em.Column.define('Protocol', em.builtin_types['text'], nullok=False,),
               em.Column.define('Start_Time', em.builtin_types['int4'], comment=column_comment['Start_Time'],),
               em.Column.define('Duration', em.builtin_types['int4'], comment=column_comment['Duration'],),
               em.Column.define('Cellular_Location', em.builtin_types['text'], comment=column_comment['Cellular_Location'],),
               ]

visible_columns = {'*': [{'source': 'RID'},
                         {'source': 'Name'},
                         {'source': [{'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Protocol_FKey']},
                                     'RID']},
                         {'source': 'Step_Number'},
                         {'source': [{'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Protocol_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Protocol_Protocol_Type_FKey']},
                                     'RID']},
                         'Start_Time',
                         'Duration',
                         {'source': [{'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Cellular_Location_Term_FKey']},
                                     'id']},
                         {'aggregate': 'array',
                          'comment': 'Additive used in protocol step',
                          'entity': True,
                          'markdown_name': 'Additive',
                          'source': [{'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                     'RID']},
                         {'aggregate': 'array',
                          'comment': 'Additive concentration used in protocol step',
                          'entity': True,
                          'markdown_name': 'Concentration',
                          'source': [{'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     'Additive_Concentration']},
                         {'source': 'Description'}],
                   'filter': {'and': [{'source': 'RID'},
                                      {'source': 'Name'},
                                      {'source': [{'outbound': ['Beta_Cell',
                                                                'Protocol_Step_Protocol_FKey']},
                                                  'RID']},
                                      {'source': [{'outbound': ['Beta_Cell',
                                                                'Protocol_Step_Protocol_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Protocol_Protocol_Type_FKey']},
                                                  'RID']},
                                      {'source': [{'outbound': ['Beta_Cell, '
                                                                'Protocol_Step_Cellular_Location_Term_FKey']},
                                                  'id']},
                                      {'aggregate': 'array',
                                       'comment': 'Additive used in protocol step',
                                       'entity': True,
                                       'markdown_name': 'Additive',
                                       'source': [{'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                                  'RID']},
                                      {'aggregate': 'array',
                                       'comment': 'Concentration in mM of additive '
                                       'used in protocol step',
                                       'entity': True,
                                       'markdown_name': 'Concentration',
                                       'source': [{'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  'Additive_Concentration'],
                                       'ux_mode': 'choices'},
                                      {'source': ['Duration'], 'ux_mode': 'choices'},
                                      {'entity': False,
                                       'source': 'Step_Number',
                                       'ux_mode': 'choices'},
                                      {'source': 'Description'}]}}

visible_foreign_keys = {'*': [['Beta_Cell',
                               'Protocol_Step_Cellular_Location_Term_FKey'],
                              {'source': [{'inbound': ['Beta_Cell',
                                                       'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                          'RID']}]}

table_display = {
    'row_name': {
        'row_markdown_pattern': '{{#Protocol}}{{$fkeys.Beta_Cell.Protocol_Step_Protocol_FKey.rowName}}{{/Protocol}}{{#Step_Number}} '
        '(Step '
        '{{Step_Number}}){{/Step_Number}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'Defines a single step in a protocol'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['Step_Number', 'Protocol'],
                  constraint_names=[('Beta_Cell', 'Protocol_Step_Key')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'Protocol_Step_RIDkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Cellular_Location'],
                         'vocab', 'cellular_location_terms', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Protocol_Step_Cellular_Location_Term_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         ),
    em.ForeignKey.define(['Protocol'],
                         'Beta_Cell', 'Protocol', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Protocol_Step_Protocol_FKey')],
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
