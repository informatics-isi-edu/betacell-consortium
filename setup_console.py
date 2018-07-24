from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

# Create connection to the PBC server
def init_varibles():
    server = 'pbcconsortium.isrd.isi.edu'
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()

    # Get references to main tables for manipulating the model.
    experiment = model_root.table('isa', 'experiment')
    biosample = model_root.table('isa', 'biosample')
    dataset = model_root.table('isa', 'dataset')
    protocol = model_root.table('isa','protocol')
    replicate = model_root.table('isa','replicate')
    imaging_data = model_root.table('isa','imaging_data')
    model = model_root.table("viz", 'model')


    # Get references to the main tables for managing their contents using DataPath library
    pb = catalog.getPathBuilder()
    # Get main schema
    isa = pb.isa
    viz = pb.viz

    # Get tables....
    experiment_dp = isa.experiment
    biosample_dp = isa.biosample
    dataset_dp = isa.dataset
    protocol_dp = isa.protocol
    replicate_dp = isa.replicate
    xray_tomography_dp = isa.xray_tomography_data
    specimen_dp = isa.specimen
    model_dp = viz.model
