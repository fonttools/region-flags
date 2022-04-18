#!/usr/bin/env python3

import re
import glob
import unicodedata


def load_aliases(filename):
    aliases = []
    for line in open(filename, encoding='utf-8'):
        if line.__contains__("*"):
            line_content = line.split('\t')
            for i in load_subregion_codes(line_content[0].removesuffix("*")):
                aliases.append(f"{i}\t{line_content[1]}")
        else:
            aliases.append(line)

    return dict([
        [x.strip() for x in line.split('\t')]
        for line in aliases
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
        'Local variant',
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

    region_codes = []
    for i in glob.glob("tsv/*.tsv"):
        region_code = i.removeprefix("tsv/iso-3166-2-").removesuffix(".tsv")
        match region_code:
            case "bq":
                region_codes.append([region_code, "en"])
            case "ca":
                region_codes.append([region_code, "en"])
            case "et":
                region_codes.append([region_code, "en"])
            case "fi":
                region_codes.append([region_code, "fi"])
            case _:
                region_codes.append(region_code)

    for i in region_codes:
        filename = 'tsv/iso-3166-2-%s.tsv' % i
        match i:
            case "ae":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(e['Local variant']),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "ar":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title("File:Bandera de la Provincia de " + e['Subdivision name']),
                    }
                    for e in load_subregion_entries(filename)
                    if e['Language code'] == 'es'
                })
            case "br":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title("File:Bandeira do " + e['Subdivision name']),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "ch":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title("Canton of " + e['Subdivision name']),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "cl":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': strip_accents(e['Subdivision name']) + ", Chile",
                    }
                    for e in load_subregion_entries(filename)
                })
            case "cr":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title("File:Bandera de la Provincia de " + e['Subdivision name']),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "dk":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title("Region " + e['Subdivision name']),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "ec":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title("File:Bandera Provincia " + e['Subdivision name']),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "ee":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(f"File:{e['Subdivision name']} lipp" if e[
                                                                                                   'Subdivision category'] == "county" else f"File:{e['Subdivision name']} valla lipp"),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "fr":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(f"File:Drapeau fr département {e['Subdivision name']}" if e[
                                                                                                                     'Subdivision category'] == "metropolitan department" else
                                                       e['Subdivision name']),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "ge":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(strip_brackets(e['Subdivision name'])),
                    }
                    for e in load_subregion_entries(filename)
                    if e['Subdivision category'] not in ['region']
                })
                """
            case "gb":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(strip_brackets(e['Subdivision name'])),
                    }
                    for e in load_subregion_entries(filename)
                    if e['Subdivision category'] in ['country', 'province']
                })
                """
            case "jp":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(e['Subdivision name'] + " Prefecture"),
                    }
                    for e in load_subregion_entries(filename)
                })
            case "kr":
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(e['Subdivision name'].split("-")[0]),
                    }
                    for e in load_subregion_entries(filename)
                })
            case [_, _]:
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(strip_brackets(e['Subdivision name'])),
                    }
                    for e in load_subregion_entries('tsv/iso-3166-2-%s.tsv' % i[0])
                    if e['Language code'] == i[1]
                })
            case _:
                subregions.update({
                    e['3166-2 code'].rstrip("*"): {
                        'Subdivision name': full_title(strip_brackets(e['Subdivision name'])),
                    }
                    for e in load_subregion_entries(filename)
                    if not e['Subdivision name'].endswith('*')
                })

    return subregions


def load_subregion_codes(region):
    subregions = {}
    region_code = region.split("-")[0].lower()
    subregions.update({
        e['3166-2 code'].rstrip("*"): {
            'Subdivision name': e['Local variant'],
        }
        for e in load_subregion_entries('tsv/iso-3166-2-%s.tsv' % region_code)
    })

    subregions_codes = []
    subregions_keys = sorted(subregions.keys())
    for i in subregions_keys:
        if i.startswith(region) and i != region:
            subregions_codes.append(i)

    return subregions_codes


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
