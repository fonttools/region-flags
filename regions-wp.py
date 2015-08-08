#!/usr/bin/env python3

from regions import load_regions, load_subregions, load_aliases

def load_region_wp_urls(region_keys_names):

    aliases_wp = load_aliases("data/ALIASES-WP")
    urls = {}

    for region_key, region_name in region_keys_names.items():

        # Apply Wikipedia-specific mappings
        region_name = aliases_wp.get(region_name, region_name)
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


if __name__ == '__main__':
    REGION_URLS = load_region_wp_urls(load_region_key_names())
    SORTED_KEYS = sorted(REGION_URLS.keys())

    for key in SORTED_KEYS:
        print("%s    %s" % (key, REGION_URLS[key]))
