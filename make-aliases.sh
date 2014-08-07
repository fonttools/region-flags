#!/bin/sh
mkdir -p html svg png
IFS='	'
while read from to; do

	for dir in html svg png; do
		f="$dir/$from.$dir"

		if test -f "$f"; then
			echo "ERROR: $f exist; skipping"
			continue
		fi
		ln -s "$to.$dir" "$f"

	done
done < ALIASES
