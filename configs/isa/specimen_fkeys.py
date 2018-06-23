import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

fkey_defs = [
    em.ForeignKey.define(
            ['anatomy'],
            'vocab', 'anatomy_terms', ['id'],
            constraint_names = [('isa', 'specimen_anatomy_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(
            ['cell_line'],
            'vocab', 'cell_line_terms', ['id'],
            constraint_names = [('isa', 'specimen_cell_line_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        comment = 'Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(
            ['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names = [('isa', 'specimen_dataset_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(
            ['species'],
            'vocab', 'species_terms', ['id'],
            constraint_names = [('isa', 'specimen_species_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
]

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:specimen')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', action="store_true", help='delete existing foreign keys before loading)')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'isa'
    table_name = 'specimen'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    if delete_fkeys:
        for k in table.foreign_keys:
            k.delete(catalog)

    model_root = catalog.getCatalogModel()
    for i in fkey_defs:
        table.create_fkey(catalog,i)

if __name__ == "__main__":
    main()
