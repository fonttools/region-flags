#!/bin/sh

./regions.py | while read x y; do test -f "$x.png" || echo $x $y; done
