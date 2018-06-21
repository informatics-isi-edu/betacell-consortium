from deriva.core import ErmrestCatalog, get_credential
import deriva.core.ermrest_model as em


column_defs = [
    em.Column.define(
        "protocol", em.builtin_types.text, nullok=False,
        comment="Protocol Foreign key."
    ),
    em.Column.define(
        "treatment", em.builtin_types.text, nullok=False,
        comment="Treatment foreign key."
    ),

]

key_defs = [
  em.Key.define(
    ["protocol", 'treatment'], # this is a list to allow for compound keys
    constraint_names=[ ['isa', "protocol_treatment_RID_key"] ],
    comment="protocol and treatment must be distinct.",
    annotations={},
  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['protocol'],
        'isa', 'protocol', ['RID'],
        constraint_names=[['isa', 'protocol_treatment_protocol_fkey']],
    ),
    em.ForeignKey.define(
        ["treatment"],  # this is a list to allow for compound foreign keys
        "vocab", "treatment_terms", ["RID"],  # this is a list to allow for compound keys
        constraint_names=[['isa', "protocol_treatement_treatment_fkey"]],
        comment="Must be a valid reference to a treatment.",
        acls={}, acl_bindings={},
        annotations={'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Treatment'}}
    ),
]

schema_name = 'isa'
table_name = 'protocol_treatment'
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



