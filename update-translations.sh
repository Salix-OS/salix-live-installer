#!/bin/sh

intltool-extract --type="gettext/ini" src/salix-live-installer.desktop.in

xgettext --from-code=utf-8 \
	-L Glade \
	-o po/salix-live-installer.pot \
	src/salix-live-installer.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o po/salix-live-installer.pot \
	src/salix-live-installer.py
xgettext --from-code=utf-8 -j -L C -kN_ -o po/salix-live-installer.pot src/salix-live-installer.desktop.in.h

rm src/salix-live-installer.desktop.in.h

cd po
for i in `ls *.po`; do
	msgmerge -U $i salix-live-installer.pot
done
rm -f ./*~

