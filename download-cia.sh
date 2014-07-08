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
	gif="$iso2.gif"
	png="$iso2.png"

	test -s "$png" && continue
	rm -f "$gif" "$png"

	echo "Downloading:	$iso2	$country ($gec; $cctld)"

	if wget -q -O "$gif.partial" "$url"; then
		mv "$gif.partial" "$gif"
	else
		rm -f "$gif.partial"
		echo "ERROR: Download failed.  Investigate."
		continue
	fi

	echo "Converting from GIF to PNG and optimizing PNG"
	if convert "$gif" "$png" && optipng -quiet "$png"; then
		rm -f "$gif"
	else
		rm -f "$gif" "$png"
		echo "ERROR: convert or optipng failed.  Investigate."
		continue
	fi

done < appendix-d.txt
