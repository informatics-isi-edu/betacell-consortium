from deriva.core import ErmrestCatalog, get_credential
import deriva.core.ermrest_model as em

schema_name = 'isa'
table_name = 'xray_tomography_data'
column_defs = [
    em.Column.define('dataset', em.builtin_types.text, comment='None'),
    em.Column.define('anatomy', em.builtin_types.text, comment='None'),
    em.Column.define('device', em.builtin_types.text, comment='None'),
    em.Column.define('equipment_model', em.builtin_types.text, comment='None'),
    em.Column.define('description', em.builtin_types.markdown, comment='None'),
    em.Column.define('url', em.builtin_types.text, comment='None' ),
    em.Column.define('filename',em.builtin_types.text, comment='None'),
    em.Column.define('file_type',em.builtin_types.text, comment='None'),
    em.Column.define('byte_count', em.builtin_types.int8, comment='None'),
    em.Column.define('submitted_on', em.builtin_types.timestamptz, comment='None'),
    em.Column.define('md5', em.builtin_types.text, comment='None'),
    em.Column.define('file_id',	em.builtin_types.int4, comment='None'),
    em.Column.define('replicate',em.builtin_types.text, comment='None')
]

key_defs = [
  em.Key.define(
    ["dataset", "RID"], # this is a list to allow for compound keys
    constraint_names=[ ['isa', "xray_tomography_data_dataset_RID_key"] ],
    comment="RID and dataset must be distinct.",
    annotations={},
  ),
    em.Key.define(
        ["url"],  # this is a list to allow for compound keys
        constraint_names=[['isa', "xray_tomography_data_url_key"]],
        comment="Unique URL must be provided.",
        annotations={},
    )
]

fkey_defs = [
    em.ForeignKey.define(
        ["dataset"], # this is a list to allow for compound foreign keys
        "isa", "dataset", ["RID"], # this is a list to allow for compound keys
        constraint_names=[ ['isa', "xray_tomography_dataset_fkey"] ],
        comment="Must be a valid reference to a dataset.",
        on_update='CASCADE', on_delete='RESTRICT',
        acls={}, acl_bindings={},
        annotations={},
    ),
    em.ForeignKey.define(
        ["device"],  # this is a list to allow for compound foreign keys
        "vocab", "image_creation_device_terms", ['dbxref'],  # this is a list to allow for compound keys
        constraint_names=[['isa', "xray_tomography_data_device_fkey"]],
        comment="Must be a valid reference to a device.",
        on_update='CASCADE', on_delete='RESTRICT',
        acls={}, acl_bindings={},
        annotations={},
    ),
    em.ForeignKey.define(
        ["anatomy"],  # this is a list to allow for compound foreign keys
        "vocab", "anatomy_terms", ["dbxref"],  # this is a list to allow for compound keys
        constraint_names=[['isa', "xray_tomography_data_anatomy_fkey"]],
        comment="Must be a valid reference to a anatomy.",
        on_update='CASCADE', on_delete='RESTRICT',
        acls={}, acl_bindings={},
        annotations={},
    ),
    em.ForeignKey.define(
        ["dataset", "replicate"],  # this is a list to allow for compound foreign keys
        "isa", "replicate", ['dataset', 'RID'],  # this is a list to allow for compound keys
        constraint_names=[['isa', "xray_tomography_data_replicate_fkey"]],
        comment="Must be a valid reference to a dataset.",
        on_update='CASCADE', on_delete='RESTRICT',
        acls={}, acl_bindings={},
        annotations={},
    ),
    em.ForeignKey.define(
        ["equipment_model"],  # this is a list to allow for compound foreign keys
        "vocab", "instrument_terms", ["dbxref"],  # this is a list to allow for compound keys
        constraint_names=[['isa', "xray_tomography_data_equiptment_model_fkey"]],
        comment="Must be a valid reference to a dataset.",
        on_update='CASCADE', on_delete='RESTRICT',
        acls={}, acl_bindings={},
        annotations={},
    ),
    em.ForeignKey.define(
        ["file_type"],  # this is a list to allow for compound foreign keys
        "vocab", "file_format_terms", ["dbxref"],  # this is a list to allow for compound keys
        constraint_names=[['isa', "xray_tomography_data_file_type_fkey"]],
        comment="Must be a valid reference to a dataset.",
        on_update='CASCADE', on_delete='RESTRICT',
        acls={}, acl_bindings={},
        annotations={},
    )
]

table_def = em.Table.define(
  "xray_tomography_data",
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs[0:5],
  comment="Table to hold X-Ray Tomography MRC files.",
  acls={},
  acl_bindings={},
  annotations={},
  provide_system=True,
)

visible_foreign_keys = {
    'detailed': [['isa', 'thumbnail_thumbnail_of_fkey'],
    ['isa', 'mesh_data_derived_from_fkey']],
    'entry': [['isa', 'thumbnail_thumbnail_of_fkey'],
    ['isa', 'mesh_data_derived_from_fkey']]
}

visible_columns = {
    'filter': {'and': [{'source': 'filename',
    'open': False,
    'markdown_name': 'File Name',
    'entity': True},
   {'source': [{'outbound': ['isa', 'xray_tomography_data_replicate_fkey']}, 'RID'],
    'open': True,
    'markdown_name': 'Replicate',
    'entity': True},
   {'source': [{'outbound': ['isa', 'xray_tomography_data_anatomy_fkey']}, 'id'],
    'open': True,
    'markdown_name': 'Anatomy',
    'entity': True},
   {'source': [{'outbound': ['isa', 'xray_tomography_data_device_fkey']}, 'id'],
    'open': True,
    'markdown_name': 'Imaging Device',
    'entity': True},
   {'source': [{'outbound': ['isa', 'xray_tomography_data_equipment_model_fkey']},
     'id'],
    'open': True,
    'markdown_name': 'Equipment Model',
    'entity': True},
   {'source': [{'outbound': ['isa', 'xray_tomography_data_file_type_fkey']}, 'id'],
    'open': True,
    'markdown_name': 'File Type',
    'entity': True},
   {'source': 'submitted_on',
    'open': False,
    'markdown_name': 'Submitted On',
    'entity': True}]},
 'entry': ['RID',
  ['isa', 'xray_tomography_data_replicate_fkey'],
  ['isa', 'xray_tomography_data_anatomy_fkey'],
  ['isa', 'xray_tomography_data_device_fkey'],
  ['isa', 'xray_tomography_data_equipment_model_fkey'],
  'description',
  'url',
  'filename',
  ['isa', 'xray_tomography_data_file_type_fkey'],
  'byte_count',
  'md5',
  'submitted_on'],
 'detailed': [['isa', 'xray_tomography_data_pkey'],
  ['isa', 'xray_tomography_data_dataset_fkey'],
  ['isa', 'xray_tomography_data_replicate_fkey'],
  ['isa', 'xray_tomography_data_device_fkey'],
  'filename',
  ['isa', 'xray_tomography_data_file_type_fkey'],
  'byte_count',
  'md5',
  'submitted_on'],
 'compact': [['isa', 'xray_tomography_data_pkey'],
  'replicate_fkey',
  'url',
  'file_type',
  'byte_count',
  'md5',
  'submitted_on']}

server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas['isa']
tomography_table = schema.create_table(catalog, table_def)

for k,v in visible_columns.items():
    tomography_table.visible_columns[k] = v

for k,v in visible_foreign_keys.items():
    tomography_table.visible_foreign_keys[k] = v

tomography_table.apply(catalog)

#schema.tables['xray_tomography_data'].delete(catalog, schema=schema)