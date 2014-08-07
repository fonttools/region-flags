#!/usr/bin/python3

from regions import load_regions, load_aliases

def load_region_urls():

	aliases = load_aliases("ALIASES")
	aliases_wp = load_aliases("ALIASES-WP")
	regions = load_regions()

	keys = sorted(regions.keys())
	urls = {}
	for k in keys:

		# If this uses another flag, skip
		if k in aliases:
			continue

		s = regions[k]['Description']

		# Apply Wikipedia-specific mappings
		s = aliases_wp.get(s, s)

		s = s.replace(' ', '_')
		url = "https://commons.wikimedia.org/wiki/File:Flag_of_%s.svg" % s
		urls[k] = url
	return urls

if __name__ == '__main__':
	urls = load_region_urls()
	keys = sorted(urls.keys())
	for k in keys:
		print("%s	%s" % (k, urls[k]))
