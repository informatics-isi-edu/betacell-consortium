import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'id',em.builtin_types.{'typename': 'serial4', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'label',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'description',em.builtin_types.{'typename': 'markdown', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'bg_color_r',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'bg_color_g',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'bg_color_b',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'bounding_box_color_r',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'bounding_box_color_g',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'bounding_box_color_b',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'show_bounding_box',em.builtin_types.{'typename': 'boolean', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'rotate',em.builtin_types.{'typename': 'boolean', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'volume',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'experiment',em.builtin_types.{'typename': 'ermrest_rid', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['RID'],
                constraint_names=[('viz', 'model_RID_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['id'],
                constraint_names=[('viz', 'model_pkey')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['experiment'],
            'isa', 'experiment', ['RID'],
            constraint_names = [('viz', 'model_experiment_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'SET NULL',
    ),
    em.ForeignKey.define(
            ['volume'],
            'isa', 'imaging_data', ['RID'],
            constraint_names = [('viz', 'model_volume_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
]

table_annotations =
{   'tag:isrd.isi.edu,2016:table-display': {   'compact': {   'row_markdown_pattern': ':::iframe '
                                                                                      '[{{{label}}}](/mesh-viewer/view.html?model=/ermrest/catalog/1/entity/viz:model_json/RID={{{_RID}}}){width=1024 '
                                                                                      'height=768 '
                                                                                      '.iframe} \n'
                                                                                      ':::'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'viz',
                                                                    'model_dataset_fkey'],
                                                                'label',
                                                                'description',
                                                                [   'viz',
                                                                    'model_derived_from_fkey'],
                                                                [   'viz',
                                                                    'model_anatomy_fkey']]},
    'tag:misd.isi.edu,2015:display': {'name': '3D Surface Models'}}

table_def = em.Table.define(
    model,
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
    parser = argparse.ArgumentParser(description='Load foreign key defs for table viz:model')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'viz'
    table_name = 'model'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
