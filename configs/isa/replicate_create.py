import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'dataset',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'biosample',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'bioreplicate_number',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'technical_replicate_number',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
    em.Column.define(
            'experiment',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['technical_replicate_number', 'dataset', 'experiment', 'biosample'],
                constraint_names=[('isa', 'replicate_dataset_experiment_biosample_technical_replicate__key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['technical_replicate_number', 'dataset', 'biosample', 'experiment', 'bioreplicate_number'],
                constraint_names=[('isa', 'replicate_dataset_experiment_biosample_bioreplicate_number__key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['dataset', 'RID'],
                constraint_names=[('isa', 'replicate_RID_dataset_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'replicate_pkey')],
                annotation={},
                comment=None),
]

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

table_annotations =
{   'tag:isrd.isi.edu,2016:table-display': {   'compact': {   'row_order': [   {   'column': 'bioreplicate_number',
                                                                                   'descending': False}]},
                                               'row_name': {   'row_markdown_pattern': '{{local_identifier}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'replicate_pkey'],
                                                                [   'isa',
                                                                    'replicate_biosample_fkey'],
                                                                'bioreplicate_number',
                                                                'technical_replicate_number'],
                                                 'detailed': [   [   'isa',
                                                                     'replicate_pkey'],
                                                                 [   'isa',
                                                                     'replicate_experiment_fkey'],
                                                                 [   'isa',
                                                                     'replicate_biosample_fkey'],
                                                                 'bioreplicate_number',
                                                                 'technical_replicate_number'],
                                                 'entry': [   [   'isa',
                                                                  'replicate_experiment_fkey'],
                                                              [   'isa',
                                                                  'replicate_biosample_fkey'],
                                                              'bioreplicate_number',
                                                              'technical_replicate_number'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'markdown_name': 'Dataset',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'replicate_dataset_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Experiment',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'replicate_experiment_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Biosample',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'replicate_biosample_fkey']},
                                                                                            'RID']}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'xray_tomography_data_replicate_fkey'],
                                                                      [   'isa',
                                                                          'mesh_data_replicate_fkey'],
                                                                      [   'isa',
                                                                          'processed_data_replicate_fkey'],
                                                                      [   'isa',
                                                                          'imaging_data_replicate_fkey']],
                                                      'entry': [   [   'isa',
                                                                       'xray_tomography_data_replicate_fkey'],
                                                                   [   'isa',
                                                                       'mesh_data_replicate_fkey'],
                                                                   [   'isa',
                                                                       'processed_data_replicate_fkey'],
                                                                   [   'isa',
                                                                       'imaging_data_replicate_fkey']]}}

table_def = em.Table.define(
    replicate,
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
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:replicate')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'replicate'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
