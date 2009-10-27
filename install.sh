#!/bin/sh

install -d -m 755 $DESTDIR/usr/sbin
install -d -m 755 $DESTDIR/usr/share/applications
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/24x24/apps
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/64x64/apps
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/128x128/apps
install -d -m 755 $DESTDIR/usr/share/icons/hicolor/scalable/apps
install -d -m 755 $DESTDIR/usr/share/salix-live-installer

install -m 755 src/salix-live-installer $DESTDIR/usr/sbin/salix-live-installer
install -m 644 salix-live-installer.desktop \
$DESTDIR/usr/share/applications/
install -m 644 salix-live-installer-kde.desktop \
$DESTDIR/usr/share/applications/
install -m 644 icons/salix-live-installer-24.png \
$DESTDIR/usr/share/icons/hicolor/24x24/apps/salix-live-installer.png
install -m 644 icons/salix-live-installer-64.png \
$DESTDIR/usr/share/icons/hicolor/64x64/apps/salix-live-installer.png
install -m 644 icons/salix-live-installer-128.png \
$DESTDIR/usr/share/icons/hicolor/128x128/apps/salix-live-installer.png
install -m 644 icons/salix-live-installer.svg \
$DESTDIR/usr/share/icons/hicolor/scalable/apps/

for i in `ls locale/*.mo|sed "s|locale/\(.*\).mo|\1|"`; do
	install -d -m 755 $DESTDIR/usr/share/locale/${i}/LC_MESSAGES
	install -m 644 locale/${i}.mo \
	$DESTDIR/usr/share/locale/${i}/LC_MESSAGES/salix-live-installer.mo
done

