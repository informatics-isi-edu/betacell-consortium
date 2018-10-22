import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_name = 'mesh_data'
schema_name = 'isa'

column_annotations = {
    'RCB': {},
    'RCT': {},
    'RID': {},
    'RMB': {},
    'RMT': {},
    'filename': {
        'tag:isrd.isi.edu,2016:column-display': {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'},
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}},
    'url': {
        'tag:isrd.isi.edu,2017:asset': {
            'byte_count_column': 'byte_count',
            'filename_column': 'filename',
            'md5': 'md5',
            'url_pattern': '/hatrac/commons/previews/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}'}}}

column_comment = {'RCB': 'System-generated row created by user provenance.',
                  'RCT': 'System-generated row creation timestamp.',
                  'RID': 'System-generated unique row ID.',
                  'RMB': 'System-generated row modified by user provenance.',
                  'RMT': 'System-generated row modification timestamp'}

column_acls = {}

column_acl_bindings = {}

column_defs = [em.Column.define('RID', em.builtin_types['ermrest_rid'], nullok=False, comment=column_comment['RID'],),
               em.Column.define('url', em.builtin_types['text'], nullok=False, annotations=column_annotations['url'],),
               em.Column.define('filename', em.builtin_types['text'], nullok=False, annotations=column_annotations['filename'],),
               em.Column.define('byte_count', em.builtin_types['int8'], nullok=False,),
               em.Column.define('md5', em.builtin_types['text'], nullok=False,),
               em.Column.define('dataset', em.builtin_types['text'], nullok=False,),
               em.Column.define('derived_from', em.builtin_types['text'],),
               em.Column.define('anatomy', em.builtin_types['text'],),
               em.Column.define('label', em.builtin_types['text'],),
               em.Column.define('description', em.builtin_types['markdown'],),
               em.Column.define('RCB', em.builtin_types['ermrest_rcb'], comment=column_comment['RCB'],),
               em.Column.define('RMB', em.builtin_types['ermrest_rmb'], comment=column_comment['RMB'],),
               em.Column.define('RCT', em.builtin_types['ermrest_rct'], nullok=False, comment=column_comment['RCT'],),
               em.Column.define('RMT', em.builtin_types['ermrest_rmt'], nullok=False, comment=column_comment['RMT'],),
               em.Column.define('biosample', em.builtin_types['text'],),
               ]

visible_columns = {'compact': [['isa', 'mesh_data_pkey'],
                               'biosample',
                               ['isa', 'mesh_data_derived_from_fkey'],
                               'url',
                               'byte_count',
                               'md5'],
                   'detailed': [['isa', 'mesh_data_pkey'],
                                ['isa', 'mesh_data_dataset_fkey'],
                                ['isa', 'mesh_data_biosample_fkey'],
                                ['isa', 'mesh_data_derived_from_fkey'],
                                'filename',
                                'byte_count',
                                'md5',
                                ['isa', 'mesh_data_anatomy_fkey'],
                                'label',
                                'description'],
                   'entry': ['RID',
                             ['isa', 'mesh_data_biosample_fkey'],
                             ['isa', 'mesh_data_derived_from_fkey'],
                             'url',
                             'filename',
                             'byte_count',
                             'md5',
                             ['isa', 'mesh_data_anatomy_fkey'],
                             'label',
                             'description'],
                   'filter': {'and': [{'entity': True,
                                       'markdown_name': 'File Name',
                                       'open': False,
                                       'source': 'filename'},
                                      {'entity': True,
                                       'markdown_name': 'Dataset',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'mesh_data_dataset_fkey']},
                                                  'RID']},
                                      {'entity': True,
                                       'markdown_name': 'Biosample',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'mesh_data_biosample_fkey']},
                                                  'RID']},
                                      {'entity': True,
                                       'markdown_name': 'Derived From File',
                                       'open': True,
                                       'source': [{'outbound': ['isa',
                                                                'mesh_data_derived_from_fkey']},
                                                  'RID']}]}}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'table_display': {
        'row_name': {
            'row_markdown_pattern': '{{{filename}}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'],
                  constraint_names=[('isa', 'mesh_data_pkey')],
                  ),
    em.Key.define(['url'],
                  constraint_names=[('isa', 'mesh_data_url_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(['dataset'],
                         'Beta_Cell', 'Dataset', ['RID'],
                         constraint_names=[('isa', 'mesh_data_dataset_fkey')],
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['biosample'],
                         'Beta_Cell', 'Biosample', ['RID'],
                         constraint_names=[
                             ('isa', 'mesh_data_biosample_fkey')],
                         on_update='CASCADE',
                         on_delete='RESTRICT',
                         ),
    em.ForeignKey.define(['derived_from'],
                         'Beta_Cell', 'XRay_Tomography_Data', ['RID'],
                         constraint_names=[
                             ('isa', 'mesh_data_derived_from_fkey')],
                         on_update='CASCADE',
                         on_delete='RESTRICT',
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
