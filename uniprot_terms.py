import os.path
import rdflib

g = rdflib.Graph()
result = g.parse("uniprot.rdf")

qres = g.query("""
PREFIX  up_core:<http://purl.uniprot.org/core/>
PREFIX uniprot:<http://purl.uniprot,org/uniprot>
SELECT  ?protein ?mnemonic ?name ?alternative_name ?shortname ?sub_name ?function
where {
 ?protein a up_core:Protein . 
 ?protein up_core:mnemonic ?mnemonic . 
 OPTIONAL { ?protein up_core:recommendedName ?id2 . 
            ?id2 up_core:fullName ?name } .
 OPTIONAL { ?protein up_core:submittedName ?sn .
            ?sn up_core:fullName ?sub_name } .
 OPTIONAL { ?protein up_core:annotation ?a .
        	?a a up_core:Function_Annotation .
            ?a rdfs:comment ?function
 } .
 OPTIONAL {?protein up_core:alternativeName ?n1 .
        ?n1 up_core:fullName ?alternative_name
 } .
 OPTIONAL {?protein up_core:recommendedName ?rn .
           ?rn up_core:shortName ?shortname }
 }
""")
 
id_list = list(qres)

# qres = g.query("""
# PREFIX  up_core:<http://purl.uniprot.org/core/>
# PREFIX uniprot:<http://purl.uniprot,org/uniprot>
# SELECT  ?protein ?mnemonic ?alternative?altname ?altshortname
# where {
# ?protein a up_core:Protein .
# ?protein up_core:mnemonic ?mnemonic .
#  ?protein up_core:submittedName ?id2 .
#  ?id2 up_core:fullName ?altname .
#   OPTIONAL {?id2 up_core:shortName ?altshortname } .
#    OPTIONAL { ?protein up_core:annotation ?a .
#         	?a a up_core:Function_Annotation .
#             ?a rdfs:comment ?function
# }
#  }
# """)

#id_list.extend(list(qres))

uniprot_entries = {}
for i in id_list:
    id =  os.path.basename(i['protein'])
    if id not in uniprot_entries:
        entry = uniprot_entries[id] = {
            'id' : id,
            'url': i['protein'].toPython(),
        }

    if 'name' in i.labels and i['name']:
        if i['name'].toPython() == entry.get('name', i['name'].toPython()):
            entry['name'] = i['name'].toPython()
        else:
            print("Multiple names for id {}: {} and {}".format(id, i['name'].toPython(), entry['name']))
    if 'alternative_name' in i.labels and i['alternative_name']:
        print('adding alternative name', i['alternative_name'])
        entry['alternative_name'] = entry.get('alternative_name',set())
        entry['alternative_name'].add(i['alternative_name'].toPython())
        print(entry['alternative_name'])
    if 'sub_name' in i.labels and i['sub_name']:
        entry['sub_name'] = entry.get('sub_name',set())
        entry['sub_name'].add(i['sub_name'].toPython())
    if 'mnemonic' in i.labels:
        if i['mnemonic'].toPython() == entry.get('mnemonic', i['mnemonic'].toPython()):
            entry['mnemonic'] = i['mnemonic'].toPython()
        else:
            print("Multiple mnemonics for id {}: {} and {}".format(id, i['mnemonic'].toPython(), entry['mnemonic']))
    if 'function' in i.labels and i['function']:
        if i['function'].toPython() == entry.get('function', i['function'].toPython()):
            entry['function'] = i['function'].toPython()
        else:
            print("Multiple mnemonics for id {}: {} and {}".format(id, i['mnemonic'].toPython(), entry['mnemonic']))
    if 'shortname' in i.labels and i['shortname']:
        entry['shortname'] = entry.get('shortname',set())
        entry['shortname'].add(i['shortname'].toPython())

term_list = []
for k,v  in uniprot_entries.items():
    term = {'id' : 'UNIPROT:{}'.format(v['id']),
            'uri' : v['url'],
            'synonyms' : [v['mnemonic']]}
    if 'name' in v:
        term['name'] = v['name']
    elif 'sub_name' in v and len(v['sub_name']) > 0:
        term['name'] = v['sub_name'].pop()
    else:
        print('name missing', v)
    if 'function' in v:
        term['description'] = v['function']
    if 'alternative_name' in v:
        term['synonyms'].extend(v['alternative_name'])
    if 'sub_name' in v:
        term['synonyms'].extend(v['sub_name'])
    term_list.append(term)

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

