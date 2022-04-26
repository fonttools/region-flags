#!/usr/bin/env python3

import sys
from regions import load_regions, load_subregions, load_aliases
from urllib.parse import quote
import urllib.request
import json

def load_region_wp_urls(region_keys_names):
    aliases_wp = load_aliases("data/ALIASES-WP")
    urls = {}

    for region_key, region_name in region_keys_names.items():

        # Apply Wikipedia-specific mappings
        region_name = aliases_wp.get(region_key, aliases_wp.get(region_name, region_name))
        region_name = region_name.replace(' ', '_')
        urls[region_key] = "https://commons.wikimedia.org/wiki/File:Flag_of_%s.svg" % region_name

    return urls


def load_region_key_names():

    aliases = load_aliases("data/ALIASES")
    regions = load_regions()
    regions.update(load_subregions())

    region_keys_names = {}
    region_keys = sorted(regions.keys())

    for k in region_keys:

        # If this uses another flag, skip
        if k in aliases:
            continue

        if 'Description' in regions[k].keys():
            region_keys_names[k] = regions[k]['Description']
        else:
            region_keys_names[k] = regions[k]['Subdivision name']

    return region_keys_names

# The below code is responsible for translating Wikimedia Commons
# description page URIs to the direct URI of the image

# Prefix of Wikimedia Commons URIs to translate
W_PREFIX = 'https://commons.wikimedia.org/wiki/File:'
# API endpoint to get direct URI
W_API = 'https://commonsapi.toolforge.org/?format=json&image='
# Number of images to translate at once
W_DOWNLOAD_CHUNK_SIZE = 3

# Copied from https://stackoverflow.com/a/312464/
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def find_wp_direct_links(urls):
    for k in urls.keys():
        urls[k] = quote(urls[k][len(W_PREFIX):])
    translated = {}
    wp_urls = list(urls.values())
    for chunk in chunks(wp_urls,W_DOWNLOAD_CHUNK_SIZE):
        query_url = W_API + "|".join(chunk)
        #print("GET %s" % query_url, file=sys.stderr)
        with urllib.request.urlopen(query_url) as f:
            response = json.loads(f.read().decode('utf-8'))
            images = response["image"] if "image" in response else [response]
            for image in images:
                if not "image" in image:
                    image["name"] = image["file"]["title"][len("File:"):]
                translated[quote(image["name"])] = image["file"]["urls"]["file"]
    for k in urls.keys():
        if urls[k] in translated:
            urls[k] = translated[urls[k]]
    return urls


if __name__ == '__main__':
    REGION_URLS = load_region_wp_urls(load_region_key_names())
    SORTED_KEYS = sorted(REGION_URLS.keys())

    if "-d" in sys.argv:
        REGION_URLS = find_wp_direct_links(REGION_URLS)

    for key in SORTED_KEYS:
        print("%s    %s" % (key, REGION_URLS[key]))
