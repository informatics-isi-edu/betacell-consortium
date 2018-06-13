%load_ext autoreload
%autoreload 2

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import csv
import re

def delete_column(catalog,table,col_def):
    # delete column from the table
    # Remove column from visible columns list if it was there
    return

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