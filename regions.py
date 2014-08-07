#!/usr/bin/python3


def load_aliases(filename):
	return dict([[x.strip() for x in line.split('	')]
		    for line in open(filename)])

def load_entries(filename):
	entries = []
	entry = {}
	f = open(filename, encoding='utf-8')
	f.readline ()
	f.readline ()
	for line in f:
		if line.startswith('%%'):
			entries.append(entry)
			entry = {}
			continue
		if line.startswith('  '):
			# Continuation
			entry[fields[0]] += ' ' + line.strip()
			continue
		fields = [x.strip() for x in line.split(':')]
		entry[fields[0]] = fields[1]
	entries.append(entry)
	return entries

def load_regions():

	entries = load_entries("language-subtag-registry") + load_entries("language-subtag-private")

	regions = [e for e in entries if
			e['Type'] == 'region' and
			len(e['Subtag']) == 2 and
			e['Description'] != 'Private use' and
			'Deprecated' not in e]

	regions = {e['Subtag']:e for e in regions}
	for r in regions.values():
		del r['Type']
		del r['Subtag']

	return regions

if __name__ == '__main__':
	regions = load_regions()
	keys = sorted(regions.keys())
	for k in keys:
		print("%s	%s" % (k, regions[k]))
