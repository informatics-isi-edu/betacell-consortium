% load_ext
autoreload
% autoreload
2

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()

experiment = model_root.table('isa', 'experiment')
biosample = model_root.table('isa', 'biosample')
dataset = model_root.table('isa', 'dataset')
protocol = model_root.table('isa', 'protocol')
replicate = model_root.table('isa', 'replicate')
imaging_data = model_root.table('isa', 'imaging_data')

pb = catalog.getPathBuilder()
isa = pb.isa
pbexperiment = isa.experiment
pbbiosample = isa.biosample
pbdataset = isa.dataset
pbprotocol = isa.protocol

experiment.visible_columns['filter'] = {
    'and': [
        {'source': [{'outbound': ['isa', 'experiment_protocol_fkey']},
                    'RID'],
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

experiment.visible_columns['entry'] = [
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

experiment.visible_columns['detailed'] = [
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

experiment.visible_columns['compact'] = [['isa', 'experiment_pkey'],
                                         ['isa', 'experiment_dataset_fkey'],
                                         ['isa', 'experiment_experiment_type_fkey'],
                                         ['isa', 'experiment_protocol_fkey'],
                                         'local_identifier']

experiment.visible_foreign_keys['detailed'] = [
    ['isa', 'experiment_control_assay_fkey'],
    ['isa', 'replicate_experiment_fkey'],
    {'source': [{'inbound': ['isa', 'replicate_experiment_fkey']},
                {'inbound': ['isa', 'sequencing_data_replicate_fkey']},
                'RID']},
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

experiment.visible_foreign_keys['entry'] = [
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

experiment.apply(catalog)
