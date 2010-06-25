#!/bin/sh

cd $(dirname $0)
./compile.sh
mkdir -p pkg
export DESTDIR=$PWD/pkg
./install.sh
VER=$(grep 'version =' src/salix-live-installer.py | head -n 1 | sed "s/.*'\(.*\)'/\1/")
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
makepkg -l y -c n ../salix-live-installer-$VER-noarch-1plb.txz
cd ..
md5sum salix-live-installer-$VER-noarch-1plb.txz > salix-live-installer-$VER-noarch-1plb.md5
echo -e "python,parted,salixtools" > salix-live-installer-$VER-noarch-1plb.dep
rm -rf pkg
