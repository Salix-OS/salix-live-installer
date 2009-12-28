#!/bin/sh

cd $(dirname $0)
./compile.sh
mkdir -p pkg
export DESTDIR=$PWD/pkg
./install.sh
VER=$(grep 'version =' src/salix-live-installer.py | head -n 1 | sed "s/.*'\(.*\)' - \([0-9]*\).*/\1.\2/")
cd pkg
makepkg -l y -c n ../salix-live-installer-$VER-noarch-1plb.txz
cd ..
rm -rf pkg
