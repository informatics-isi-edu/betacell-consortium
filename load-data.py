%load_ext autoreload
%autoreload 2

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import csv
import re

# Read in the CSV File....
data = {}
biosample_entities = []
with open('NCXT_April data.csv', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel')
    data = [row for row in reader]


pbcserver = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(pbcserver)
catalog = ErmrestCatalog('https', pbcserver, 1, credentials=credential)

pb = catalog.getPathBuilder()
isa_dp = pb.isa
experiment_dp = isa_dp.experiment
biosample_dp = isa_dp.biosample
dataset_dp = isa_dp.dataset
protocol_dp = isa_dp.protocol
replicate_dp = isa_dp.replicate

dataset_key ='1-882P'
homo_sapiens_key = 'NCBITAXON:9606:'
frozen_key = 'commons:167:'
xray_tomography = 'commons:598:'
cell_line_keys = {
    'HEK293': 'commons:595:',
    'EndoC-BH1': 'commons:596:',
    'INS-1E' : 'commons:597:'
}


# Load biosamples
biosample_entities = []
replicates = {}
protocols = {}
experiments = {}
for i in data:
    m = re.search('{}_([0-9]+)'.format(i['Capillary Number']), i['Filename'])
    i['Bead Position'] = m[1]

    pr =  {'treatment': i['Treatment Type'],
           'treatment_concentration': i['Treatment Volume (mM)'],
           'timepoint' : i['Timepoint (minutes)']}
    pr['name'] = '{}-{}-{}'.format(pr['treatment'],pr['treatment_concentration'], pr['timepoint'])
    experiment_name = '{}-{}'.format(i['Cell Line'],pr['name'])
    biosample_name = 'C{}-{}'.format(i['Capillary Number'], i['Bead Position'])

    if pr['treatment'] == 'None':
        pr['description'] = 'No treatment for {} minutes'.format(pr['timepoint'])
    else:
    pr['description'] = \
        "{} at {} mM concentration for {} minutes".format(pr['treatment'], pr['treatment_concentration'], pr['timepoint'])
    protocols[pr['name']] = pr

    experiments['{}-{}'.format(i['Cell Line'],pr['name']) ] = {'protocol' : pr['name']}
    biosample_entities.append({
        'dataset':  dataset_key,
        'local_identifier': 'C{}-{}'.format(i['Capillary Number'], i['Bead Position']) ,
        'species': homo_sapiens_key,
        'specimen': frozen_key,
        'strain': cell_line_keys[i['Cell Line']],
        'capillary_number': i['Capillary Number'],
        'sample_position': i['Bead Position'],
        'collection_date': '2018-04-01'
    })
    replicates[experiment_name] = replicates.get(experiment_name, []) + [biosample_name]

for i in biosample_entities:
    existing_sample = biosample_dp.filter(biosample_dp.local_identifier == i['local_identifier']).entities()
    if len(existing_sample) == 1:
        i['RID'] = existing_sample[0]['RID']
        print('Updating exsiting biosample', i['local_identifier'])
        biosample_dp.update([i])
    else:
        print('Inserting exsiting biosample', i)
        biosample.insert([i])

# load protocols
for k,v in protocols.items():
    print(v['name'])
    existing_protocol = protocol_dp.filter(protocol_dp.column_definitions['name'] == v['name']).entities()
    if len(existing_protocol) == 1:
        v['RID'] = existing_protocol[0]['RID']
        print('Updating exsiting protocol', v['name'])
        protocol_dp.update([v])
    else:
        print('Inserting exsiting protocol', v)
        protocol_dp.insert([v])

# Load experiments.....
for k,v in experiments.items():
    exp = {}
    exp['experiment_type'] = xray_tomography
    exp['protocol'] = protocol_dp.filter(protocol_dp.column_definitions['name'] == v['protocol']).entities()[0]['RID']
    exp['dataset']  = dataset_key
    exp['local_identifier'] = k
    existing_experiment = experiment_dp.filter(experiment_dp.column_definitions['local_identifier'] == exp['local_identifier']).entities()
    if len(existing_experiment) == 1:
        exp['RID'] = existing_experiment[0]['RID']
        print('Updating exsiting experiment', exp['local_identifier'])
        experiment_dp.update([exp])
    else:
        print('Inserting new experiment', exp['local_identifier'])
        experiment_dp.insert([exp])


#load replicates
for k,v in replicates.items():
    for i,biosample in enumerate(v):
        rep = {'dataset': dataset_key, 'technical_replicate_number':1, 'bioreplicate_number': i+1}
        rep['experiment'] = experiment_dp.filter(experiment_dp.local_identifier == k).entities()[0]['RID']
        rep['biosample'] = biosample_dp.filter(biosample_dp.local_identifier == biosample).entities()[0]['RID']
        existing_rep = replicate_dp.filter((replicate_dp.biosample == rep['biosample']) &
                                           (replicate_dp.experiment == rep['experiment'])).entities()
        if len(existing_rep) >= 1:
            rep['RID'] = existing_rep[0]['RID']
            print('Updating exsiting experiment', rep['RID'])
            replicate_dp.update([rep])
        else:
            print('Inserting new replicate {}/{}'.format(rep['experiment'],rep['biosample']))
            replicate_dp.insert([rep])

