import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'first_name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'middle_name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'last_name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'email',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'degrees',em.builtin_types.{'typename': 'json', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'affiliation',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'website',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['name'],
                constraint_names=[('isa', 'person_pkey')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'person_RID_key')],
                annotation={},
                comment=None),
]

fkey_defs = [
]

table_annotations =
{   'tag:isrd.isi.edu,2016:table-display': {   '*': {   'row_order': [   {   'column': 'last_name',
                                                                             'descending': False}]},
                                               'row_name': {   'row_markdown_pattern': '{{{first_name}}} '
                                                                                       '{{{last_name}}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   'name',
                                                                'email',
                                                                'affiliation'],
                                                 'detailed': [   'name',
                                                                 'email',
                                                                 'affiliation']}}

table_def = em.Table.define(
    person,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment='domain',
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:person')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'person'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
