from deriva.core import HatracStore, ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import pprint
import re

server = 'pbcconsortium.isrd.isi.edu'
term_table = 'foobar_terms'
term_comment = 'Here you go'

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


