import os.path
import rdflib

g = rdflib.Graph()
result = g.parse("locations-all.rdf")

qres = g.query("""
SELECT  ?id ?name ?synonym ?description
where {
?id rdfs:comment ?description .
?id skos:altLabel ?synonym .
?id skos:prefLabel ?name .}
""")

term_dict = {}
for row in qres:
    name = row['name'].toPython()
    if name not in term_dict:
        term_dict[name] = {
            'id': 'UNIPROT:{}'.format(os.path.basename(row['id'])),
            'uri': row['id'].toPython(),
            'description': row['description'].toPython(),
            'name': name,
            'synonyms': [row['synonym'].toPython()]
        }
    else:
        term_dict[name]['synonyms'].append(row['synonym'].toPython())


# Now flatten dictionary out to an entity list
term_list = [ v for k,v in term_dict.items()]

def add_terms(catalog, term_table, term_list):
    pb = catalog.getPathBuilder()
    # Get main schema
    vocab_dp = pb.vocab
    # Get the term table....
    species_terms_dp = vocab_dp.term_table
    # Now add the terms....
    species_terms_dp.insert(term_list)

