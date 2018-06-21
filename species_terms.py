from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import re


requests.exceptions.HTTPError: 409 Client Error: Conflict for url: https://pbcconsortium.isrd.isi.edu/ermrest/catalog/1/schema/vocab/table/species_terms details: \

    b'constraint clinical_assay_species_fkey on table isa.clinical_assay depends on table vocab.species_terms\nconstraint dataset_organism_organism_fkey on ' \
    b'table isa.dataset_organism depends on table vocab.species_terms\nconstraint ' \
    b'sample_species_fkey on table isa.sample depends on table vocab.species_terms\
    constraint species_paths_object_dbxref_fkey on table vocab.species_paths depends on table vocab.species_terms
    constraint species_paths_subject_dbxref_fkey on table vocab.species_paths depends on table vocab.species_terms
    b'se DROP ... CASCADE to drop the dependent objects too.\n\n'

server = 'pbcconsortium.isrd.isi.edu'

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()

schema = model_root.schemas['vocab']

new_vocab_table = schema.create_table(catalog,
    em.Table.define_vocabulary('species_terms','PBCCONSORTIUM:{RID}',comment='Terms for species')
)

cell_line_vocab_table = schema.create_table(catalog,
    em.Table.define_vocabulary('cell_line_terms','PBCCONSORTIUM:{RID}',comment='Terms for cell lines')
)

treatment_vocab_table = schema.create_table(catalog,
    em.Table.define_vocabulary('treatment_terms','PBCCONSORTIUM:{RID}',comment='Terms for treatments')
)

anatomy_vocab_table = schema.create_table(catalog,
    em.Table.define_vocabulary('anatomy_terms','PBCCONSORTIUM:{RID}',comment='Terms for anatomy')
)

experiment_type_vocab_table = schema.create_table(catalog,
    em.Table.define_vocabulary('experiment_type_terms','PBCCONSORTIUM:{RID}',comment='Terms for experiment types')
)


species_list = [
    {'id': 'NCBITAXON:9606',
     'uri': 'http://purl.bioontology.org/ontology/NCBITAXON/9606',
     'name': 'Homo Sapiens',
    'synonyms': ["man"],
     'description': 'NCBI Taxon for man.'},
    {'id': 'NCBITAXON:10116',
     'uri': 'http://purl.bioontology.org/ontology/NCBITAXON/10116',
     'name': 'Rattus norvegicus',
     'synonyms': ["brown rat"],
     'description' : 'NCBI Taxon for rat'
     }
]

cell_line_list = [
    { 'id': 'CVCL_L909',
     'name' : 'EndoC-betaH1',
     'uri' :'https://web.expasy.org/cellosaurus/CVCL_L909',
     'synonyms': ['EndoC-BH1'],
    'description' :'Human Betacell'
     },
    {'name' : 'HEC293',
    'uri' : '/id/{RID}', 'id' : 'PBCCONSORTIUM:{RID}',
    'description' : 'Human embryonic kidney',
    'synonyms' : ['HEK-293']
     },
    {'name' : 'INS-1E',
     'id': 'RRID:CVCL_0351',
     'uri' : 'http://purl.obolibrary.org/obo/BCGO_0000120',
    'synonyms' : ['INS1-E', 'INS1E'],
    'description' :'An INS-1 cell which has high insulin secretion in responses to glucose.'
     }
]

treatment_list = [
    { 'name' : 'glucose',
      'id' : 'CHEBI:17234',
      'uri': 'http://purl.obolibrary.org/obo/chebi#3_STAR',
        'synonyms' : ['DL-glucose','glucose','Glc','Glukose','Glucose','gluco-hexose'],
      'description' : 'An aldohexose used as a source of energy and metabolic intermediate.'
    }
]

specimen_type_list = [
    {'name': 'chemically fixed tissue', 'id': 'FBbi:00000002',
     'uri': 'http://purl.obolibrary.org/obo/FBbi_00000002',
     'description': ''},
    {'name': 'cryostat sectioned tissue', 'id': 'FBbi:00000027',
     'uri': 'http://purl.obolibrary.org/obo/FBbi_00000027',
     'description': ''},
    {'name': 'fresh specimen', 'id': 'OBI:0000971',
     'uri': 'http://purl.obolibrary.org/obo/OBI_0000971',
     'description': ''
     },
    {'name': 'frozen specimen', 'id': 'OBI:0000922',
     'uri': 'URL:http://purl.obolibrary.org/obo/OBI_0000922',
     'description': ''
     },
    {'name': 'sectioned tissue', 'id': 'FBbi:00000026',
     'uri': 'http://purl.obolibrary.org/obo/FBbi_00000026',
     'description': ''
     },
    {'name': 'Single cell specimen', 'id': 'OBI:0002127',
     'uri': 'http://purl.obolibrary.org/obo/OBI_0002127',
     'description': ''
     },
    {'name': 'tissue specimen', 'id': 'OBI:000147',
     'uri': 'http://purl.obolibrary.org/obo/OBI_0001479',
     'description': ''},
    {'name': 'whole mount tissue', 'id': 'OBI_1000049',
     'uri': "http://purl.obolibrary.org/obo/OBI_1000049",
     'description': ''
     },
    {'name': 'whole organism preparation', 'id': 'OBI:0000680',
     'uri': "http://purl.obolibrary.org/obo/OBI_0000680",
            'description': ''
     }
]

experiment_type_list = [
    {
    'name': 'microcomputed tomography',
    'synonyms': ['micro-CT', 'X-ray microtomography', 'high-resolution x-ray tomography', 'high-resolution computed tomography'],
    'id': 'MMO:0000570',
    'uri' : 'http://purl.obolibrary.org/obo/MMO_0000570',
    'description': 'High-resolution computed tomography in which the pixel sizes of the cross-sections are in the micrometer range.'
    }
]

experiment_type_list
http: // purl.obolibrary.org / obo / OBI_0000982
Definition: An image acquisition device that generates a three-dimensional image of the inside of an object from a large series of two-dimensional X-ray images taken around a single axis of rotation.
X-ray computed tomography scanner; CT scanner
pb = catalog.getPathBuilder()
# Get main schema
vocab_dp = pb.vocab

species_terms_dp = vocab_dp.species_terms
species_terms_dp.insert(species_list)

cell_line_terms_dp = vocab_dp.cell_line_terms
cell_line_terms_dp.insert(cell_line_list)

treatment_terms_dp = vocab_dp.treatment_terms
treatment_terms_dp.insert(treatment_list)

specimen_type_terms = vocab_dp.specimen_type_terms
specimen_type_terms_dp.insert(specimen_type_list)

experiment_type_terms_dp = vocab_dp.experiment_type_terms
experiment_type_terms_dp.insert(experiment_type_list)

for i in specimen_dp.entities(specimen_type_terms.RID):


def map_column(map,table,column):
    '1 - 956Y'