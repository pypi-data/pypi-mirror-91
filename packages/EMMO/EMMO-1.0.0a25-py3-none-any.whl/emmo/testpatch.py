from emmo import get_ontology


emmo = get_ontology()
emmo.load()

print('*** get_parents:', emmo.Atom.get_parents)
print(emmo.Atom.get_parents())


print('*** get_preferred_label:', emmo.Atom.get_preferred_label)
print(emmo.Atom.get_preferred_label())
