from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import re

server = 'pbcconsortium.isrd.isi.edu'
term_table = 'foobar_terms'
term_comment = 'Here you go'

# List of terms you would like to add to this new table
term_list = [
    {'id': 'NCBITAXON:9606',
     'uri': 'http://purl.bioontology.org/ontology/NCBITAXON/9606',
     'name': 'Homo Sapiens',
     'synonyms': ["man"],
     'description': 'NCBI Taxon for man.'},
    {'id': 'NCBITAXON:10116',
     'uri': 'http://purl.bioontology.org/ontology/NCBITAXON/10116',
     'name': 'Rattus norvegicus',
     'synonyms': ["brown rat"],
     'description': 'NCBI Taxon for rat'
     }
]

credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)


def set_visible_columns(catalog, term_table):
    """
    Set visible columns so you are looking just at the ones associated with vocab (i.e. no system)
    :param catalog:
    :param term_table:
    :return:
    """
    term_visible_columns = {
        'filter': {'and': [{'source': 'name', 'open': True},
                           {'source': 'id', 'open': True},
                           {'source': 'synonyms', 'open': True}]},
        'entry': ['name', 'id', 'synonyms', 'uri', 'description'],
        'detailed': ['name', 'id', 'synonyms', 'uri', 'description'],
        'compact': ['name', 'id', 'synonyms', 'description']}

    model_root = catalog.getCatalogModel()
    for k, v in term_visible_columns.items():
        model_root.schemas['vocab'].tables[term_table].visible_columns[k] = v
    model_root.schemas['vocab'].tables[term_table].apply(catalog)


def create_vocabulary_table(catalog,term_table, term_comment):
    model_root = catalog.getCatalogModel()
    new_vocab_table = \
        model_root.schemas['vocab'].create_table(catalog, em.Table.define_vocabulary(term_table,'PBCCONSORTIUM:{RID}',comment=term_comment)
)

def add_terms(catalog, term_table, term_list):
    pb = catalog.getPathBuilder()
    # Get main schema
    vocab_dp = pb.vocab
    # Get the term table....
    terms_dp = vocab_dp.tables[term_table]
    # Now add the terms....
    terms_dp.insert(term_list)


experiment_type_terms_dp = vocab_dp.experiment_type_terms
experiment_type_terms_dp.insert(experiment_type_list)

def delete_foreign_keys(catalog,schema,table):
    model_root = catalog.getCatalogModel()
    for i in model_root.schemas['isa'].tables['specimen'].foreign_keys:
        i.delete(catalog)


