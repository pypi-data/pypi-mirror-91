from emmo import get_ontology

emmo = get_ontology(
    'https://emmo-repo.github.io/versions/1.0.0-beta/emmo-inferred.ttl')
emmo.load()

query = f'''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?cls
    WHERE ?cls rdfs:subClassOf <{emmo.Physical.iri}> .
    '''


# print(list(emmo.world.sparql_query(query)))

g = emmo.world.as_rdflib_graph()
# print(list(g.query(query)))
