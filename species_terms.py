from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import re

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas['isa']

schema = model_root.schemas[schema_name]

new_vocab_table = schema.create_table(catalog,
    em.Table.define_vocabulary('species_terms','PBCCONSORTIUM:{RID}',comment='Terms for species')
)