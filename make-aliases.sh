#!/usr/bin/env sh

mkdir -p html svg png
IFS='	'
while read dst src; do

	for dir in html svg png; do
		s="$dir/$src.$dir"
		d="$dir/$dst.$dir"

		if test -f "$d"; then
			echo "ERROR: $d exist; skipping"
			continue
		fi
		cp -f "$s" "$d"

	done
done < data/ALIASES
