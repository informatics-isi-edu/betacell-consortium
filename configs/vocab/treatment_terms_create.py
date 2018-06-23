import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'id',em.builtin_types.{'typename': 'ermrest_curie', 'is_array': False},
            nullok=False,
            annotations={}
            comment='The preferred Compact URI (CURIE) for this term.'),
    
    em.Column.define(
            'uri',em.builtin_types.{'typename': 'ermrest_uri', 'is_array': False},
            nullok=False,
            annotations={}
            comment='The preferred URI for this term.'),
    
    em.Column.define(
            'name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment='The preferred human-readable name for this term.'),
    
    em.Column.define(
            'description',em.builtin_types.{'typename': 'markdown', 'is_array': False},
            nullok=False,
            annotations={}
            comment='A longer human-readable description of this term.'),
    
    em.Column.define(
            'synonyms',em.builtin_types.{'typename': 'text[]', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Alternate human-readable names for this term.'),
    
key_defs = [
    em.Key.define(
                ['uri'],
                constraint_names=[('vocab', 'treatment_terms_urikey1')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('vocab', 'treatment_terms_RIDkey1')],
                annotation={},
                comment=None),
    em.Key.define(
                ['id'],
                constraint_names=[('vocab', 'treatment_terms_idkey1')],
                annotation={},
                comment=None),
]

fkey_defs = [
]

table_annotations =
{   'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   'name',
                                                                'id',
                                                                'synonyms',
                                                                'description'],
                                                 'detailed': [   'name',
                                                                 'id',
                                                                 'synonyms',
                                                                 'uri',
                                                                 'description'],
                                                 'entry': [   'name',
                                                              'id',
                                                              'synonyms',
                                                              'uri',
                                                              'description'],
                                                 'filter': {   'and': [   {   'open': True,
                                                                              'source': 'name'},
                                                                          {   'open': True,
                                                                              'source': 'id'},
                                                                          {   'open': True,
                                                                              'source': 'synonyms'}]}}}

table_def = em.Table.define(
    treatment_terms,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment='Terms for treatments',
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table vocab:treatment_terms')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'vocab'
    table_name = 'treatment_terms'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
