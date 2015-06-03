#!/usr/bin/env sh

IFS='    '
python3 ./regions-wp.py |
while read region htmlurl ; do

	html="html/$region.html"
	svg="svg/$region.svg"
	png="png/$region.png"

	test -s "$html" && continue
	rm -f "$html" "$svg" "$png"

	echo "Downloading:	$region	$htmlurl"

	if ! wget -q -O "$html" "${htmlurl}"; then
		echo "ERROR: failed downloading html: ${htmlurl}"
		continue
	fi

	if ! grep -q public_domain $html; then
		echo "WARNING: flag NOT in public domain; check license"
	fi

	svgurl="https:`cat "$html" | LANG=C sed 's@.*href="\(//upload.wikimedia.org/wikipedia/commons/[^"]*[.]svg\)".*@\1@' | grep '^//upload.wikimedia' | grep -v '/archive/' | head -n1`"
	svgdata="`wget -q -O - "$svgurl"`"
	if test "x$svgdata" = x; then
		echo "ERROR: failed downloading SVG: $svgurl"
		continue
	fi
	echo "$svgdata" > $svg.dos
	if ! dos2unix -q $svg.dos; then
		echo "ERROR: dos2unix failed."
		rm -f $svg.dos
		continue
	else
		mv $svg.dos $svg
	fi

	if ! rsvg-convert $svg > $png.tmp; then
		echo "ERROR rsvg-convert failed."
		rm -f $png.tmp
		continue
	fi

	if !  optipng -quiet $png.tmp; then
		echo "ERROR: optipng failed."
		rm -f $png.tmp
		continue
	else
		mv $png.tmp $png
	fi

done
