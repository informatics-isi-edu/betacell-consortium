import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args
from deriva.core.ermrest_config import tag as chaise_tags
import deriva.core.ermrest_model as em

display = {'name_style': {'underline_space': True}}

bulk_upload = {
    'asset_mappings': [
        {
            'default_columns': ['RID', 'RCB', 'RMB', 'RCT', 'RMT'],
            'ext_pattern': '^.*[.](?P<file_ext>json|csv)$',
            'asset_type': 'table',
            'file_pattern': '^((?!/assets/).)*/records/(?P<schema>.+?)/(?P<table>.+?)[.]'
        },
        {
            'checksum_types': ['md5'],
            'record_query_template': '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}',
            'hatrac_templates': {
                'hatrac_uri': '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'
            },
            'create_record_before_upload': 'False',
            'ext_pattern': '.mrc$',
            'file_pattern': '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec',
            'target_table': ['Beta_Cell', 'XRay_tomography_data'],
            'hatrac_options': {
                'versioned_uris': 'True'
            },
            'metadata_query_templates': [
                '/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'
            ],
            'dir_pattern': '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/tomography)',
            'column_map': {
                'url': '{URI}',
                'dataset': '{dataset_rid}',
                'byte_count': '{file_size}',
                'biosample': '{biosample_rid}',
                'filename': '{file_name}',
                'md5': '{md5}'
            }
        },
        {
            'checksum_types': ['md5'],
            'record_query_template': '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}',
            'hatrac_templates': {
                'hatrac_uri': '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'
            },
            'create_record_before_upload': 'False',
            'ext_pattern': '.csv$',
            'file_pattern': '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec',
            'target_table': ['Beta_Cell', 'XRay_tomography_data'],
            'hatrac_options': {
                'versioned_uris': 'True'
            },
            'metadata_query_templates': [
                '/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'
            ],
            'dir_pattern': '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/proteomics)',
            'column_map': {
                'url': '{URI}',
                'dataset': '{dataset_rid}',
                'byte_count': '{file_size}',
                'biosample': '{biosample_rid}',
                'filename': '{file_name}',
                'md5': '{md5}'
            }
        }
    ],
    'version_update_url': 'https://github.com/informatics-isi-edu/deriva-qt/releases',
    'version_compatibility': [['>=0.4.3', '<1.0.0']]
}

annotations = {chaise_tags.bulk_upload: bulk_upload, chaise_tags.display: display, }

acls = {
    'insert': [
        'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764'
    ],
    'create': [],
    'update': ['https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a'],
    'write': [],
    'enumerate': ['*'],
    'owner': [
        'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
        'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
    ],
    'select': [
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a'
    ],
    'delete': ['https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a']
}


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_catalog(mode, annotations, acls, replace=replace)


if __name__ == "__main__":
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_catalog=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)

