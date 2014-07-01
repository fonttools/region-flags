#!/bin/sh
IFS='	'
while read country gec && read iso2 iso3 junk && read junk cctld junk ; do
	test "x$iso2$gec" = x-- && continue
	if test "x$iso2" = x-; then
		#echo "No ISO 3166-2 code for $country ($gec); skipping."
		continue
	fi
	if test "x$gec" = x-; then
		#echo "No GEC code for $iso2 $cctld; skipping."
		continue
	fi

	url="https://www.cia.gov/library/publications/the-world-factbook/graphics/flags/large/`echo $gec | tr A-Z a-z`-lgflag.gif"
	out="$iso2.gif"

	test -s "$out" && continue
	test -f "$out" && rm -f "$out"

	echo "Downloading:	$iso2	$country ($gec; $cctld)"

	if wget -q -O "$out.partial" "$url"; then
		mv "$out.partial" "$out"
	else
		rm -f "$out.partial"
		echo "ERROR: Download failed.  Investigate."
	fi

done < appendix-d.txt
