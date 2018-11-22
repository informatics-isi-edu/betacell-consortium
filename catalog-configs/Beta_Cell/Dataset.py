import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'Dataset'
schema_name = 'Beta_Cell'

groups = AttrDict({
    'admins':
    'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'modelers':
    'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
    'curators':
    'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'writers':
    'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'readers':
    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'isrd':
    'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
})

tags = AttrDict({
    'immutable':
    'tag:isrd.isi.edu,2016:immutable',
    'display':
    'tag:misd.isi.edu,2015:display',
    'visible_columns':
    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys':
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':
    'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':
    'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives':
    'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':
    'tag:isrd.isi.edu,2016:column-display',
    'asset':
    'tag:isrd.isi.edu,2017:asset',
    'export':
    'tag:isrd.isi.edu,2016:export',
    'generated':
    'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':
    'tag:isrd.isi.edu,2017:bulk-upload'
})

column_annotations = {
    'RCB': {
        tags.display: {
            '*': {
                'markdown_name': 'Owner'
            }
        },
        tags.column_display: {
            '*': {
                'markdown_pattern':
                '{{{$fkeys.Beta_Cell.Dataset_RCB_Fkey.values._display_name}}}'
            }
        }
    }
}

column_comment = {}

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
        annotations=column_annotations['RCB'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
    ),
    em.Column.define(
        'Title',
        em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define(
        'Project',
        em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
    ),
]

groups = AttrDict({
    'admins':
    'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'modelers':
    'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
    'curators':
    'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'writers':
    'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'readers':
    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'isrd':
    'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
})

tags = AttrDict({
    'immutable':
    'tag:isrd.isi.edu,2016:immutable',
    'display':
    'tag:misd.isi.edu,2015:display',
    'visible_columns':
    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys':
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':
    'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':
    'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives':
    'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':
    'tag:isrd.isi.edu,2016:column-display',
    'asset':
    'tag:isrd.isi.edu,2017:asset',
    'export':
    'tag:isrd.isi.edu,2016:export',
    'generated':
    'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':
    'tag:isrd.isi.edu,2017:bulk-upload'
})

visible_columns = {
    'filter': {
        'and':
        [{
            'source': ['RID']
        },
         {
             'source': [{
                 'inbound':
                 ['Beta_Cell', 'Dataset_Experiment_Type_Dataset_id_FKey']
             },
                        {
                            'outbound': [
                                'Beta_Cell',
                                'Dataset_Experiment_Type_Experiment_type_FKey'
                            ]
                        }, 'dbxref'],
             'open':
             False,
             'entity':
             True
         },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Dataset_project_fkey']
             }, {
                 'inbound': ['isa', 'project_investigator_project_id_fkey']
             }, {
                 'outbound': ['isa', 'project_investigator_person_fkey']
             }, 'RID'],
             'open':
             False,
             'markdown_name':
             'Project Investigator',
             'entity':
             True
         }, {
             'source': 'Title',
             'open': False,
             'entity': False
         },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Dataset_project_fkey']
             }, 'id'],
             'open':
             False,
             'entity':
             True
         }, {
             'source': 'release_date',
             'open': False,
             'entity': False
         },
         {
             'source': [{
                 'outbound': ['Beta_Cell', 'Dataset_status_fkey']
             }, 'name'],
             'open':
             False,
             'entity':
             True
         }]
    },
    'entry': ['Title', ['Beta_Cell', 'Dataset_Project_FKey'], 'Description'],
    'detailed': [['Beta_Cell', 'Dataset_RID_key'], 'RCB', 'Description',
                 ['Beta_Cell', 'Dataset_project_fkey'],
                 ['Beta_Cell', 'Dataset_Status_FKey'], 'funding',
                 'release_date',
                 ['Beta_Cell', 'Dataset__Experiment_type_Dataset__id_fkey'],
                 ['Beta_Cell', 'Dataset_data_type_dataset_id_fkey'],
                 ['Beta_Cell', 'Dataset_anatomy_Dataset_id_fkey']],
    'compact': [['Beta_Cell', 'Dataset_RID_Key'], 'RCB', 'Title',
                ['Beta_Cell', 'Dataset_Project_FKey'], 'Description']
}

visible_foreign_keys = {
    '*': [['viz', 'model_Dataset_fkey'],
          ['Beta_Cell', 'Experiment_Dataset_FKey'],
          ['Beta_Cell', 'Biosample_Dataset_FKey'],
          ['Beta_Cell', 'File_Dataset_FKey']]
}

table_display = {
    '*': {
        'row_order': [{
            'column': 'accession',
            'descending': True
        }]
    },
    'row_name': {
        'row_markdown_pattern': '{{Title}}'
    }
}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = None

table_acls = {}

table_acl_bindings = {
    'self_service': {
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['RID'],
        constraint_names=[('Beta_Cell', 'Dataset_RID_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client',
        ['id'],
        constraint_names=[('Beta_Cell', 'Dataset_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Project'],
        'isa',
        'project',
        ['id'],
        constraint_names=[('Beta_Cell', 'Dataset_Project_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
]

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True)


def main(skip_args=False, mode='annotations', replace=False, server='pbcconsortium.isrd.isi.edu', catalog_id=1):
    
    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_table=True)
    update_catalog.update_table(mode, replace, server, catalog_id, schema_name, table_name, 
                                table_def, column_defs, key_defs, fkey_defs,
                                table_annotations, table_acls, table_acl_bindings, table_comment,
                                column_annotations, column_acls, column_acl_bindings, column_comment)


if __name__ == "__main__":
    main()
