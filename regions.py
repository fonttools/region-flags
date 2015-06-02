#!/usr/bin/env python3

def load_aliases(filename):
    return dict([[x.strip() for x in line.split('\t')]
                 for line in open(filename, encoding='utf-8')])

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

def load_subregion_entries(filename):
    entries = []
    subregions_file_obj = open(filename, encoding='utf-8')
    schema = ['Subdivision category', '3166-2 code',
              'Subdivision name', 'Language code',
              'Romanization system', 'Parent subdivision']

    for line in subregions_file_obj:
        if line.startswith(';') == False:
            fields = [x for x in line.strip('\n').split('\t')]
            entries.append({k: v for k, v in zip(schema, fields)})
    return entries

def load_regions():

    entries = []
    entries.extend(load_region_entries('data/language-subtag-registry'))
    entries.extend(load_region_entries('data/language-subtag-private'))

    regions = [e for e in entries if
               e['Type'] == 'region' and
               len(e['Subtag']) == 2 and
               e['Description'] != 'Private use' and
               'Deprecated' not in e]

    regions = {e['Subtag']:e for e in regions}
    for r_val_key in regions.values():
        del r_val_key['Type']
        del r_val_key['Subtag']

    return regions

def load_subregions():

    import re

    entries = []

    entries.extend(load_subregion_entries('data/iso-3166-2-us.tsv'))
    entries.extend(load_subregion_entries('data/iso-3166-2-gb.tsv'))

    subregions = [e for e in entries if
                  e['Subdivision category']
                  in ['province', 'country', 'state']] # US states, plus countries of GB

    subregions = {e['3166-2 code']: e for e in subregions}

    for r_val_key in subregions.values():
        del r_val_key['3166-2 code'], r_val_key['Romanization system'], r_val_key['Language code']
        r_val_key['Subdivision name'] = re.sub(r' \[.*\]', '', r_val_key['Subdivision name'])

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

