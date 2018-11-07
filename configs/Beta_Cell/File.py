import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'File'
schema_name = 'Beta_Cell'

column_annotations = {
    'Filename': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    'URL': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'},
            'detailed': {
                'markdown_pattern': '[**{{Filename}}**]({{{URL}}})'}},
        'tag:isrd.isi.edu,2017:asset': {
            'byte_count_column': 'byte_count',
            'filename_column': 'filename',
            'md5': 'md5',
            'url_pattern': '/hatrac/commons/data/{{{Dataset}}}/{{#encode}}{{{Filename}}}{{/encode}}'}}}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False,),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False,),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False,),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'],),
               em.Column.define('URL', em.builtin_types['text'], annotations=column_annotations['URL'],),
               em.Column.define('Filename', em.builtin_types['text'], nullok=False, annotations=column_annotations['Filename'],),
               em.Column.define('Description', em.builtin_types['markdown'],),
               em.Column.define('byte_count', em.builtin_types['int8'],),
               em.Column.define('Submitted_On', em.builtin_types['timestamptz'],),
               em.Column.define('md5', em.builtin_types['text'],),
               em.Column.define('Dataset', em.builtin_types['text'], nullok=False,),
               ]

display = {'name': 'Supplementary Files'}

visible_columns = {'compact': [['isa', 'file_RID_key'],
                               'url',
                               'byte_count',
                               'md5',
                               'description'],
                   'detailed': ['filename',
                                'byte_count',
                                'md5',
                                ['isa', 'file_thumbnail_fkey'],
                                ['isa', 'file_dataset_fkey'],
                                'submitted_on',
                                'description'],
                   'entry': ['url',
                             'byte_count',
                             'md5',
                             ['isa', 'file_thumbnail_fkey'],
                             ['isa', 'file_dataset_fkey'],
                             'submitted_on',
                             'description'],
                   'filter': {'and': [{'entity': True,
                                       'markdown_name': 'Dataset',
                                       'open': False,
                                       'source': [{'outbound': ['isa',
                                                                'file_dataset_fkey']},
                                                  'accession']}]}}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_alternatives = {'compact': [
    'isa', 'file_compact'], 'compact/brief': ['isa', 'file_compact']}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:misd.isi.edu,2015:display': display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
    'tag:isrd.isi.edu,2016:table-alternatives': table_alternatives,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['URL'],
                  constraint_names=[('Beta_Cell', 'File_url_key')],
                  ),
    em.Key.define(['RID'],
                  constraint_names=[('Beta_Cell', 'File_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['Dataset'],
                         'Beta_Cell', 'Dataset', ['RID'],
                         constraint_names=[('Beta_Cell', 'File_Dataset_FKey')],
                         acls={'insert': ['*'], 'update': ['*']},
                         on_update='CASCADE',
                         on_delete='SET NULL',
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
