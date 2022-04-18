#!/usr/bin/env sh

IFS='    '

wget -q -O "data/language-subtag-registry" "https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry"

# shellcheck disable=SC2162
python3 -c 'exec("""\nfrom regions import load_regions\nregions = sorted(load_regions().keys())\nfor k in regions:\n    print(k)\n""")' | while read line ; do
   # shellcheck disable=SC2039
   python3 ./regions-iso.py "$line" > tsv/iso-3166-2-"${line,,}".tsv
done
find tsv -empty -delete
