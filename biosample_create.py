from deriva.core import ErmrestCatalog, get_credential
import deriva.core.ermrest_model as em



column_names = ['RID',
 'dataset',
 'local_identifier',
 'summary',
 'species',
 'specimen',
 'strain',
 'anatomy',
 'gender',
 'collection_date',
 '_keywords',
'cell_line'
 'RCB',
 'RMB',
 'RCT',
 'RMT',
 'capillary_number',
 'sample_position']



cell_line_column_def = em.Column.define(
    "cell_line", em.builtin_types.text, nullok=True,
    comment="Cell line used for the biosample.",
)

specimen_column_def = em.Column.define(
    "specimen", em.builtin_types.text, nullok=True,
    comment="Biological material used for the biosample.",
)

specimen_type_column_def = em.Column.define(
    'specimen_type', em.builtin_types.text, nullok=True,
    comment='Method by which specimen is prepared.'
)

cell_line_fk = em.ForeignKey.define(
    ["cell_line"],  # this is a list to allow for compound foreign keys
    "vocab", "strain_terms", ["dbxref"],  # this is a list to allow for compound keys
    constraint_names=[['isa', "biosample_cell_line_fkey"]],
    comment="Must be a valid reference to a cell line.",
    acls={}, acl_bindings={},
    annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Cell Line'}}
)

specimen_fk = em.ForeignKey.define(
    ["specimen"],  # this is a list to allow for compound foreign keys
    "isa", "specimen", ["RID"],  # this is a list to allow for compound keys
    constraint_names=[['isa', "biosample_specimen_hack_fkey"]]
)

specimen_type_fk = em.ForeignKey.define(
    ['specimen_type'],
    "vocab", "specimen_terms", ["dbxref"],
    constraint_names=[['isa', "biosample_specimen_type_fkey"]],
    comment="Must be a valid reference to a specimen type.",
    acls={}, acl_bindings={},
    annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Specimen Type'}}
)


schema_name = 'isa'
table_name = 'biosample'

server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()

biosample = model_root.table('isa', 'biosample')

biosample.create_column(catalog, cell_line_column_def)
biosample.create_column(catalog,specimen_column_def)
biosample.create_column(catalog,specimen_type_column_def)
biosample.column_definitions[5].delete(catalog)
