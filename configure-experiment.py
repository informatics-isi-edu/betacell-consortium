%load_ext autoreload
%autoreload 2

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
protocol = model_root.table('isa','protocol')
replicate = model_root.table('isa','replicate')
imaging_data = model_root.table('isa','imaging_data')

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

experiment.apply(catalog)