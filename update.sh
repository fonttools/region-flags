#!/usr/bin/env sh
set -ex

python3 ./regions-wp.py > SOURCES

rm -rf html svg png
mkdir -p html svg png

bash ./download-wp.sh true
bash ./make-aliases.sh

