import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

fkey_defs = [
    em.ForeignKey.define(
            ['dataset', 'experiment'],
            'isa', 'experiment', ['dataset', 'RID'],
            constraint_names = [('isa', 'replicate_experiment_fkey')],
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
    em.ForeignKey.define(
            ['biosample'],
            'isa', 'biosample', ['RID'],
            constraint_names = [('isa', 'replicate_biosample_fkey')],
        annotations = {'tag:isrd.isi.edu,2016:foreign-key': {'domain_filter_pattern': 'dataset={{{_dataset}}}'}},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
    em.ForeignKey.define(
            ['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names = [('isa', 'replicate_dataset_fkey')],
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
]

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:replicate')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', action="store_true", help='delete existing foreign keys before loading)')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'isa'
    table_name = 'replicate'

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
