import deriva.core.ermrest_model as em
from deriva.core import ErmrestCatalog, get_credential
from deriva.core.ermrest_config import tag as chaise_tags
from requests.exceptions import HTTPError

from attrdict import AttrDict


def default_catalog_config(catalog):
    model = catalog.getCatalogModel()
    groups = config.groups

    # Set up default display
    model.annotations['display'] = {'name_style': {'underline_space': True}}

    # modify local representation of catalog ACL config
    model.acls.update({
        "owner": [groups.admin],
        "insert": [groups.curator, groups.writer],
        "update": [groups.curator],
        "delete": [groups.curator],
        "select": [groups.writer, groups.reader],
        "enumerate": ["*"],
    })
    # apply these local config changes to the server
    model.apply(catalog)

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
                    '/attribute/D:=Beta_Cell:Dataset/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID'
                ],
                'dir_pattern': '^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+/tomography)',
                'column_map': {
                    'url': '{URI}',
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


def default_table_config(catalog, schema_name, table_name):
    """
    This function adds the following basic configuration details to an existing table:
    1) Creates a self service modification policy in which creators can update update any row they create.  Optionally,
       an Owner column can be provided, which allows the creater of a row to delegate row ownership to a specific
       individual.
    2) Adds display annotations and foreign key declarations so that system columns RCB, RMB display in a user friendly
       way.
    :param catalog:
    :param schema_name:
    :param table_name:
    :return:
    """

    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    if table.column_definitions['Owner']:
        print('Table missing owner column.')

    # Make table policy be self service, creators can update.
    self_service_policy = {
        "self_service_creator": {
            "types": ["update", "delete"],
            "projection": ["RCB"],
            "projection_type": "acl"
        }
    }

    if table.column_definitions['Owner']:
        self_service_policy['self_service_owner'] = {
            "types": ["update", "delete"],
            "projection": ["Owner"],
            "projection_type": "acl"
        }

    table.acl_bindings.update(self_service_policy)
    model_root.apply(catalog)

    # Set up foreign key to ermrest_client on RCB and Owner.
    for col, display in [('RCB', 'Created By'), ('RMB', 'Modified By'), ('Owner', 'Ownder')]:
        fk_name = '{}_{}_fkey'.format(table_name, col)
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

        # Add a display annotation so that we use the user name on RCB and RMB and Owner
        column_annotation = {
            'tag:isrd.isi.edu,2016:column-display':
                {'*': {
                    'markdown_pattern': '{{{{{{$fkeys.{}.{}.values._display_name}}}}}}'.format(schema_name, fk_name)}},
            'tag:misd.isi.edu,2015:display': {'markdown_name': display}
        }
        table.column_definitions[col].annotations.update(column_annotation)
    table.apply(catalog, schema)

    return


def default_visible_columns(table):
    """
    return a baseline visible columns annotation for all the columns in a table that can be modified to create more
    customized displays.

    """
    pass
