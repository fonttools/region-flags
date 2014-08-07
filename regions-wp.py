#!/usr/bin/python3

from regions import regions, load_aliases

aliases = load_aliases("ALIASES")
aliases_wp = load_aliases("ALIASES-WP")

if __name__ == '__main__':
	keys = sorted(regions.keys())
	for k in keys:

		# If this uses another flag, skip
		if k in aliases:
			continue

		s = regions[k]['Description']

		# Apply Wikipedia-specific mappings
		s = aliases_wp.get(s, s)

		s = s.replace(' ', '_')
		url = "https://commons.wikimedia.org/wiki/File:Flag_of_%s.svg" % s
		print("%s	%s" % (k, url))
