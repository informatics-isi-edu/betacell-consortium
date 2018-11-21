import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Dataset'
schema_name = 'Beta_Cell'

column_annotations = {}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('Title', em.builtin_types['text'], nullok=False,),
               em.Column.define('Project', em.builtin_types['int8'], nullok=False,),
               em.Column.define('Description', em.builtin_types['markdown'],),
               ]

visible_columns = {'compact': [['Beta_Cell', 'Dataset_RID_Key'],
                               {'source': [{'outbound': ['Beta_Cell',
                                                         'Dataset_RCB_FKey']},
                                           'display_name']},
                               'Title',
                               ['Beta_Cell', 'Dataset_Project_FKey'],
                               'Description'],
                   'detailed': [['Beta_Cell', 'Dataset_RID_key'],
                                'Description',
                                ['Beta_Cell', 'Dataset_project_fkey'],
                                ['Beta_Cell', 'Dataset_Status_FKey'],
                                'funding',
                                'release_date',
                                ['Beta_Cell', 'Dataset__Experiment_type_Dataset__id_fkey'],
                                ['Beta_Cell', 'Dataset_data_type_dataset_id_fkey'],
                                ['Beta_Cell', 'Dataset_anatomy_Dataset_id_fkey']],
                   'entry': ['Title', ['Beta_Cell', 'Dataset_Project_FKey'], 'Description'],
                   'filter': {'and': [{'source': ['RID']},
                                      {'entity': True,
                                       'open': False,
                                       'source': [{'inbound': ['Beta_Cell',
                                                               'Dataset_Experiment_Type_Dataset_id_FKey']},
                                                  {'outbound': ['Beta_Cell',
                                                                'Dataset_Experiment_Type_Experiment_type_FKey']},
                                                  'dbxref']},
                                      {'entity': True,
                                       'markdown_name': 'Project Investigator',
                                       'open': False,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Dataset_project_fkey']},
                                                  {'inbound': ['isa',
                                                               'project_investigator_project_id_fkey']},
                                                  {'outbound': ['isa',
                                                                'project_investigator_person_fkey']},
                                                  'RID']},
                                      {'entity': False,
                                       'open': False,
                                       'source': 'Title'},
                                      {'entity': True,
                                       'open': False,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Dataset_project_fkey']},
                                                  'id']},
                                      {'entity': False,
                                       'open': False,
                                       'source': 'release_date'},
                                      {'entity': True,
                                       'open': False,
                                       'source': [{'outbound': ['Beta_Cell',
                                                                'Dataset_status_fkey']},
                                                  'name']}]}}

visible_foreign_keys = {'*': [['viz', 'model_Dataset_fkey'],
                              ['Beta_Cell', 'Experiment_Dataset_FKey'],
                              ['Beta_Cell', 'Biosample_Dataset_FKey'],
                              ['Beta_Cell', 'File_Dataset_FKey']]}

table_display = {'*': {'row_order': [{'column': 'accession',
                                      'descending': True}]},
                 'row_name': {'row_markdown_pattern': '{{Title}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'Dataset_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Project'],
                         'isa', 'project', ['id'],
                         constraint_names=[
                             ('Beta_Cell', 'Dataset_Project_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['RCB'],
                         'public', 'ermrest_client', ['id'],
                         constraint_names=[('Beta_Cell', 'Dataset_RCB_FKey')],
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


def main(skip_args=False, mode='annotations', replace=False, server='pbcconsortium.isrd.isi.edu', catalog_id=1):
    
    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
