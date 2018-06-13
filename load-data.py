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
isa = pb.isa
experiment = isa.experiment
biosample = isa.biosample
dataset = isa.dataset

dataset_key='1-882P'
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
for i in data:
    m = re.search('{}_([0-9]+)'.format(i['Capillary Number']), i['Filename'])
    i['Bead Position'] = m[1]
    biosample_entities.append({
        'dataset':  dataset_key,
        'local_identifier': 'C{}-{}'.format(i['Capillary Number'], i['Bead Position']) ,
        'species': homo_sapiens_key,
        'specimen': frozen_key,
        'strain': cell_line_keys[i['Cell Line']],
        'collection_date': '2018-04-01'
    })

for i in biosample_entities:
    existing_sample = biosample.filter(biosample.local_identifier == i['local_identifier']).entities()
    if len(existing_sample) == 1:
        i['RID'] = existing_sample[0]['RID']
        print('Updating exsiting biosample', i['local_identifier'])
        biosample.update([i])
    else:
        print('Inserting exsiting biosample', i)
        biosample.insert([i])


# load experiments
experiment_entities = []
for i in data:
    m = re.search('{}_([0-9]+)'.format(i['Capillary Number']), i['Filename'])
    i['Bead Position'] = m[1]
    biosample_entities.append({
        'dataset':  dataset_key,
        'local_identifier': 'C{}-{}'.format(i['Capillary Number'], i['Bead Position']) ,
        'experiment_type': xray_tomography,
    })


dataset_key
    local_id
    experiment_type
    protocol


biosample.update(


#load replicates
    replicate_entities.append({
        'experiment': 'abc'
        'biosample' : 'abc'
        'bioreplicate_number' :1,
        'technical_replicate_number' : 1
    })
