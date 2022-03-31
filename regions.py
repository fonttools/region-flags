#!/usr/bin/env python3

import re
import unicodedata


def load_aliases(filename):
    return dict([
        [x.strip() for x in line.split('\t')]
        for line in open(filename, encoding='utf-8')
    ])


def load_region_entries(filename):
    entries = []
    entry = {}
    fields = []

    region_file_obj = open(filename, encoding='utf-8')
    region_file_obj.readline()
    region_file_obj.readline()

    for line in region_file_obj:
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
    entries = []
    entries.extend(load_region_entries('data/language-subtag-registry'))
    entries.extend(load_region_entries('data/language-subtag-private'))

    regions = {
        e['Subtag']: e
        for e in entries
        if e['Type'] == 'region'
        and len(e['Subtag']) == 2
        and e['Description'] != 'Private use'
        and 'Deprecated' not in e
    }

    for r_val_key in regions.values():
        del r_val_key['Type']
        del r_val_key['Subtag']

    return regions


def strip_accents(s):
    return ''.join(c
        for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def full_title(s):
    parts = s.split(", ")
    return " ".join(parts[::-1])


def strip_brackets(s):
    return re.sub(r' \[.*\]', '', s)


def load_subregion_entries(filename):
    entries = []
    subregions_file_obj = open(filename, encoding='utf-8')
    schema = [
        'Subdivision category',
        '3166-2 code',
        'Subdivision name',
        'Language code',
        'Romanization system',
        'Parent subdivision',
    ]
    for line in subregions_file_obj:
        if line.startswith(';') == False:
            fields = [x for x in line.strip('\n').split('\t')]
            entries.append({k: v for k, v in zip(schema, fields)})
    return entries


def load_subregions():
    subregions = {}

    # US: States (50) and DC
    subregions.update({
        e['3166-2 code']: {
            'Subdivision name': e['Subdivision name'],
        }
        for e in load_subregion_entries('data/iso-3166-2-us.tsv')
        if e['Language code'] == 'en'
        and e['Subdivision category'] in ['state', 'district']
    })

    # GB: Countries (3) and provinces (1)
    subregions.update({
        e['3166-2 code']: {
            'Subdivision name': strip_brackets(e['Subdivision name']),
        }
        for e in load_subregion_entries('data/iso-3166-2-gb.tsv')
        if e['Language code'] == 'en'
        and e['Subdivision category'] in ['country', 'province']
    })

    # CA: Provinces (10) and territories (3)
    subregions.update({
        e['3166-2 code']: {
            'Subdivision name': e['Subdivision name'],
        }
        for e in load_subregion_entries('data/iso-3166-2-ca.tsv')
        if e['Language code'] == 'en'
        and e['Subdivision category'] in ['province', 'territory']
    })

    # CO: departments (32) and capital districts (1)
    subregions.update({
        e['3166-2 code']: {
            'Subdivision name': e['Subdivision name'],
        }
        for e in load_subregion_entries('data/iso-3166-2-co.tsv')
        if e['Subdivision category'] in ['department', 'capital district']
    })

    # MX: States (31) and CDMX
    subregions.update({
        e['3166-2 code']: {
            'Subdivision name': strip_accents(e['Subdivision name']),
        }
        for e in load_subregion_entries('data/iso-3166-2-mx.tsv')
        if e['Language code'] == 'es'
        and e['Subdivision category'] in ['state', 'federal district']
    })

    # ES: Autonomous communities(17) and autonomous cities in North Africa (2)
    subregions.update({
        e['3166-2 code'].rstrip("*"): {
            'Subdivision name': full_title(strip_brackets(e['Subdivision name'])),
        }
        for e in load_subregion_entries('data/iso-3166-2-es.tsv')
        if e['Subdivision category'] in ['autonomous community',
                                         'autonomous city in North Africa']
        and not e['Subdivision name'].endswith('*')
    })

    # AU: States (6) and territories (2)
    subregions.update({
        e['3166-2 code']: {
            'Subdivision name': e['Subdivision name'],
        }
        for e in load_subregion_entries('data/iso-3166-2-au.tsv')
        if e['Language code'] == 'en'
        and e['Subdivision category'] in ['state', 'territory']
    })

    # DE: Lands (16)
    subregions.update({
        e['3166-2 code']: {
            'Subdivision name': e['Subdivision name'],
        }
        for e in load_subregion_entries('data/iso-3166-2-de.tsv')
        if e['Subdivision category'] in ['land']
    })

    return subregions


def load_all():
    regions = load_regions()
    keys = sorted(regions.keys())
    for k in keys:
        print('%s    %s' % (k, regions[k]))

    subregions = load_subregions()
    keys = sorted(subregions.keys())
    for k in keys:
        print('%s   %s' % (k, subregions[k]))


if __name__ == '__main__':
    load_all()
