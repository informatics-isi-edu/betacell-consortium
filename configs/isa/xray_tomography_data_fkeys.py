import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

fkey_defs = [
    em.ForeignKey.define(
            ['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names = [('isa', 'xray_tomography_dataset_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a dataset.',
    ),
    em.ForeignKey.define(
            ['device'],
            'vocab', 'image_creation_device_terms', ['dbxref'],
            constraint_names = [('isa', 'xray_tomography_data_device_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a device.',
    ),
    em.ForeignKey.define(
            ['replicate', 'dataset'],
            'isa', 'replicate', ['RID', 'dataset'],
            constraint_names = [('isa', 'xray_tomography_data_replicate_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a dataset.',
    ),
    em.ForeignKey.define(
            ['equipment_model'],
            'vocab', 'instrument_terms', ['dbxref'],
            constraint_names = [('isa', 'xray_tomography_data_equipment_model_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a dataset.',
    ),
]

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:xray_tomography_data')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', action="store_true", help='delete existing foreign keys before loading)')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'isa'
    table_name = 'xray_tomography_data'

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
