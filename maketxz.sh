#!/bin/sh

cd $(dirname $0)
./compile.sh
mkdir -p pkg
export DESTDIR=$PWD/pkg
./install.sh
VER=$(grep 'version =' src/salix-live-installer.py | head -n 1 | sed "s/.*'\(.*\)'/\1/")
RLZ=1plb
cd pkg
cat <<EOF > install/slack-desc
salix-live-installer: Salix Live Installer - Install Salix Standard from LiveCD.
salix-live-installer:
salix-live-installer: Salix Live Installer will enable you to install Salix
salix-live-installer: from the comfort of the graphical interface of Salix
salix-live-installer: LiveCD environment.
salix-live-installer:
salix-live-installer:
salix-live-installer:
salix-live-installer:
salix-live-installer:
salix-live-installer:
EOF
makepkg -l y -c n ../salix-live-installer-$VER-noarch-$RLZ.txz
cd ..
md5sum salix-live-installer-$VER-noarch-$RLZ.txz > salix-live-installer-$VER-noarch-$RLZ.md5
echo -e "gparted,python,salixtools" > salix-live-installer-$VER-noarch-$RLZ.dep
rm -rf pkg
