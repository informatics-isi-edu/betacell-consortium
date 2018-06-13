%load_ext autoreload
%autoreload 2

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import em.builtin_types as typ
import csv
import re

dataset_key='1-882P'
homo_sapiens_key = 'NCBITAXON:9606:'
frozen_key = 'commons:167:'
cell_line_keys = {
    'HEC293': 0,
    'EndoC-BH1': 1,
    'INS-1E' : 2
}

pbcserver = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(pbcserver)

catalog = ErmrestCatalog('https', pbcserver, 1, credentials=credential)

pb = catalog.getPathBuilder()
isa = pb.isa



data = {}
biosample_entities = []
with open('NCXT_April data.csv', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, dialect='excel')
    data = [row for row in reader]

# Load biosamples
for i in data:
    m = re.search('{}_([0-9]+)'.format(i['Capillary Number']), i['Filename'])
    i['Bead Position'] = m[1]
    biosample_entities.append({
        'dataset':  dataset_key,
        'local_identifier': 'C{}-{}'.format(i['Capillary Number'], i['Bead Position']) ,
        'species': homo_sapiens_key,
        'specimen': frozen_key,
        'cell_line': cell_line_keys[i['Cell Line']],
        'collection_date': '2018-04-01'
    })

#load replicates
    replicate_entities.append({
        'experiment': 'abc'
        'biosample' : 'abc'
        'bioreplicate_number' = 1,
        'technical_replicate_number' = 1
    })
# load experiments
dataset_key
    local_id
    experiment_type
    protocol