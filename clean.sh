#!/bin/sh
cd $(dirname "$0")
find . -type f -name '*.pyc' -delete
find . -type f -name '*.mo' -delete
[ -d data/locale ] && rm -r data/locale
[ -d build ] && rm -r build
