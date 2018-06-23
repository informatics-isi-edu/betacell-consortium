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
            'accession',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment=None),
    
    em.Column.define(
            'title',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'project',em.builtin_types.{'typename': 'int8', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'funding',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'summary',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'description',em.builtin_types.{'typename': 'markdown', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'mouse_genetic',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'human_anatomic',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'study_design',em.builtin_types.{'typename': 'markdown', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'release_date',em.builtin_types.{'typename': 'date', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'status',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{ $fkeys.isa.dataset_status_fkey.rowName }}}'}}}
            comment=None),
    
    em.Column.define(
            'show_in_jbrowse',em.builtin_types.{'typename': 'boolean', 'is_array': False},
            nullok=True,
            annotations={'tag:misd.isi.edu,2015:display': {'name': 'Genome Browser'}, 'tag:isrd.isi.edu,2016:column-display': {'detailed': {'markdown_pattern': '{{#_show_in_jbrowse}}Use the embedded browser here or [view in a new window](/jbrowse/latest/?dataset={{{_RID}}}){target=_blank}.\n :::iframe [](/jbrowse/latest/?dataset={{{_RID}}}){width=800 height=600 .iframe} \n:::{{/_show_in_jbrowse}}'}}}
            comment=None),
    
    em.Column.define(
            '_keywords',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['id'],
                constraint_names=[('isa', 'dataset_pkey')],
                annotation={},
                comment=None),
    em.Key.define(
                ['accession'],
                constraint_names=[('isa', 'accession_unique')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'dataset_RID_key')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['status'],
            'vocab', 'dataset_status_terms', ['dbxref'],
            constraint_names = [('isa', 'dataset_status_fkey')],
        annotations = {'tag:isrd.isi.edu,2016:foreign-key': {'to_name': 'Status'}},
    ),
    em.ForeignKey.define(
            ['project'],
            'isa', 'project', ['id'],
            constraint_names = [('isa', 'dataset_project_fkey')],
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
]

table_annotations =
{   'tag:isrd.isi.edu,2016:table-display': {   '*': {   'row_order': [   {   'column': 'accession',
                                                                             'descending': True}]},
                                               'row_name': {   'row_markdown_pattern': '{{title}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'dataset_RID_key'],
                                                                [   'isa',
                                                                    'accession_unique'],
                                                                'title',
                                                                [   'isa',
                                                                    'dataset_project_fkey'],
                                                                'status',
                                                                'release_date'],
                                                 'detailed': [   [   'isa',
                                                                     'dataset_RID_key'],
                                                                 'accession',
                                                                 'description',
                                                                 'study_design',
                                                                 [   'isa',
                                                                     'dataset_project_fkey'],
                                                                 [   'isa',
                                                                     'dataset_status_fkey'],
                                                                 'funding',
                                                                 'release_date',
                                                                 'show_in_jbrowse',
                                                                 [   'isa',
                                                                     'publication_dataset_fkey'],
                                                                 [   'isa',
                                                                     'dataset_experiment_type_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_data_type_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_phenotype_dataset_fkey'],
                                                                 [   'isa',
                                                                     'dataset_organism_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_anatomy_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_gender_dataset_id_fkey'],
                                                                 [   'isa',
                                                                     'dataset_instrument_dataset_id_fkey']],
                                                 'entry': [   'accession',
                                                              'title',
                                                              [   'isa',
                                                                  'dataset_project_fkey'],
                                                              'description',
                                                              'study_design',
                                                              'release_date',
                                                              [   'isa',
                                                                  'dataset_status_fkey'],
                                                              'show_in_jbrowse'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_organism_dataset_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_organism_organism_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_experiment_type_dataset_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_experiment_type_experiment_type_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_data_type_data_type_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_data_type_dataset_id_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_anatomy_dataset_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_anatomy_anatomy_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'dataset_phenotype_dataset_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'dataset_phenotype_phenotype_fkey']},
                                                                                            'dbxref']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Pubmed '
                                                                                               'ID',
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'publication_dataset_fkey']},
                                                                                            'pmid']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Project '
                                                                                               'Investigator',
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'dataset_project_fkey']},
                                                                                            {   'inbound': [   'isa',
                                                                                                               'project_investigator_project_id_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'project_investigator_person_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': False,
                                                                              'open': False,
                                                                              'source': 'accession'},
                                                                          {   'entity': False,
                                                                              'open': False,
                                                                              'source': 'title'},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'dataset_project_fkey']},
                                                                                            'id']},
                                                                          {   'entity': False,
                                                                              'open': False,
                                                                              'source': 'release_date'},
                                                                          {   'entity': True,
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'dataset_status_fkey']},
                                                                                            'name']}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   '*': [   [   'isa',
                                                                   'thumbnail_dataset_fkey'],
                                                               [   'viz',
                                                                   'model_dataset_fkey'],
                                                               [   'isa',
                                                                   'previews_dataset_id_fkey'],
                                                               [   'isa',
                                                                   'experiment_dataset_fkey'],
                                                               [   'isa',
                                                                   'biosample_dataset_fkey'],
                                                               [   'isa',
                                                                   'enhancer_dataset_fkey'],
                                                               [   'isa',
                                                                   'clinical_assay_dataset_fkey'],
                                                               [   'isa',
                                                                   'file_dataset_fkey'],
                                                               [   'isa',
                                                                   'external_reference_id_fkey']]}}

table_def = em.Table.define(
    dataset,
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
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:dataset')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'dataset'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
