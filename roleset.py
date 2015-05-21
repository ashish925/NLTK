from nltk.corpus import propbank
turn_01 = propbank.roleset('turn.01')
for role in turn_01.findall("roles/role"):
	print(role.attrib['n'], role.attrib['descr'])