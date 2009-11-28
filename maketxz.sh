#!/bin/sh

cd $(dirname $0)
./compile.sh
mkdir -p pkg
export DESTDIR=$PWD/pkg
./install.sh
VER=$(grep 'Version=' src/salix-live-installer | cut -d\' -f2)
cd pkg
makepkg -l y -c n ../salix-live-installer-$VER-noarch-1plb.txz
cd ..
rm -rf pkg
