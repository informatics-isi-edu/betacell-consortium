from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

server = 'pbcconsortium.isrd.isi.edu'
schema_name = 'isa'
table_name = 'replicate'

filename= 'table_config.py'

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]


table.visible_columns