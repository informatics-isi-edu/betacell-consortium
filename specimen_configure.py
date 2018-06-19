from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re


server = 'pbcconsortium.isrd.isi.edu'

schema_name = 'isa'
table_name = 'specimen'

visible_columns = {
    'entry': [
        ['isa', 'local_identifier'],
        ['isa', 'specimen_dataset_fkey'],
        ['isa', 'specimen_cell_line_fkey'],
        ['isa', 'specimen_species_fkey'],
        ['isa', 'specimen_anatomy_fkey'],
        'description',
        'collection_date'
    ],
    'detailed': [
        ['isa', 'specimen_pkey'],
        'local_identifier',
        ['isa', 'specimen_dataset_fkey'],
        ['isa', 'specimen_cell_line_fkey'],
        ['isa', 'specimen_species_fkey'],
        ['isa', 'specimen_anatomy_fkey'],
        'description',
        'collection_date'
    ],
    'compact' : [
        ['isa', 'specimen_pkey'],
        'local_identifier',
        ['isa', 'specimen_cell_line_fkey'],
    ]
}

visible_foreign_keys = {
}

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]

if len(visible_columns) > 0:
    for k,v in visible_columns.items():
     table.visible_columns[k] = v

if len(visible_foreign_keys) > 0:
    for k,v in visible_foreign_keys.items():
        table.visible_foreign_keys[k] = v

table.apply(catalog)