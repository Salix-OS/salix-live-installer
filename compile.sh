#!/bin/sh

cd $(dirname $0)
for i in `ls po/*.po`;do
	echo "Compiling `echo $i|sed "s|po/||"`"
	msgfmt $i -o `echo $i |sed "s/.po//"`.mo
done
intltool-merge po/ -d -u src/salix-live-installer.desktop.in src/salix-live-installer.desktop
intltool-merge po/ -d -u src/salix-live-installer-kde.desktop.in src/salix-live-installer-kde.desktop
