from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re


server = 'pbcconsortium.isrd.isi.edu'

schema_name = 'isa'
table_name = 'experiment'

table_display = \
    {
        'row_name': {'row_markdown_pattern': '{{RID}}{{#local_identifier}} - {{local_identifier}} {{/local_identifier}}{{#biosample_summary}} - {{biosample_summary}}{{/biosample_summary}}'}
    }


visible_columns['filter'] = \
    {'and': [{'source': [{'outbound': ['isa', 'experiment_protocol_fkey']}, 'RID'],
              'open': True,
              'entity': True},
             {'source': [{'outbound': ['isa', 'experiment_experiment_type_fkey']},
                         'dbxref'],
              'open': True,
              'entity': True},
             {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                         {'outbound': ['isa', 'replicate_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_species_fkey']},
                         'dbxref'],
              'open': True,
              'entity': True},
             {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                         {'outbound': ['isa', 'replicate_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_cell_line_fkey']},
                         'dbxref'],
              'open': True,
              'entity': True},
             {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                         {'outbound': ['isa', 'replicate_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_stage_fkey']},
                         'dbxref'],
              'open': True,
              'entity': True},
             {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                         {'outbound': ['isa', 'replicate_biosample_fkey']},
                         {'outbound': ['isa', 'biosample_genotype_fkey']},
                         'dbxref'],
              'open': True,
              'entity': True}]}

evisible_columns['entry'] = \
    [
        ['isa', 'experiment_dataset_fkey'],
        'local_identifier',
        'biosample_summary',
        ['isa', 'experiment_experiment_type_fkey'],
        ['isa', 'experiment_molecule_type_fkey'],
        ['isa', 'experiment_strandedness_fkey'],
        ['isa', 'experiment_rnaseq_selection_fkey'],
        ['isa', 'experiment_target_of_assay_fkey'],
        ['isa', 'experiment_chromatin_modifier_fkey'],
        ['isa', 'experiment_transcription_factor_fkey'],
        ['isa', 'experiment_histone_modification_fkey'],
        ['isa', 'experiment_control_assay_fkey'],
        ['isa', 'experiment_protocol_fkey']
    ]

visible_columns['detailed'] = \
    [
        ['isa', 'experiment_pkey'],
        ['isa', 'experiment_dataset_fkey'],
        'local_identifier',
        ['isa', 'experiment_experiment_type_fkey'],
        'biosample_summary',
        ['isa', 'experiment_molecule_type_fkey'],
        ['isa', 'experiment_strandedness_fkey'],
        ['isa', 'experiment_rnaseq_selection_fkey'],
        ['isa', 'experiment_target_of_assay_fkey'],
        ['isa', 'experiment_chromatin_modifier_fkey'],
        ['isa', 'experiment_transcription_factor_fkey'],
        ['isa', 'experiment_histone_modification_fkey'],
        ['isa', 'experiment_control_assay_fkey'],
        ['isa', 'experiment_protocol_fkey']
    ]

visible_columns['compact'] = \
    [
        ['isa', 'experiment_pkey'],
        ['isa', 'experiment_dataset_fkey'],
        ['isa', 'experiment_experiment_type_fkey'],
        ['isa', 'experiment_protocol_fkey'],
        'local_identifier'
    ]


visible_foreign_keys['detailed'] = [
    ['isa', 'experiment_control_assay_fkey'],
    {'source': [{'outbound': ['isa', 'experiment_dataset_fkey']},
                {'outbound': ['viz', 'model_dataset_fkey']},
                'model']},
    ['isa', 'replicate_experiment_fkey'],
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'processed_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'xray_tomography_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'imaging_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'mesh_data_replicate_fkey']},
                'RID']}
]

visible_foreign_keys['entry'] = [
    ['isa', 'experiment_control_assay_fkey'],
    ['isa', 'replicate_experiment_fkey'],
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'sequencing_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'xray_tomography_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'processed_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'imaging_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'mesh_data_replicate_fkey']},
                'RID']},
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'track_data_replicate_fkey']},
                'RID']},
]

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.tables[table_name]

if len(visible_columns) > 0:
    for k,v in visible_columns.items():
     table.visible_columns[k] = v

if len(visible_foreign_keys) > 0:
    for k,v in visible_foreign_keys.items():
        table.visible_foreign_keys[k] = v

table.apply(catalog)


