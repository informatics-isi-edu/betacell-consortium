%load_ext autoreload
%autoreload 2

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import csv
import re

server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)

model_root = catalog.getCatalogModel()

experiment = model_root.table('isa', 'experiment')
biosample = model_root.table('isa', 'biosample')
dataset = model_root.table('isa', 'dataset')

# Clean up experiment
delcolumn = experiment.column_definitions['histone_modification']
delcolumn.delete(catalog, table = experiment)

delcolumn = experiment.column_definitions['strandedness']
delcolumn.delete(catalog, table = experiment)

delcolumn = experiment.column_definitions['target_of_assay']
delcolumn.delete(catalog, table = experiment)

delcolumn = experiment.column_definitions['molecule_type']
delcolumn.delete(catalog, table = experiment)

delcolumn = experiment.column_definitions['chromatin_modifier']
delcolumn.delete(catalog, table = experiment)

delcolumn = experiment.column_definitions['rnaseq_selection']
delcolumn.delete(catalog, table = experiment)

delcolumn = experiment.column_definitions['transcription_factor']
delcolumn.delete(catalog, table = experiment)

# Clean up biosample
delcolumn = biosample.column_definitions['gene']
delcolumn.delete(catalog, table = biosample)

delcolumn = biosample.column_definitions['genotype']
delcolumn.delete(catalog, table = biosample)

delcolumn = biosample.column_definitions['mutation']
delcolumn.delete(catalog, table = biosample)

delcolumn = biosample.column_definitions['stage']
delcolumn.delete(catalog, table = biosample)

delcolumn = biosample.column_definitions['theiler_stage']
delcolumn.delete(catalog, table = biosample)

delcolumn = biosample.column_definitions['litter']
delcolumn.delete(catalog, table = biosample)

delcolumn = biosample.column_definitions['phenotype']
delcolumn.delete(catalog, table = biosample)

delcolumn = biosample.column_definitions['origin']
delcolumn.delete(catalog, table = biosample)

# Clean up dataset

dataset.visible_columns["detailed"] = [
    ['isa', 'dataset_RID_key'],
    'accession',
    'description',
    'study_design',
    ['isa', 'dataset_project_fkey'],
    ['isa', 'dataset_status_fkey'],
    'funding',
    'release_date',
    'show_in_jbrowse',
    ['isa', 'publication_dataset_fkey'],
    ['isa', 'dataset_experiment_type_dataset_id_fkey'],
    ['isa', 'dataset_data_type_dataset_id_fkey'],
    ['isa', 'dataset_phenotype_dataset_fkey'],
    ['isa', 'dataset_organism_dataset_id_fkey'],
    ['isa', 'dataset_anatomy_dataset_id_fkey'],
    ['isa', 'dataset_gender_dataset_id_fkey'],
    ['isa', 'dataset_instrument_dataset_id_fkey']]

dataset.apply(catalog)
