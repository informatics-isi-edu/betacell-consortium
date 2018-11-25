
import deriva.core.ermrest_model as em
from deriva.core import ErmrestCatalog, get_credential
from requests.exceptions import HTTPError


def setup_table(server, catalog_id, schema_name, table_name):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    # Make table policy be self service, creators can update.
    self_service_policy = {
        "self_service_creator": {
            "types": ["update", "delete"],
            "projection": ["RCB"],
            "projection_type": "acl"
        },
        "self_service_owner": {
            "types": ["update", "delete"],
            "projection": ["Owner"],
            "projection_type": "acl"
        }
    }
    table.acl_bindings.clear()
    table.acl_bindings.update(self_service_policy)
    model_root.apply(catalog)

    # Set up foreign key to ermrest_client on RCB and Owner.
    for col in ['RCB', 'Owner']:
        fk_name = '{}_{}_Fkey'.format(table_name, col)
        fk = em.ForeignKey.define(
            [col],
            'public',
            'ermrest_client',
            ['id'],
            constraint_names=[(schema_name, fk_name)],
        )

        try:
            # Delete old fkey if there is one laying around....
            f = table.foreign_keys[(schema_name, fk_name)]
            f.delete(catalog, table)
        except KeyError:
            pass
        table.create_fkey(catalog, fk)

    # Add a display annotation so that we use the user name on RCB
    fk_name
    column_annotation = {
        'tag:isrd.isi.edu,2016:column-display' :
            {'*': {'markdown_pattern': '{{{{{{$fkeys.{}.{}.values._display_name}}}}}}'.format(schema_name,fk_name)}},
        'tag:misd.isi.edu,2015:display' : {'markdown_name': 'Creator'}
    }
    table.column_definitions['RCB'].annotations.clear()
    table.column_definitions['RCB'].annotations.update(column_annotation)

    column_annotation = {
        'tag:isrd.isi.edu,2016:column-display' :
            {'*': {'markdown_pattern': '{{{{{{$fkeys.{}.{}.values._display_name}}}}}}'.format(schema_name,fk_name)}},
    }
    table.column_definitions['Owner'].annotations.clear()
    table.column_definitions['Owner'].annotations.update(column_annotation)


    model_root.apply(catalog)
    return

annotations = {chaise_tags.bulk_upload:{'asset_mappings': [{'default_columns': ['RID', 'RCB', 'RMB', 'RCT', 'RMT'], 'ext_pattern': '^.*[.](?P<file_ext>json|csv)$', 'asset_type': 'table', 'file_pattern': '^((?!/assets/).)*/records/(?P<schema>.+?)/(?P<table>.+?)[.]'}, {'checksum_types': ['md5'], 'record_query_template': '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}', 'hatrac_templates': {'hatrac_uri': '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'}, 'create_record_before_upload': 'False', 'ext_pattern': '.mrc$', 'file_pattern': '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec', 'target_table': ['Beta_Cell', 'XRay_tomography_data'], 'hatrac_options': {'versioned_uris': 'True'}, 'metadata_query_templates': ['/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'], 'dir_pattern': '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/tomography)', 'column_map': {'url': '{URI}', 'dataset': '{dataset_rid}', 'byte_count': '{file_size}', 'biosample': '{biosample_rid}', 'filename': '{file_name}', 'md5': '{md5}'}}, {'checksum_types': ['md5'], 'record_query_template': '/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/md5={md5}/url={URI_urlencoded}', 'hatrac_templates': {'hatrac_uri': '/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}'}, 'create_record_before_upload': 'False', 'ext_pattern': '.csv$', 'file_pattern': '.*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec', 'target_table': ['Beta_Cell', 'XRay_tomography_data'], 'hatrac_options': {'versioned_uris': 'True'}, 'metadata_query_templates': ['/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'], 'dir_pattern': '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/proteomics)', 'column_map': {'url': '{URI}', 'dataset': '{dataset_rid}', 'byte_count': '{file_size}', 'biosample': '{biosample_rid}', 'filename': '{file_name}', 'md5': '{md5}'}}], 'version_update_url': 'https://github.com/informatics-isi-edu/deriva-qt/releases', 'version_compatibility': [['>=0.4.3', '<1.0.0']]}chaise_tags.display:{'name_style': {'underline_space': True}}}
