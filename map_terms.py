credential = get_credential(server)

catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()

table_name = 'protocol_treatment'
key_column = 'specimen_type'

for i in model_root.schemas['isa'].tables[table_name].foreign_keys:
    i.delete(catalog)

table = pb.isa.protocol_treatment
term_table = pb.vocab.treatment_terms
key_column = 'treatment'

term_map = {i['RID']:i['id'] for i in term_table.entities(term_table.RID, term_table.id)}
keys = list(table.entities(table.RID, getattr(table,key_column)))

for i in keys:
    i[key_column] = term_map[i[key_column]]

table.update(keys)