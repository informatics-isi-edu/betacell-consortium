import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args
from deriva.core.ermrest_config import tag as chaise_tags
import deriva.core.ermrest_model as em

groups = {
    'pbcconsortium-reader': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'pbcconsortium-curator': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'pbcconsortium-writer': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'pbcconsortium-admin': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422'
}

display = {'name_style': {'underline_space': True}}

bulk_upload = {
    'asset_mappings': [
        {
            'asset_type': 'table',
            'ext_pattern': '^.*[.](?P<file_ext>json|csv)$',
            'file_pattern': '^((?!/assets/).)*/records/(?P<schema>.+?)/(?P<table>.+?)[.]',
            'default_columns': ['RID', 'RCB', 'RMB', 'RCT', 'RMT']
        },
        {
            'column_map': {
                'md5': '{md5}',
                'url': '{URI}',
                'dataset': '{dataset_rid}',
                'filename': '{file_name}',
                'biosample': '{biosample_rid}',
                'byte_count': '{file_size}'
            },
            'dir_pattern': '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/tomography)',
            'ext_pattern': '.mrc$',
            'file_pattern': '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec',
            'target_table': ['Beta_Cell', 'XRay_tomography_data'],
            'checksum_types': ['md5'],
            'hatrac_options': {
                'versioned_uris': 'True'
            },
            'hatrac_templates': {
                'hatrac_uri': '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'
            },
            'record_query_template': '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}',
            'metadata_query_templates': [
                '/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'
            ],
            'create_record_before_upload': 'False'
        },
        {
            'column_map': {
                'md5': '{md5}',
                'url': '{URI}',
                'dataset': '{dataset_rid}',
                'filename': '{file_name}',
                'biosample': '{biosample_rid}',
                'byte_count': '{file_size}'
            },
            'dir_pattern': '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/proteomics)',
            'ext_pattern': '.csv$',
            'file_pattern': '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec',
            'target_table': ['Beta_Cell', 'XRay_tomography_data'],
            'checksum_types': ['md5'],
            'hatrac_options': {
                'versioned_uris': 'True'
            },
            'hatrac_templates': {
                'hatrac_uri': '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'
            },
            'record_query_template': '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}',
            'metadata_query_templates': [
                '/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'
            ],
            'create_record_before_upload': 'False'
        },
        {
            'asset_type': 'table',
            'ext_pattern': '^.*[.](?P<file_ext>json|csv)$',
            'file_pattern': '^((?!/assets/).)*/records/(?P<schema>WWW?)/(?P<table>Page)[.]',
            'target_table': ['WWW', 'Page'],
            'default_columns': ['RID', 'RCB', 'RMB', 'RCT', 'RMT']
        },
        {
            'column_map': {
                'MD5': '{md5}',
                'URL': '{URI}',
                'Length': '{file_size}',
                'Filename': '{file_name}',
                'Page_RID': '{table_rid}'
            },
            'dir_pattern': '^.*/(?P<schema>WWW)/(?P<table>Page)/(?P<key_column>.*)/',
            'ext_pattern': '^.*[.](?P<file_ext>.*)$',
            'file_pattern': '.*',
            'target_table': ['WWW', 'Page_Asset'],
            'checksum_types': ['md5'],
            'hatrac_options': {
                'versioned_uris': True
            },
            'hatrac_templates': {
                'hatrac_uri': '/hatrac/{schema}/{table}/{md5}.{file_name}'
            },
            'record_query_template': '/entity/{schema}:{table}_Asset/{table}_RID={table_rid}/MD5={md5}/URL={URI_urlencoded}',
            'metadata_query_templates': [
                '/attribute/D:={schema}:{table}/RID={key_column}/table_rid:=D:RID'
            ]
        }
    ],
    'version_update_url': 'https://github.com/informatics-isi-edu/deriva-qt/releases',
    'version_compatibility': [['>=0.4.3', '<1.0.0']]
}

annotations = {
    chaise_tags.display: display,
    chaise_tags.bulk_upload: bulk_upload,
    'tag:isrd.isi.edu,2019:catalog-config': {
        'name': 'pbcconsortium',
        'groups': {
            'admin': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
            'reader': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
            'writer': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
            'curator': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a'
        }
    },
}

acls = {
    'insert': [groups['pbcconsortium-curator'], groups['pbcconsortium-writer']],
    'delete': [groups['pbcconsortium-curator']],
    'enumerate': ['*'],
    'create': [],
    'select': [groups['pbcconsortium-writer'], groups['pbcconsortium-reader']],
    'owner': [groups['pbcconsortium-admin']],
    'write': [],
    'update': [groups['pbcconsortium-curator']]
}


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_catalog(mode, annotations, acls, replace=replace)


if __name__ == "__main__":
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_catalog=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)

