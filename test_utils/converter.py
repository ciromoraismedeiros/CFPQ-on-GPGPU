"""
RDF converter from popular formats (XML, Turtle, etc.) to simple triple
format (.txt).

Usage:
- Create a conversion configuration file called 'convconfig' in the same
  directory. Each line must contain an IRI, a whitespace character and a
  string to replace the IRI.
- Run converter.py <input file>
- Result will have the same name of the input file, with .txt extension.
  The graph will contain explicit inverted edges added an 'R'.
"""

import rdflib, sys, os

if len(sys.argv) < 2:
	print('Usage: converter.py <input file>')
	exit()

replace = {} # map for replacing predicates
for l in open('convconfig','r').readlines():
	pair = l.split(' ')
	old = rdflib.URIRef(pair[0].strip(' '))
	new = pair[1].strip('\n').strip(' ')
	replace[old] = new

res = {}    # map from resources to integer ids
next_id = 1 # id counter

graph = rdflib.Graph()
graph.parse(sys.argv[1])

out = open(os.path.splitext(sys.argv[1])[0]+'.txt','w') # output file
for s,p,o in graph:
	for r in [s,o]:
		if r not in res:
			res[r] = str(next_id)
			next_id += 1
	
	if p in replace:
		out.write(res[s]+' '+replace[p]+' ' +res[o]+'\n')
		out.write(res[o]+' '+replace[p]+'R '+res[s]+'\n')
	else:
		out.write(res[s]+' OTHER '+res[o]+'\n')
	
