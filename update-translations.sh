#!/bin/sh
cd $(dirname "$0")
# create data/po/salix-live-installer.pot template file from glade file
xgettext --from-code=utf-8 \
	-L Glade \
	-o data/po/salix-live-installer.pot \
	src/resources/salix-live-installer.glade
# update data/po/salix-live-installer.pot template file from python files
for p in \
    src/salix_live_installer/config.py \
    src/salix_live_installer/installer.py \
    src/salix_live_installer/installer_gtk.py \
    src/salix_live_installer/gathergui.py \
    src/salix_live_installer/installer_curses.py \
    ; do
  xgettext --from-code=utf-8 \
    -j \
    -L Python \
    -o data/po/salix-live-installer.pot \
    $p
done
# create data/salix-live-installer.desktop.in.h containing the key to translate
intltool-extract --type="gettext/ini" data/salix-live-installer.desktop.in
# use the .in.h file to update the template file
xgettext --from-code=utf-8 \
  -j \
  -L C \
  -kN_ \
  -o data/po/salix-live-installer.pot \
  data/salix-live-installer.desktop.in.h
# remove unused .in.h file
rm data/salix-live-installer.desktop.in.h
# update the po files using the pot file
(
  cd data/po
  for p in *.po; do
	  msgmerge -U $p salix-live-installer.pot
  done
  rm -f ./*~
)
