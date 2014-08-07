#!/usr/bin/python3

import urllib.request
from xml.dom import minidom
from regions_wp import load_region_urls

def download_url(url):

	print("Downloading", url)
	httpfile = urllib.request.urlopen(url)
	xmldoc = minidom.parse(httpfile)
	links = xmldoc.getElementsByTagName('a')
	hrefs = [l.attributes['href'].value
		 for l in links if 'href' in l.attributes.keys()]
	hrefs = [h for h in hrefs if
		 h.endswith(".svg") and
		 h.startswith("//upload.wikimedia.org/wikipedia/commons/") and
		 h.find("/archive/") == -1]
	if not hrefs:
		raise Exception("Failed extracting SVG url from page.")
	svgurl = hrefs[0]
	for alturl in hrefs[1:]:
		assert alturl == svgurl
	svgurl = "https:" + svgurl

	print("Downloading", svgurl)
	svg = urllib.request.urlopen(svgurl).read()
	import pprint
	pprint.pprint(svgurl)

if __name__ == '__main__':
	urls = load_region_urls()
	keys = sorted(urls.keys())
	for k in keys:
		url = urls[k]
		download_url(url)
