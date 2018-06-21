from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import csv
import re

# File ment to load basic variables for interacting with PBC catalog.


# Create connection to the PBC server
server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()

#schemas

isa = model_root.schemas['isa']
viz = model_root.schemas['isa']

# Get references to main tables for manipulating the model.
experiment = model_root.table('isa', 'experiment')
biosample = model_root.table('isa', 'biosample')
dataset = model_root.table('isa', 'dataset')
protocol = model_root.table('isa','protocol')
replicate = model_root.table('isa','replicate')
imaging_data = model_root.table('isa','imaging_data')
model = model_root.table("viz", 'model')
specimen = model_root.table('isa', 'specimen')

# Get references to the main tables for managing their contents using DataPath library
pb = catalog.getPathBuilder()
# Get main schema
isa_dp = pb.isa
viz_dp = pb.viz

# Get tables....
experiment_dp = isa_dp.experiment
biosample_dp = isa_dp.biosample
dataset_dp = isa_dp.dataset
protocol_dp = isa_dp.protocol
replicate_dp = isa_dp.replicate
xray_tomography_dp = isa_dp.xray_tomography_data
specimen_dp = isa_dp.specimen
model_dp = viz_dp.model