import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'project'
schema_name = 'isa'

column_annotations = {
    'RCB': {}, 'RCT': {}, 'RID': {}, 'RMB': {}, 'RMT': {}, 'name': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '{{{pis}}}: '
                '{{{name}}}'}}}, 'pis': {
                    'tag:misd.isi.edu,2015:display': {
                        'name': 'List of PI Last Names'}}, 'url': {
                            'tag:isrd.isi.edu,2016:column-display': {
                                '*': {
                                    'markdown_pattern': '[{{{url}}}]({{{url}}})'}}}}

column_comment = {
    'RCB': 'System-generated row created by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RID': 'System-generated unique row ID.',
    'RMB': 'System-generated row modified by user provenance.',
    'RMT': 'System-generated row modification timestamp',
    'pis': 'List of Last Names of Principal Investigator separated by /',
    'url': 'url for more information on this project on externalre site'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('id', em.builtin_types['serial4'], nullok=False,),
               em.Column.define('funding', em.builtin_types['text'],),
               em.Column.define('url', em.builtin_types['text'], annotations=column_annotations['url'], comment=column_comment['url'],),
               em.Column.define('name', em.builtin_types['text'], annotations=column_annotations['name'],),
               em.Column.define('abstract', em.builtin_types['markdown'],),
               em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False, comment=column_comment['RID'],),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'], comment=column_comment['RCB'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'], comment=column_comment['RMB'],),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False, comment=column_comment['RCT'],),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False, comment=column_comment['RMT'],),
               em.Column.define('pis', em.builtin_types['text'], annotations=column_annotations['pis'], comment=column_comment['pis'],),
               ]

visible_columns = {'compact': ['name', 'abstract'],
                   'detailed': ['name',
                                'funding',
                                'url',
                                'abstract',
                                'group_membership_url',
                                ['isa', 'project_publication_project_id_fkey']],
                   'entry': ['name',
                             'funding',
                             'url',
                             'abstract',
                             'pis',
                             ['isa', 'project_groups_fkey'],
                             'group_membership_url'],
                   'filter': {'and': [{'entity': True,
                                       'markdown_name': 'Investigator',
                                       'open': True,
                                       'source': [{'inbound': ['isa',
                                                               'project_investigator_project_id_fkey']},
                                                  'username']},
                                      {'entity': False,
                                       'open': False,
                                       'source': 'funding'},
                                      {'entity': True,
                                       'markdown_name': 'Publication',
                                       'open': False,
                                       'source': [{'inbound': ['isa',
                                                               'project_publication_project_id_fkey']},
                                                  'pmid']}]}}

visible_foreign_keys = {'detailed': [['isa', 'project_investigator_project_id_fkey'],
                                     ['isa', 'project_member_project_id_fkey'],
                                     ['isa', 'dataset_project_fkey']]}

table_display = {
    'compact': {
        'row_order': [
            {
                'column': 'pis', 'descending': False}]}, 'row_name': {
                    'row_markdown_pattern': '{{{pis}}}: {{{name}}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = 'domain'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['name'],
                  constraint_names=[('isa', 'project_name_key')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('isa', 'project_RID_key')],
                  ),
    em.Key.define(['id'],
                  constraint_names=[('isa', 'project_pkey')],
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
