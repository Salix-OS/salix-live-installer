#!/bin/sh

VER=$(grep 'version =' src/salix-live-installer.py | head -n 1 | sed "s/.*'\(.*\)'/\1/")

cd $(dirname $0)
install -d -m 755 $DESTDIR/usr/doc/salix-live-installer-$VER
install -d -m 755 $DESTDIR/install
install -d -m 755 $DESTDIR/usr/sbin
install -d -m 755 $DESTDIR/usr/share/applications
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/24x24/apps
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/64x64/apps
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/128x128/apps
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/scalable/apps
install -d -m 755 $DESTDIR/usr/share/salix-live-installer

install -m 755 src/salix-live-installer.py $DESTDIR/usr/sbin/salix-live-installer.py
install -m 644 src/Goode-homolosine.jpg \
$DESTDIR/usr/share/salix-live-installer
install -m 644 src/salix-live-installer.glade \
$DESTDIR/usr/share/salix-live-installer
install -m 644 src/salix-live-installer.desktop \
$DESTDIR/usr/share/applications/
install -m 644 src/salix-live-installer-kde.desktop \
$DESTDIR/usr/share/applications/
install -m 644 icons/salix-live-installer-24.png \
$DESTDIR/usr/share/icons/hicolor/24x24/apps/salix-live-installer.png
install -m 644 icons/salix-live-installer-64.png \
$DESTDIR/usr/share/icons/hicolor/64x64/apps/salix-live-installer.png
install -m 644 icons/salix-live-installer-128.png \
$DESTDIR/usr/share/icons/hicolor/128x128/apps/salix-live-installer.png
install -m 644 icons/salix-live-installer.svg \
$DESTDIR/usr/share/icons/hicolor/scalable/apps/
install -m 644 src/salix-live-installer.png \
$DESTDIR/usr/share/salix-live-installer/

for i in `ls po/*.mo|sed "s|po/\(.*\).mo|\1|"`; do
	install -d -m 755 $DESTDIR/usr/share/locale/${i}/LC_MESSAGES
	install -m 644 po/${i}.mo \
	$DESTDIR/usr/share/locale/${i}/LC_MESSAGES/salix-live-installer.mo
done

for i in `ls docs`; do
	install -m 644 docs/${i} \
	$DESTDIR/usr/doc/salix-live-installer-$VER/
done
