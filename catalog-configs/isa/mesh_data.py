import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_name = 'mesh_data'
schema_name = 'isa'

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
    'RID': {},
    'url': {
        tags.asset: {
            'filename_column':
            'filename',
            'byte_count_column':
            'byte_count',
            'url_pattern':
            '/hatrac/commons/previews/{{{_dataset}}}/{{{_biosample}}}/{{{filename}}}',
            'md5':
            'md5'
        }
    },
    'filename': {
        tags.column_display: {
            'compact': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            },
            'detailed': {
                'markdown_pattern': '[**{{filename}}**]({{{url}}})'
            }
        }
    },
    'RCB': {},
    'RMB': {},
    'RCT': {},
    'RMT': {}
}

column_comment = {
    'RID': 'System-generated unique row ID.',
    'RCB': 'System-generated row created by user provenance.',
    'RMB': 'System-generated row modified by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RMT': 'System-generated row modification timestamp'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
        comment=column_comment['RID'],
    ),
    em.Column.define(
        'url',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['url'],
    ),
    em.Column.define(
        'filename',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['filename'],
    ),
    em.Column.define(
        'byte_count',
        em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define(
        'md5',
        em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define(
        'dataset',
        em.builtin_types['text'],
        nullok=False,
    ),
    em.Column.define(
        'derived_from',
        em.builtin_types['text'],
    ),
    em.Column.define(
        'anatomy',
        em.builtin_types['text'],
    ),
    em.Column.define(
        'label',
        em.builtin_types['text'],
    ),
    em.Column.define(
        'description',
        em.builtin_types['markdown'],
    ),
    em.Column.define(
        'RCB',
        em.builtin_types['ermrest_rcb'],
        comment=column_comment['RCB'],
    ),
    em.Column.define(
        'RMB',
        em.builtin_types['ermrest_rmb'],
        comment=column_comment['RMB'],
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
        comment=column_comment['RCT'],
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
        comment=column_comment['RMT'],
    ),
    em.Column.define(
        'biosample',
        em.builtin_types['text'],
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
        'and': [{
            'source': 'filename',
            'open': False,
            'markdown_name': 'File Name',
            'entity': True
        },
                {
                    'source': [{
                        'outbound': ['isa', 'mesh_data_dataset_fkey']
                    }, 'RID'],
                    'open':
                    True,
                    'markdown_name':
                    'Dataset',
                    'entity':
                    True
                },
                {
                    'source': [{
                        'outbound': ['isa', 'mesh_data_biosample_fkey']
                    }, 'RID'],
                    'open':
                    True,
                    'markdown_name':
                    'Biosample',
                    'entity':
                    True
                },
                {
                    'source': [{
                        'outbound': ['isa', 'mesh_data_derived_from_fkey']
                    }, 'RID'],
                    'open':
                    True,
                    'markdown_name':
                    'Derived From File',
                    'entity':
                    True
                }]
    },
    'entry': [
        'RID', ['isa', 'mesh_data_biosample_fkey'],
        ['isa', 'mesh_data_derived_from_fkey'],
        'url', 'filename', 'byte_count', 'md5',
        ['isa', 'mesh_data_anatomy_fkey'], 'label', 'description'
    ],
    'detailed': [['isa', 'mesh_data_pkey'], ['isa', 'mesh_data_dataset_fkey'],
                 ['isa', 'mesh_data_biosample_fkey'],
                 ['isa', 'mesh_data_derived_from_fkey'],
                 'filename', 'byte_count', 'md5',
                 ['isa', 'mesh_data_anatomy_fkey'], 'label', 'description'],
    'compact': [['isa', 'mesh_data_pkey'], 'biosample',
                ['isa', 'mesh_data_derived_from_fkey'], 'url', 'byte_count',
                'md5']
}

visible_foreign_keys = {}

table_display = {'row_name': {'row_markdown_pattern': '{{{filename}}}'}}

table_annotations = {
    'tag:isrd.isi.edu,2016:table-display': table_display,
    'tag:isrd.isi.edu,2016:visible-foreign-keys': visible_foreign_keys,
    'table_display': {
        'row_name': {
            'row_markdown_pattern': '{{{filename}}}'
        }
    },
    'tag:isrd.isi.edu,2016:visible-columns': visible_columns,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['RID'],
        constraint_names=[('isa', 'mesh_data_pkey')],
    ),
    em.Key.define(
        ['url'],
        constraint_names=[('isa', 'mesh_data_url_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['biosample'],
        'Beta_Cell',
        'Biosample',
        ['RID'],
        constraint_names=[('isa', 'mesh_data_biosample_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['dataset'],
        'Beta_Cell',
        'Dataset',
        ['RID'],
        constraint_names=[('isa', 'mesh_data_dataset_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['derived_from'],
        'Beta_Cell',
        'XRay_Tomography_Data',
        ['RID'],
        constraint_names=[('isa', 'mesh_data_derived_from_fkey')],
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
