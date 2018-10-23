import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'Protocol'
schema_name = 'Beta_Cell'

column_annotations = {'Description': {}, 'Type': {}}

column_comment = {'Description': 'A description of the protocol.',
                  'Type': 'The type of object for which this protocol is used.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Description', em.builtin_types['markdown'], comment=column_comment['Description'],),
               em.Column.define('Type', em.builtin_types['text'], nullok=False, comment=column_comment['Type'],),
               ]

visible_columns = {'*': ['RID',
                         ['Beta_Cell', 'Protocol_Protocol_Type_FKey'],
                         {'aggregate': 'array',
                             'comment': 'Additive used in protocol step',
                             'entity': True,
                             'markdown_name': 'Additive',
                          'source': [{'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     {'outbound': ['Beta_Cell',
                                                   'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                     'RID']},
                         {'aggregate': 'array',
                          'comment': 'Additive used in protocol step',
                          'entity': True,
                          'markdown_name': 'Concentration',
                          'source': [{'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Protocol_FKey']},
                                     {'inbound': ['Beta_Cell',
                                                  'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                     'Additive_Concentration']},
                         {'aggregate': 'array',
                             'source': [{'inbound': ['Beta_Cell',
                                                     'Protocol_Step_Protocol_FKey']},
                                        'Duration'],
                          'ux_mode': 'choices'},
                         'Description'],
                   'filter': {'and': [{'source': 'RID'},
                                      {'source': [{'outbound': ['Beta_Cell',
                                                                'Protocol_Protocol_Type_FKey']},
                                                  'RID']},
                                      {'aggregate': 'array',
                                       'comment': 'Additive used in protocol step',
                                       'entity': True,
                                       'markdown_name': 'Additive',
                                       'source': [{'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Protocol_Step_Additive_Term_Additive_Term_FKey']},
                                                  'RID']},
                                      {'aggregate': 'array',
                                       'comment': 'Additive used in protocol step',
                                       'entity': True,
                                       'markdown_name': 'Concentration',
                                       'source': [{'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  {'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Additive_Term_Protocol_Step_FKey']},
                                                  'Additive_Concentration'],
                                       'ux_mode': 'choices'},
                                      {'aggregate': 'array',
                                       'markdown_name': 'Duration',
                                       'source': [{'inbound': ['Beta_Cell',
                                                               'Protocol_Step_Protocol_FKey']},
                                                  'Duration'],
                                       'ux_mode': 'choices'},
                                      'Description']}}

visible_foreign_keys = {'*': [['Beta_Cell', 'Protocol_Step_Protocol_FKey'],
                              ['Beta_Cell', 'Experiment_Protocol_FKey'],
                              ['Beta_Cell', 'Biosample_Protocol_FKey'],
                              ['Beta_Cell', 'Specimen_Protocol_FKey'],
                              ['Beta_Cell', 'Cell_Line_Protocol_FKey']]}

table_display = {
    'row_name': {
        'row_markdown_pattern': '{{#RID}}Protocol:{{Description}}{{/RID}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'Table containing names of Beta Cell protocols'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'Protocol_RIDkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Type'],
                         'Beta_Cell', 'Protocol_Type', ['RID'],
                         constraint_names=[
                             ('Beta_Cell', 'Protocol_Protocol_Type_FKey')],
                         comment='Must be a protocol type.',
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
    update_catalog.update_table(server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
