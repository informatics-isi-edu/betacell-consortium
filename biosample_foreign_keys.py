import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

fkey_defs = [
    em.ForeignKey.define(
        ['specimen'],
        'isa', 'specimen', ['RID'],
        constraint_names = [('isa', 'biosample_specimen_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(
        ['dataset'],
        'isa', 'dataset', ['RID'],
        constraint_names = [('isa', 'biosample_dataset_fkey')],
        annotations = {'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:foreign-key': {}},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
    em.ForeignKey.define(
        ['specimen_type'],
        'vocab', 'specimen_type_terms', ['id'],
        constraint_names = [('isa', 'biosample_specimen_type_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        comment = 'Must be a valid reference to a specimen type.',
    ),
]

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:biosample')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                        help='Catalog server name')
    parser.add_argument('--delete', default=False, help='delete existing foreign keys before loading)')
    args = parser.parse_args()

    delete_fkeys = args.delete
    server = args.server
    schema_name = 'isa'
    table_name = 'biosample'

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
