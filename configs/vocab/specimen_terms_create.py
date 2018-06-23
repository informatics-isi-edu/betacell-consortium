import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'dbxref',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={'tag:misd.isi.edu,2015:display': {'name': 'Code'}, 'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{dbxref}}](/chaise/record/#1/data_commons:cvterm/dbxref={{#encode}}{{dbxref}}{{/encode}})'}}}
            comment=None),
    
    em.Column.define(
            'dbxref_unversioned',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'cv',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={'tag:misd.isi.edu,2015:display': {'name': 'Controlled Vocabulary'}, 'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'definition',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'is_obsolete',em.builtin_types.{'typename': 'boolean', 'is_array': False},
            nullok=False,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'is_relationshiptype',em.builtin_types.{'typename': 'boolean', 'is_array': False},
            nullok=False,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'synonyms',em.builtin_types.{'typename': 'text[]', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'alternate_dbxrefs',em.builtin_types.{'typename': 'text[]', 'is_array': False},
            nullok=True,
            annotations={'tag:misd.isi.edu,2015:display': {'name': 'Alternate Codes'}, 'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['name', 'cv', 'is_obsolete'],
                constraint_names=[('vocab', 'specimen_terms_cv_name_is_obsolete_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('vocab', 'specimen_terms_RID_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['dbxref'],
                constraint_names=[('vocab', 'specimen_terms_pkey')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['cv'],
            'data_commons', 'cv', ['name'],
            constraint_names = [('vocab', 'specimen_terms_cv_fkey')],
    ),
    em.ForeignKey.define(
            ['dbxref'],
            'data_commons', 'cvterm', ['dbxref'],
            constraint_names = [('vocab', 'specimen_terms_dbxref_fkey')],
    ),
]

table_annotations =
{   'tag:isrd.isi.edu,2016:table-display': {   '*': {   'row_order': [   {   'column': 'name'}]},
                                               'row_name': {   'row_markdown_pattern': '{{name}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   '*': [   'name',
                                                          'dbxref',
                                                          'definition',
                                                          [   'vocab',
                                                              'specimen_terms_cv_fkey'],
                                                          'is_obsolete',
                                                          'is_relationshiptype',
                                                          'synonyms',
                                                          'alternate_dbxrefs'],
                                                 'entry': [   [   'vocab',
                                                                  'specimen_terms_dbxref_fkey']],
                                                 'filter': {   'and': [   {   'source': 'name'},
                                                                          {   'source': 'dbxref'},
                                                                          {   'source': 'definition'},
                                                                          {   'source': 'cv'},
                                                                          {   'source': 'is_obsolete'},
                                                                          {   'source': 'is_relationshiptype'}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   '*': [   {   'source': [   {   'inbound': [   'isa',
                                                                                                    'dataset_specimen_specimen_fkey']},
                                                                                 {   'outbound': [   'isa',
                                                                                                     'dataset_specimen_dataset_id_fkey']},
                                                                                 'id']}]}}

table_def = em.Table.define(
    specimen_terms,
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
    parser = argparse.ArgumentParser(description='Load foreign key defs for table vocab:specimen_terms')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'vocab'
    table_name = 'specimen_terms'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
