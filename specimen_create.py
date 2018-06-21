from deriva.core import ErmrestCatalog, get_credential
import deriva.core.ermrest_model as em

column_defs = [
    em.Column.define(
        "dataset", em.builtin_types.text, nullok=True,
        comment="Cell line used for the speciman."
    ),
    em.Column.define(
        "cell_line", em.builtin_types.text, nullok=True,
        comment="Cell line used for the speciman."
    ),
    em.Column.define(
        "species", em.builtin_types.text, nullok=True,
        comment="Species of the specimen"
    ),
    em.Column.define(
        "anatomy", em.builtin_types.text, nullok=True,
        comment="Anatomical region speciment was obtained from.",
    ),
    em.Column.define(
        "description", em.builtin_types.text, nullok=True,
        comment="Description of the specimen.",
    ),
    em.Column.define(
        'collection_date', em.builtin_types.date, nullok=True,
        comment='Date the specimen was obtained'
    )
]

key_defs = [
  em.Key.define(
    ["dataset", "RID"], # this is a list to allow for compound keys
    constraint_names=[ ['isa', "specimen_RID_key"] ],
    comment="RID and dataset must be distinct.",
    annotations={},
  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['dataset'],
        'isa', 'dataset', ['RID'],
        constraint_names=[['isa', 'specimen_dataset_fkey']],
    ),
    em.ForeignKey.define(
        ["cell_line"],  # this is a list to allow for compound foreign keys
        "vocab", "cell_line_terms", ["RID"],  # this is a list to allow for compound keys
        constraint_names=[['isa', "specimen_cell_line_fkey"]],
        comment="Must be a valid reference to a cell line.",
        acls={}, acl_bindings={},
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Cell Line'}}
    ),
    em.ForeignKey.define(
        ['species'],
        'vocab', 'species_terms', ['RID'],
        constraint_names=[['isa', 'specimen_species_fkey']],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Species'}},
    ),
    em.ForeignKey.define(
        ['anatomy'],
        'vocab', 'anatomy_terms', ['RID'],
        constraint_names=[['isa', 'specimen_anatomy_fkey']],
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Anatomy'}},
    )
]

schema_name = 'isa'
table_name = 'specimen'
table_comment = "Table of biological speciments from which biosamples will be created."

table_def = em.Table.define(
  table_name,
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment=table_comment,
  acls={},
  acl_bindings={},
  annotations={},
  provide_system=True,
)

server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.create_table(catalog, table_def)



