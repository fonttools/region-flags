#!/bin/sh
IFS='	'
./regions-wp.py |
while read region pageurl ; do

	svg="svg/$region.svg"
	png="png/$region.png"

	test -s "$svg" && continue
	rm -f "$svg"

	echo "Downloading:	$region	$pageurl"

	page="`wget -q -O - "$pageurl"`"
	if test "x$page" = x; then
		echo "ERROR: failed downloading page: $pageurl"
		continue
	fi

	svgurl="https:`echo "$page" | LANG=C sed 's@.*href="\(//upload.wikimedia.org/wikipedia/commons/[^"]*[.]svg\)".*@\1@' | grep '^//upload.wikimedia' | grep -v '/archive/' | head -n1`"
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
