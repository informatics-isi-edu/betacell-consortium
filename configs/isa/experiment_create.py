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
            'local_identifier',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'biosample_summary',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:generated': None}
            comment='System-generated column with summary of all related biosamples'),
    
    em.Column.define(
            'experiment_type',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_experiment_type_fkey.rowName}}}'}}}
            comment=None),
    
    em.Column.define(
            'control_assay',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'protocol',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.experiment_protocol_fkey.rowName}}}'}}}
            comment=None),
    
key_defs = [
    em.Key.define(
                ['dataset', 'RID'],
                constraint_names=[('isa', 'experiment_RID_dataset_key')],
                annotation={},
                comment=None),
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'experiment_pkey')],
                annotation={},
                comment=None),
    em.Key.define(
                ['dataset', 'local_identifier'],
                constraint_names=[('isa', 'experiment_dataset_local_identifier_key')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['protocol'],
            'isa', 'protocol', ['RID'],
            constraint_names = [('isa', 'experiment_protocol_fkey')],
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
    em.ForeignKey.define(
            ['experiment_type'],
            'vocab', 'experiment_type_terms', ['RID'],
            constraint_names = [('isa', 'experiment_experiment_type_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(
            ['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names = [('isa', 'experiment_dataset_fkey')],
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
    ),
]

table_annotations =
{   'table_display': {   'row_name': {   'row_markdown_pattern': '{{RID}}{{#local_identifier}} '
                                                                 '- '
                                                                 '{{local_identifier}} '
                                                                 '{{/local_identifier}}{{#biosample_summary}} '
                                                                 '- '
                                                                 '{{biosample_summary}}{{/biosample_summary}}'}},
    'tag:isrd.isi.edu,2016:table-display': {   'row_name': {   'row_markdown_pattern': '{{RID}}{{#local_identifier}} '
                                                                                       '- '
                                                                                       '{{local_identifier}} '
                                                                                       '{{/local_identifier}}{{#biosample_summary}} '
                                                                                       '- '
                                                                                       '{{biosample_summary}}{{/biosample_summary}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'experiment_pkey'],
                                                                [   'isa',
                                                                    'experiment_dataset_fkey'],
                                                                [   'isa',
                                                                    'experiment_experiment_type_fkey'],
                                                                [   'isa',
                                                                    'experiment_protocol_fkey'],
                                                                'local_identifier'],
                                                 'detailed': [   [   'isa',
                                                                     'experiment_pkey'],
                                                                 [   'isa',
                                                                     'experiment_dataset_fkey'],
                                                                 'local_identifier',
                                                                 [   'isa',
                                                                     'experiment_experiment_type_fkey'],
                                                                 'biosample_summary',
                                                                 [   'isa',
                                                                     'experiment_target_of_assay_fkey'],
                                                                 [   'isa',
                                                                     'experiment_control_assay_fkey'],
                                                                 [   'isa',
                                                                     'experiment_protocol_fkey']],
                                                 'entry': [   [   'isa',
                                                                  'experiment_dataset_fkey'],
                                                              'local_identifier',
                                                              'biosample_summary',
                                                              [   'isa',
                                                                  'experiment_experiment_type_fkey'],
                                                              [   'isa',
                                                                  'experiment_target_of_assay_fkey'],
                                                              [   'isa',
                                                                  'experiment_control_assay_fkey'],
                                                              [   'isa',
                                                                  'experiment_protocol_fkey']],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'experiment_protocol_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Treatmemt',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'experiment_protocol_fkey']},
                                                                                            {   'inbound': [   'isa',
                                                                                                               'protocol_treatment_protocol_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'protocol_treatment_treatment_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Treatment '
                                                                                               'Concentration',
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'experiment_protocol_fkey']},
                                                                                            {   'inbound': [   'isa',
                                                                                                               'protocol_treatment_protocol_fkey']},
                                                                                            'treatment_concentration'],
                                                                              'ux_mode': 'choices'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Timepoint',
                                                                              'open': False,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'experiment_protocol_fkey']},
                                                                                            'timepoint'],
                                                                              'ux_mode': 'choices'},
                                                                          {   'entity': True,
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'experiment_experiment_type_fkey']},
                                                                                            'name']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Cell '
                                                                                               'Line',
                                                                              'open': True,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'replicate_experiment_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'replicate_biosample_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'biosample_specimen_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'specimen_cell_line_fkey']},
                                                                                            'name']}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'experiment_control_assay_fkey'],
                                                                      {   'open': False,
                                                                          'source': [   {   'inbound': [   'viz',
                                                                                                           'model_experiment_fkey']},
                                                                                        'RID']},
                                                                      [   'isa',
                                                                          'replicate_experiment_fkey'],
                                                                      {   'source': [   {   'inbound': [   'isa',
                                                                                                           'replicate_experiment_fkey']},
                                                                                        {   'inbound': [   'isa',
                                                                                                           'processed_data_replicate_fkey']},
                                                                                        'RID']},
                                                                      {   'source': [   {   'inbound': [   'isa',
                                                                                                           'replicate_experiment_fkey']},
                                                                                        {   'inbound': [   'isa',
                                                                                                           'xray_tomography_data_replicate_fkey']},
                                                                                        'RID']},
                                                                      {   'source': [   {   'inbound': [   'isa',
                                                                                                           'replicate_experiment_fkey']},
                                                                                        {   'inbound': [   'isa',
                                                                                                           'imaging_data_replicate_fkey']},
                                                                                        'RID']},
                                                                      {   'source': [   {   'inbound': [   'isa',
                                                                                                           'replicate_experiment_fkey']},
                                                                                        {   'inbound': [   'isa',
                                                                                                           'mesh_data_replicate_fkey']},
                                                                                        'RID']}],
                                                      'entry': [   [   'isa',
                                                                       'experiment_control_assay_fkey'],
                                                                   [   'viz',
                                                                       'model_experiment_fkey'],
                                                                   [   'isa',
                                                                       'replicate_experiment_fkey'],
                                                                   {   'source': [   {   'inbound': [   'isa',
                                                                                                        'replicate_experiment_fkey']},
                                                                                     {   'inbound': [   'isa',
                                                                                                        'sequencing_data_replicate_fkey']},
                                                                                     'RID']},
                                                                   {   'source': [   {   'inbound': [   'isa',
                                                                                                        'replicate_experiment_fkey']},
                                                                                     {   'inbound': [   'isa',
                                                                                                        'xray_tomography_data_replicate_fkey']},
                                                                                     'RID']},
                                                                   {   'source': [   {   'inbound': [   'isa',
                                                                                                        'replicate_experiment_fkey']},
                                                                                     {   'inbound': [   'isa',
                                                                                                        'processed_data_replicate_fkey']},
                                                                                     'RID']},
                                                                   {   'source': [   {   'inbound': [   'isa',
                                                                                                        'replicate_experiment_fkey']},
                                                                                     {   'inbound': [   'isa',
                                                                                                        'imaging_data_replicate_fkey']},
                                                                                     'RID']},
                                                                   {   'source': [   {   'inbound': [   'isa',
                                                                                                        'replicate_experiment_fkey']},
                                                                                     {   'inbound': [   'isa',
                                                                                                        'mesh_data_replicate_fkey']},
                                                                                     'RID']},
                                                                   {   'source': [   {   'inbound': [   'isa',
                                                                                                        'replicate_experiment_fkey']},
                                                                                     {   'inbound': [   'isa',
                                                                                                        'track_data_replicate_fkey']},
                                                                                     'RID']}]}}

table_def = em.Table.define(
    experiment,
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
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:experiment')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'experiment'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()
