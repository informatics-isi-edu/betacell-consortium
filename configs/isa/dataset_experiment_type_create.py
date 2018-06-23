import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'dataset_id',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'experiment_type',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['experiment_type', 'dataset_id'],
                constraint_names=[('isa', 'dataset_experiment_type_pkey')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'dataset_experiment_type_RID_key')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['dataset_id'],
            'isa', 'dataset', ['id'],
            constraint_names = [('isa', 'dataset_experiment_type_dataset_id_fkey')],
        annotations = {'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Datasets'}},
    ),
]

table_annotations =
{'tag:misd.isi.edu,2015:display': {'name': 'Experiment_type'}}

table_def = em.Table.define(
    dataset_experiment_type,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment=None,
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:dataset_experiment_type')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'dataset_experiment_type'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
