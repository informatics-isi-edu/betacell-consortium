import os.path
import rdflib

g = rdflib.Graph()
result = g.parse("uniprot.rdf")



qres = g.query("""
PREFIX  up_core:<http://purl.uniprot.org/core/>
PREFIX uniprot:<http://purl.uniprot,org/uniprot>
SELECT  ?protein ?mnemonic ?name ?shortname
where {
?protein a up_core:Protein . 
?protein up_core:mnemonic ?mnemonic . 
{
 ?protein up_core:recommendedName ?id2 . 
 ?id2 up_core:fullName ?name .
# OPTIONAL { ?id2 up_core:shortName ?shortname  }
 }
UNION 
{ ?protein up_core:submittedName ?id3 . 
?id3 up_core:fullName ?name  .
#OPTIONAL {?id3 up_core:shortName ?shortname }
}
}
""")


qres = g.query("""
PREFIX  up_core:<http://purl.uniprot.org/core/>
PREFIX uniprot:<http://purl.uniprot,org/uniprot>
SELECT  ?protein ?name ?shortname ?mnemonic
where {
    ?protein up_core:recommendedName ?id2  .
    ?protein a up_core:Protein .
    ?protein up_core:mnemonic ?mnemonic .
    ?id2 up_core:fullName ?name .
    ?id2 up_core:shortName ?shortname
}
""")

for row in qres:
    print(row['protein'].toPython(), row['name'].toPython(), row['shortname'].toPython(), row['mnemonic'].toPython())


#    print (row['id'].toPython(), row['name'].toPython(), row['synonym'].toPython(), row['description'].toPython())


def make_term_dict():
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

