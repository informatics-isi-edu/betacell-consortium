import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.manage import update_catalog
import deriva.core.ermrest_model as em

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

display = {'name_style': {'underline_space': True}}

bulk_upload = {
    'asset_mappings':
    [{
        'default_columns': ['RID', 'RCB', 'RMB', 'RCT', 'RMT'],
        'ext_pattern':
        '^.*[.](?P<file_ext>json|csv)$',
        'asset_type':
        'table',
        'file_pattern':
        '^((?!/assets/).)*/records/(?P<schema>.+?)/(?P<table>.+?)[.]'
    },
     {
         'checksum_types': ['md5'],
         'record_query_template':
         '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}',
         'hatrac_templates': {
             'hatrac_uri':
             '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'
         },
         'create_record_before_upload':
         'False',
         'ext_pattern':
         '.mrc$',
         'file_pattern':
         '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec',
         'target_table': ['Beta_Cell', 'XRay_tomography_data'],
         'hatrac_options': {
             'versioned_uris': 'True'
         },
         'metadata_query_templates': [
             '/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'
         ],
         'dir_pattern':
         '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/tomography)',
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
         'record_query_template':
         '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}',
         'hatrac_templates': {
             'hatrac_uri':
             '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'
         },
         'create_record_before_upload':
         'False',
         'ext_pattern':
         '.csv$',
         'file_pattern':
         '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec',
         'target_table': ['Beta_Cell', 'XRay_tomography_data'],
         'hatrac_options': {
             'versioned_uris': 'True'
         },
         'metadata_query_templates': [
             '/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'
         ],
         'dir_pattern':
         '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/proteomics)',
         'column_map': {
             'url': '{URI}',
             'dataset': '{dataset_rid}',
             'byte_count': '{file_size}',
             'biosample': '{biosample_rid}',
             'filename': '{file_name}',
             'md5': '{md5}'
         }
     }],
    'version_update_url':
    'https://github.com/informatics-isi-edu/deriva-qt/releases',
    'version_compatibility': [['>=0.4.3', '<1.0.0']]
}

annotations = {
    'tag:isrd.isi.edu,2017:bulk-upload': bulk_upload,
    'tag:misd.isi.edu,2015:display': display,
}

acls = {
    'insert': [groups.curators, groups.writers],
    'create': [],
    'update': [groups.curators],
    'write': [],
    'enumerate': ['*'],
    'owner': [groups.admins, groups.isrd],
    'select': [groups.writers, groups.readers],
    'delete': [groups.curators]
}




def main():
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id, is_catalog=True)
    update_catalog.update_catalog(mode, replace, server, catalog_id, annotations, acls)
    

if __name__ == "__main__":
    main()
