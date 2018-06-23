import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'model',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'mesh',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'color_r',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'color_g',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'color_b',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'opacity',em.builtin_types.{'typename': 'float8', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['model', 'mesh'],
                constraint_names=[('viz', 'model_mesh_data_model_mesh_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('viz', 'model_mesh_data_pkey')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['mesh'],
            'isa', 'mesh_data', ['RID'],
            constraint_names = [('viz', 'model_mesh_data_mesh_fkey')],
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
    em.ForeignKey.define(
            ['model'],
            'viz', 'model', ['RID'],
            constraint_names = [('viz', 'model_mesh_data_model_fkey')],
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
]

table_annotations =
{}

table_def = em.Table.define(
    model_mesh_data,
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
    parser = argparse.ArgumentParser(description='Load foreign key defs for table viz:model_mesh_data')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'viz'
    table_name = 'model_mesh_data'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
