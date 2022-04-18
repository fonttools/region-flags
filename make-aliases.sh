#!/usr/bin/env sh

mkdir -p html svg png
IFS='	'
while read dst src; do
  for dir in html svg png; do
    if [[ $dst == *[*]* ]]; then
      python3 ./subregion.py "$dst" | while read line ; do
        s="$dir/$src.$dir"
        d="$dir/$line.$dir"
        if test -f "$d"; then
          echo "ERROR: $d exist; skipping"
          continue
        fi
        cp -f "$s" "$d"
      done
    else
      s="$dir/$src.$dir"
      d="$dir/$dst.$dir"
      if test -f "$d"; then
        echo "ERROR: $d exist; skipping"
        continue
      fi
      cp -f "$s" "$d"
    fi
  done
done < data/ALIASES
