#!/usr/bin/env sh

./regions.py | while read x y; do test -f "png/$x.png" || echo $x $y; done
