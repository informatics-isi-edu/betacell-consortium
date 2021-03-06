from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

import __main__

# experiment_dp, biosample_dp, protocol_dp, replicate_dp, xray_tomography_dp, specimen_dp, model_dp, dataset_dp
# experiment, biosample, dataset, protocol, replicate, imaging_data, model

def init_variables(catalog_num=1):
    server = 'pbcconsortium.isrd.isi.edu'
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_num, credentials=credential)
    model_root = catalog.getCatalogModel()

    __main__.catalog = catalog
    __main__.model_root = model_root

    # Get references to main tables for manipulating the model.
    __main__.Experiment = model_root.table('Beta_Cell', 'Experiment')
    __main__.Specimen = model_root.table('Beta_Cell','Specimen')
    __main__.Biosample = model_root.table('Beta_Cell', 'Biosample')
    __main__.Dataset = model_root.table('Beta_Cell', 'Dataset')
    __main__.imaging_data = model_root.table('isa', 'imaging_data')
    __main__.model = model_root.table("viz", 'model')

    # Get references to the main tables for managing their contents using DataPath library
    pb = catalog.getPathBuilder()
    # Get main schema
    isa = pb.isa
    viz = pb.viz
    vocab = pb.vocab
    Beta_Cell = pb.Beta_Cell

    __main__.pb = pb
    __main__.isa = isa
    __main__.vocab = vocab

    # Get tables....
    __main__.Experiment_dp = Beta_Cell.Experiment
    __main__.Biosample_dp = Beta_Cell.Biosample
    __main__.dataset_dp = Beta_Cell.Dataset
    __main__.XRay_Tomography_dp = Beta_Cell.XRay_Tomography_Data
    __main__.Specimen_dp = Beta_Cell.Specimen
    __main__.model_dp = viz.model
